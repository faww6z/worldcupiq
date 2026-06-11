from __future__ import annotations

from datetime import datetime, timezone
from math import exp
from typing import Literal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.ml.elo import expected_result, get_team_elo
from app.ml.poisson import result_probabilities, scoreline_probabilities
from app.models import Match, ModelRun, Prediction
from app.schemas import PredictionResponse
from app.schemas.prediction import PredictedScore, ScorelineProbability

MODEL_VERSION = "v0.1-seeded-elo-poisson"
GLOBAL_AVG_GOALS = 1.35
HOST_GOAL_MULTIPLIER = 1.10

TEAM_STRENGTHS: dict[str, tuple[float, float]] = {
    "ARG": (1.24, 0.78),
    "ESP": (1.22, 0.80),
    "FRA": (1.23, 0.79),
    "ENG": (1.18, 0.83),
    "BRA": (1.18, 0.84),
    "POR": (1.17, 0.85),
    "NED": (1.16, 0.86),
    "BEL": (1.12, 0.90),
    "GER": (1.14, 0.91),
    "CRO": (1.07, 0.91),
    "URU": (1.08, 0.88),
    "COL": (1.08, 0.92),
    "MAR": (1.06, 0.86),
    "USA": (1.06, 0.94),
    "MEX": (1.04, 0.94),
    "SUI": (1.03, 0.93),
    "JPN": (1.04, 0.95),
    "SEN": (1.02, 0.94),
    "ECU": (1.00, 0.95),
    "IRN": (0.99, 0.96),
    "KOR": (1.01, 0.98),
    "AUS": (0.99, 1.00),
    "SWE": (1.01, 0.99),
    "CAN": (0.99, 1.01),
    "TUR": (1.00, 1.00),
    "CIV": (0.99, 1.02),
    "EGY": (0.97, 0.99),
    "NOR": (1.00, 1.01),
    "PAR": (0.96, 1.00),
    "AUT": (0.99, 1.02),
    "SCO": (0.96, 1.02),
    "QAT": (0.94, 1.05),
    "TUN": (0.93, 1.02),
    "GHA": (0.96, 1.05),
    "KSA": (0.92, 1.07),
    "RSA": (0.91, 1.06),
    "PAN": (0.91, 1.08),
    "BIH": (0.92, 1.06),
    "CZE": (0.94, 1.04),
    "UZB": (0.91, 1.05),
    "ALG": (0.93, 1.04),
    "IRQ": (0.89, 1.10),
    "JOR": (0.88, 1.10),
    "CPV": (0.90, 1.07),
    "NZL": (0.88, 1.09),
    "HAI": (0.87, 1.12),
    "CUW": (0.86, 1.12),
    "COD": (0.88, 1.11),
}


def _round_probability(value: float) -> float:
    return round(value, 4)


def _team_strength(team_code: str) -> tuple[float, float]:
    return TEAM_STRENGTHS.get(team_code.upper(), (1.0, 1.0))


def _elo_goal_multiplier(elo_diff: float) -> float:
    return min(max(exp(elo_diff / 1000), 0.72), 1.38)


def _expected_goals(match: Match, elo_a: float, elo_b: float) -> tuple[float, float]:
    attack_a, defence_a = _team_strength(match.team_a.code)
    attack_b, defence_b = _team_strength(match.team_b.code)
    elo_multiplier_a = _elo_goal_multiplier(elo_a - elo_b)
    elo_multiplier_b = _elo_goal_multiplier(elo_b - elo_a)
    host_multiplier_a = HOST_GOAL_MULTIPLIER if match.team_a.is_host else 1.0
    host_multiplier_b = HOST_GOAL_MULTIPLIER if match.team_b.is_host else 1.0

    expected_a = GLOBAL_AVG_GOALS * attack_a * defence_b * elo_multiplier_a * host_multiplier_a
    expected_b = GLOBAL_AVG_GOALS * attack_b * defence_a * elo_multiplier_b * host_multiplier_b
    return round(min(max(expected_a, 0.2), 3.8), 2), round(min(max(expected_b, 0.2), 3.8), 2)


