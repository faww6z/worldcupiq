from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data_pipeline.seed_worldcup import seed_all
from app.models import Match
from app.services.group_table_service import build_group_table


def test_group_table_points_goal_difference_and_sorting(db_session: Session) -> None:
    seed_all(db_session)
    mexico_match = db_session.scalar(select(Match).where(Match.match_code == "WC2026-GA-001"))
    korea_match = db_session.scalar(select(Match).where(Match.match_code == "WC2026-GA-002"))
    mexico_match.status = "finished"
    mexico_match.score_a = 2
    mexico_match.score_b = 0
    korea_match.status = "finished"
    korea_match.score_a = 1
    korea_match.score_b = 1
    db_session.commit()

    table = build_group_table(db_session, "A")

    assert [row.team_code for row in table.rows] == ["MEX", "CZE", "KOR", "RSA"]
    assert table.rows[0].points == 3
    assert table.rows[0].goal_difference == 2
    assert table.rows[1].points == 1
    assert table.rows[1].goals_for == 1
    assert table.rows[3].losses == 1


def test_group_table_ignores_scheduled_matches(db_session: Session) -> None:
    seed_all(db_session)

    table = build_group_table(db_session, "B")

    assert len(table.rows) == 4
    assert all(row.played == 0 for row in table.rows)
    assert all(row.points == 0 for row in table.rows)

