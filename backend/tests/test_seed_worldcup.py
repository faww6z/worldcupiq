from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_pipeline.seed_worldcup import seed_all
from app.models import Group, Match, Team


def test_seed_script_imports_data_idempotently(db_session: Session) -> None:
    first = seed_all(db_session)
    second = seed_all(db_session)

    assert first.groups == 12
    assert first.teams == 48
    assert first.matches == 72
    assert second.groups == 0
    assert second.teams == 0
    assert second.matches == 0
    assert db_session.scalar(select(Group).where(Group.code == "A")).name == "Group A"
    assert db_session.scalar(select(Team).where(Team.code == "MEX")).name == "Mexico"
    assert db_session.scalar(select(Team).where(Team.code == "IRQ")).name == "Iraq"
    assert db_session.scalar(select(Match).where(Match.match_code == "WC2026-GA-001")).status == "scheduled"


def test_seed_script_detaches_stale_seeded_group_assignments(db_session: Session) -> None:
    db_session.add(Group(code="I", name="Group I"))
    db_session.add(Team(code="BOL", name="Bolivia", group_code="I", confederation="CONMEBOL", is_host=False))
    db_session.commit()

    seed_all(db_session)

    stale_team = db_session.scalar(select(Team).where(Team.code == "BOL"))
    assert stale_team is not None
    assert stale_team.group_code is None


def test_seed_script_removes_stale_group_stage_fixtures(db_session: Session) -> None:
    seed_all(db_session)
    mexico = db_session.scalar(select(Team).where(Team.code == "MEX"))
    south_africa = db_session.scalar(select(Team).where(Team.code == "RSA"))
    db_session.add(
        Match(
            match_code="WC2026-GA-999",
            date=date(2026, 6, 30),
            stage="group",
            group_code="A",
            team_a_id=mexico.id,
            team_b_id=south_africa.id,
            status="scheduled",
        )
    )
    db_session.commit()

    seed_all(db_session)

    assert db_session.scalar(select(Match).where(Match.match_code == "WC2026-GA-999")) is None
