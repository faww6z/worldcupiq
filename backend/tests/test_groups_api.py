from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.data_pipeline.seed_worldcup import seed_all


def test_get_groups(client: TestClient, db_session: Session) -> None:
    seed_all(db_session)

    response = client.get("/groups")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 12
    assert payload[0]["code"] == "A"


def test_get_group_table(client: TestClient, db_session: Session) -> None:
    seed_all(db_session)

    response = client.get("/groups/A/table")

    assert response.status_code == 200
    payload = response.json()
    assert payload["group_code"] == "A"
    assert len(payload["rows"]) == 4
    assert payload["rows"][0]["rank"] == 1


def test_get_group_table_returns_404_for_missing_group(client: TestClient) -> None:
    response = client.get("/groups/Z/table")

    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"

