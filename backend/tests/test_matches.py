from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.data_pipeline.seed_worldcup import seed_all


def test_get_upcoming_matches_returns_seeded_matches_in_date_order(client: TestClient, db_session: Session) -> None:
    seed_all(db_session)

    response = client.get("/matches/upcoming")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 72
    assert payload[0]["match_code"] == "WC2026-GA-001"
    assert payload[0]["team_a"]["name"] == "Mexico"
    assert payload[0]["team_b"]["name"] == "South Africa"
    dates = [date.fromisoformat(match["date"]) for match in payload]
    assert dates == sorted(dates)


def test_get_match_by_id_returns_404_for_missing_match(client: TestClient) -> None:
    response = client.get("/matches/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match not found"
