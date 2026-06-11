from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Match
from app.schemas import MatchDetail, MatchListItem

router = APIRouter(prefix="/matches", tags=["matches"])


def _base_match_query():
    return (
        select(Match)
        .options(joinedload(Match.team_a), joinedload(Match.team_b))
        .order_by(Match.date.asc(), Match.time_utc.asc(), Match.id.asc())
    )


@router.get("", response_model=list[MatchListItem])
def list_matches(
    group_code: str | None = Query(default=None),
    team_code: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Match]:
    query = _base_match_query()
    if group_code:
        query = query.where(Match.group_code == group_code.upper())
    if status:
        query = query.where(Match.status == status.lower())
    if team_code:
        code = team_code.upper()
        query = query.where(Match.team_a.has(code=code) | Match.team_b.has(code=code))
    return list(db.scalars(query).unique())


@router.get("/upcoming", response_model=list[MatchListItem])
def list_upcoming_matches(db: Session = Depends(get_db)) -> list[Match]:
    query = _base_match_query().where(Match.status == "scheduled")
    return list(db.scalars(query).unique())


@router.get("/{match_id}", response_model=MatchDetail)
def get_match(match_id: int, db: Session = Depends(get_db)) -> Match:
    query = _base_match_query().where(Match.id == match_id)
    match = db.scalars(query).unique().first()
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

