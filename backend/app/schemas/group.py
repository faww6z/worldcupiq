from pydantic import BaseModel, ConfigDict


class GroupSummary(BaseModel):
    id: int
    code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class GroupTableRow(BaseModel):
    rank: int
    team_id: int
    team_code: str
    team_name: str
    played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int


class GroupTableResponse(BaseModel):
    group_code: str
    rows: list[GroupTableRow]

