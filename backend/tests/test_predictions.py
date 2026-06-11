from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.data_pipeline.seed_worldcup import seed_all
from app.models import ModelRun, Prediction


def test_get_prediction_by_match_id_returns_model_output(client: TestClient, db_session: Session) -> None:
    seed_all(db_session)

    response = client.get("/predictions/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["match_id"] == 1
    assert payload["model_version"] == "v0.1-seeded-elo-poisson"
    assert payload["team_a"]["name"] == "Mexico"
    assert payload["team_b"]["name"] == "South Africa"
    assert payload["expected_goals_a"] > 0
    assert payload["expected_goals_b"] > 0
    assert len(payload["top_scorelines"]) == 5
    probability_sum = payload["team_a_win_prob"] + payload["draw_prob"] + payload["team_b_win_prob"]
    assert abs(probability_sum - 1) < 0.001
    assert payload["explanation"]


def test_get_prediction_persists_output_without_duplicate_rows(client: TestClient, db_session: Session) -> None:
    seed_all(db_session)

    first_response = client.get("/predictions/1")
    second_response = client.get("/predictions/1")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json() == second_response.json()
    prediction_count = db_session.scalar(select(func.count()).select_from(Prediction))
    run_count = db_session.scalar(select(func.count()).select_from(ModelRun))
    assert prediction_count == 1
    assert run_count == 1
    stored_prediction = db_session.scalar(select(Prediction).where(Prediction.match_id == 1))
    assert stored_prediction.model_version == "v0.1-seeded-elo-poisson"
    assert stored_prediction.scoreline_probs_json[0]["score"] == first_response.json()["top_scorelines"][0]["score"]


def test_generate_prediction_updates_persisted_output_and_records_manual_run(
    client: TestClient,
    db_session: Session,
) -> None:
    seed_all(db_session)

    get_response = client.get("/predictions/1")
    post_response = client.post("/predictions/generate/1")

    assert get_response.status_code == 200
    assert post_response.status_code == 200
    prediction_count = db_session.scalar(select(func.count()).select_from(Prediction))
    run_count = db_session.scalar(select(func.count()).select_from(ModelRun))
    manual_run_count = db_session.scalar(select(func.count()).select_from(ModelRun).where(ModelRun.run_type == "manual_prediction"))
    assert prediction_count == 1
    assert run_count == 2
    assert manual_run_count == 1


def test_get_prediction_by_match_id_returns_404_for_missing_match(client: TestClient) -> None:
    response = client.get("/predictions/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match not found"