def _confidence_label(team_a_win: float, draw: float, team_b_win: float) -> str:
    strongest = max(team_a_win, draw, team_b_win)
    if strongest >= 0.58:
        return "high"
    if strongest >= 0.45:
        return "medium"
    return "low"


def _explain(match: Match, elo_a: float, elo_b: float, expected_goals_a: float, expected_goals_b: float) -> list[str]:
    explanations: list[str] = []
    elo_diff = elo_a - elo_b
    attack_a, defence_a = _team_strength(match.team_a.code)
    attack_b, defence_b = _team_strength(match.team_b.code)

    if elo_diff > 75:
        explanations.append(f"{match.team_a.name} has the stronger seeded Elo-style rating.")
    elif elo_diff < -75:
        explanations.append(f"{match.team_b.name} has the stronger seeded Elo-style rating.")
    else:
        explanations.append("The seeded Elo-style ratings are close, so the match is treated as balanced.")

    if match.team_a.is_host:
        explanations.append(f"{match.team_a.name} receives a small host advantage adjustment.")
    if match.team_b.is_host:
        explanations.append(f"{match.team_b.name} receives a small host advantage adjustment.")

    if attack_a - attack_b > 0.08:
        explanations.append(f"{match.team_a.name} has the stronger seeded attacking profile.")
    elif attack_b - attack_a > 0.08:
        explanations.append(f"{match.team_b.name} has the stronger seeded attacking profile.")

    if defence_a + 0.08 < defence_b:
        explanations.append(f"{match.team_a.name} has the sturdier seeded defensive profile.")
    elif defence_b + 0.08 < defence_a:
        explanations.append(f"{match.team_b.name} has the sturdier seeded defensive profile.")

    if abs(expected_goals_a - expected_goals_b) < 0.25:
        explanations.append("Expected goals are close, increasing the draw and one-goal-margin outcomes.")

    return explanations[:5]


def _prediction_to_response(prediction: Prediction) -> PredictionResponse:
    return PredictionResponse(
        match_id=prediction.match_id,
        model_version=prediction.model_version,
        team_a=prediction.match.team_a,
        team_b=prediction.match.team_b,
        team_a_win_prob=prediction.team_a_win_prob,
        draw_prob=prediction.draw_prob,
        team_b_win_prob=prediction.team_b_win_prob,
        expected_goals_a=prediction.expected_goals_a,
        expected_goals_b=prediction.expected_goals_b,
        predicted_score=PredictedScore(
            team_a=prediction.predicted_score_a,
            team_b=prediction.predicted_score_b,
        ),
        top_scorelines=[
            ScorelineProbability(score=scoreline["score"], probability=scoreline["probability"])
            for scoreline in prediction.scoreline_probs_json
        ],
        confidence_label=prediction.confidence_label,
        explanation=prediction.explanation_json,
    )


def _stored_prediction(db: Session, match_id: int) -> Prediction | None:
    query = (
        select(Prediction)
        .options(joinedload(Prediction.match).joinedload(Match.team_a), joinedload(Prediction.match).joinedload(Match.team_b))
        .where(Prediction.match_id == match_id, Prediction.model_version == MODEL_VERSION)
    )
    return db.scalars(query).unique().first()


def _build_prediction_response(db: Session, match_id: int) -> PredictionResponse | None:
    query = (
        select(Match)
        .options(joinedload(Match.team_a), joinedload(Match.team_b))
        .where(Match.id == match_id)
    )
    match = db.scalars(query).unique().first()
    if match is None:
        return None

    elo_a = get_team_elo(match.team_a.code)
    elo_b = get_team_elo(match.team_b.code)
    expected_goals_a, expected_goals_b = _expected_goals(match, elo_a, elo_b)
    scorelines = scoreline_probabilities(expected_goals_a, expected_goals_b)
    team_a_win, draw, team_b_win = result_probabilities(scorelines)
    top_scorelines = sorted(scorelines, key=lambda scoreline: scoreline.probability, reverse=True)[:5]
    predicted = top_scorelines[0]

    # The Elo expected result is not returned directly yet, but computing it keeps
    # this service aligned with the baseline model and easy to expose later.
    expected_result(elo_a, elo_b)

    return PredictionResponse(
        match_id=match.id,
        model_version=MODEL_VERSION,
        team_a=match.team_a,
        team_b=match.team_b,
        team_a_win_prob=_round_probability(team_a_win),
        draw_prob=_round_probability(draw),
        team_b_win_prob=_round_probability(team_b_win),
        expected_goals_a=expected_goals_a,
        expected_goals_b=expected_goals_b,
        predicted_score=PredictedScore(team_a=predicted.score_a, team_b=predicted.score_b),
        top_scorelines=[
            ScorelineProbability(
                score=f"{scoreline.score_a}-{scoreline.score_b}",
                probability=_round_probability(scoreline.probability),
            )
            for scoreline in top_scorelines
        ],
        confidence_label=_confidence_label(team_a_win, draw, team_b_win),
        explanation=_explain(match, elo_a, elo_b, expected_goals_a, expected_goals_b),
    )


