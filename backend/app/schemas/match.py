from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TeamSummary(BaseModel):
    id: int
    code: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class MatchListItem(BaseModel):
    id: int
    match_code: str
    date: date
    time_utc: datetime | None
    stage: str
    group_code: str | None
    team_a: TeamSummary
    team_b: TeamSummary
    venue: str | None
    city: str | None
    status: str
    score_a: int | None
    score_b: int | None

    model_config = ConfigDict(from_attributes=True)


class MatchDetail(MatchListItem):
    pass

