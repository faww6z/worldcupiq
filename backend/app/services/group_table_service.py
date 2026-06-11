from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Match, Team
from app.schemas.group import GroupTableResponse, GroupTableRow


@dataclass
class Standing:
    team_id: int
    team_code: str
    team_name: str
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


def _apply_result(standing: Standing, goals_for: int, goals_against: int) -> None:
    standing.played += 1
    standing.goals_for += goals_for
    standing.goals_against += goals_against
    if goals_for > goals_against:
        standing.wins += 1
        standing.points += 3
    elif goals_for == goals_against:
        standing.draws += 1
        standing.points += 1
    else:
        standing.losses += 1


def _sorted_standings(standings: dict[int, Standing]) -> list[Standing]:
    return sorted(
        standings.values(),
        key=lambda row: (-row.points, -row.goal_difference, -row.goals_for, row.team_name),
    )


def build_group_table(db: Session, group_code: str) -> GroupTableResponse:
    normalized_group_code = group_code.upper()
    teams = list(
        db.scalars(select(Team).where(Team.group_code == normalized_group_code).order_by(Team.name.asc()))
    )
    standings = {
        team.id: Standing(team_id=team.id, team_code=team.code, team_name=team.name)
        for team in teams
    }

    matches = list(
        db.scalars(
            select(Match)
            .options(joinedload(Match.team_a), joinedload(Match.team_b))
            .where(Match.group_code == normalized_group_code, Match.status == "finished")
        ).unique()
    )

    for match in matches:
        if match.score_a is None or match.score_b is None:
            continue
        if match.team_a_id in standings:
            _apply_result(standings[match.team_a_id], match.score_a, match.score_b)
        if match.team_b_id in standings:
            _apply_result(standings[match.team_b_id], match.score_b, match.score_a)

    rows = [
        GroupTableRow(
            rank=index + 1,
            team_id=standing.team_id,
            team_code=standing.team_code,
            team_name=standing.team_name,
            played=standing.played,
            wins=standing.wins,
            draws=standing.draws,
            losses=standing.losses,
            goals_for=standing.goals_for,
            goals_against=standing.goals_against,
            goal_difference=standing.goal_difference,
            points=standing.points,
        )
        for index, standing in enumerate(_sorted_standings(standings))
    ]
    return GroupTableResponse(group_code=normalized_group_code, rows=rows)