def _record_model_run(
    db: Session,
    run_type: Literal["lazy_prediction", "manual_prediction"],
    status: Literal["completed", "failed"],
    notes: str | None = None,
    metrics_json: dict[str, object] | None = None,
) -> ModelRun:
    now = datetime.now(timezone.utc)
    model_run = ModelRun(
        model_version=MODEL_VERSION,
        run_type=run_type,
        started_at=now,
        finished_at=now,
        status=status,
        notes=notes,
        metrics_json=metrics_json,
    )
    db.add(model_run)
    return model_run


def _upsert_prediction(db: Session, response: PredictionResponse) -> Prediction:
    existing = _stored_prediction(db, response.match_id)
    scoreline_probs_json = [scoreline.model_dump() for scoreline in response.top_scorelines]
    values = {
        "team_a_win_prob": response.team_a_win_prob,
        "draw_prob": response.draw_prob,
        "team_b_win_prob": response.team_b_win_prob,
        "expected_goals_a": response.expected_goals_a,
        "expected_goals_b": response.expected_goals_b,
        "predicted_score_a": response.predicted_score.team_a,
        "predicted_score_b": response.predicted_score.team_b,
        "confidence_label": response.confidence_label,
        "explanation_json": response.explanation,
        "scoreline_probs_json": scoreline_probs_json,
    }
    if existing is None:
        prediction = Prediction(
            match_id=response.match_id,
            model_version=response.model_version,
            **values,
        )
        db.add(prediction)
    else:
        prediction = existing
        for key, value in values.items():
            setattr(prediction, key, value)
    db.flush()
    return prediction


def _generate_and_persist_prediction(
    db: Session,
    match_id: int,
    run_type: Literal["lazy_prediction", "manual_prediction"],
) -> PredictionResponse | None:
    response = _build_prediction_response(db, match_id)
    if response is None:
        return None

    try:
        prediction = _upsert_prediction(db, response)
        _record_model_run(
            db,
            run_type=run_type,
            status="completed",
            metrics_json={
                "match_id": match_id,
                "team_a_win_prob": response.team_a_win_prob,
                "draw_prob": response.draw_prob,
                "team_b_win_prob": response.team_b_win_prob,
            },
        )
        db.commit()
        db.refresh(prediction)
        prediction = _stored_prediction(db, match_id)
        if prediction is None:
            return response
        return _prediction_to_response(prediction)
    except IntegrityError:
        db.rollback()
        existing = _stored_prediction(db, match_id)
        if existing is not None:
            return _prediction_to_response(existing)
        raise
    except Exception:
        db.rollback()
        _record_model_run(db, run_type=run_type, status="failed", notes=f"Failed to generate prediction for match {match_id}")
        db.commit()
        raise


def get_prediction_for_match(db: Session, match_id: int) -> PredictionResponse | None:
    prediction = _stored_prediction(db, match_id)
    if prediction is not None:
        return _prediction_to_response(prediction)
    return _generate_and_persist_prediction(db, match_id, run_type="lazy_prediction")


def regenerate_prediction_for_match(db: Session, match_id: int) -> PredictionResponse | None:
    return _generate_and_persist_prediction(db, match_id, run_type="manual_prediction")
