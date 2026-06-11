from pydantic import BaseModel

from app.schemas.match import TeamSummary


class PredictedScore(BaseModel):
    team_a: int
    team_b: int


class ScorelineProbability(BaseModel):
    score: str
    probability: float


class PredictionResponse(BaseModel):
    match_id: int
    model_version: str
    team_a: TeamSummary
    team_b: TeamSummary
    team_a_win_prob: float
    draw_prob: float
    team_b_win_prob: float
    expected_goals_a: float
    expected_goals_b: float
    predicted_score: PredictedScore
    top_scorelines: list[ScorelineProbability]
    confidence_label: str
    explanation: list[str]

