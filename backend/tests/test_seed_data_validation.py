import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from app.data_pipeline.seed_worldcup import DEFAULT_SEED_DIR


def _read_seed_csv(name: str) -> list[dict[str, str]]:
    with Path(DEFAULT_SEED_DIR / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def test_team_seed_has_four_teams_per_group() -> None:
    teams = _read_seed_csv("teams.csv")
    teams_per_group = Counter(team["group_code"] for team in teams)

    assert len(teams) == 48
    assert teams_per_group == {group_code: 4 for group_code in "ABCDEFGHIJKL"}
    assert "IRQ" in {team["code"] for team in teams}
    assert "BOL" not in {team["code"] for team in teams}


def test_fixture_seed_contains_full_group_stage_schedule() -> None:
    fixtures = _read_seed_csv("fixtures.csv")
    match_codes = [fixture["match_code"] for fixture in fixtures]
    fixtures_per_group = Counter(fixture["group_code"] for fixture in fixtures)
    local_dates = [date.fromisoformat(fixture["date"]) for fixture in fixtures]

    assert len(fixtures) == 72
    assert len(match_codes) == len(set(match_codes))
    assert fixtures_per_group == {group_code: 6 for group_code in "ABCDEFGHIJKL"}
    assert min(local_dates) == date(2026, 6, 11)
    assert max(local_dates) == date(2026, 6, 27)
    assert all(fixture["stage"] == "group" for fixture in fixtures)
    assert all(fixture["status"] == "scheduled" for fixture in fixtures)
    assert fixtures[0]["match_code"] == "WC2026-GA-001"
    assert fixtures[-1]["match_code"] == "WC2026-GK-072"

    for fixture in fixtures:
        datetime.fromisoformat(fixture["time_utc"].replace("Z", "+00:00"))


def test_fixture_seed_references_known_teams_once_per_round() -> None:
    teams = _read_seed_csv("teams.csv")
    fixtures = _read_seed_csv("fixtures.csv")
    team_codes = {team["code"] for team in teams}
    fixture_team_counts = Counter(
        team_code
        for fixture in fixtures
        for team_code in (fixture["team_a_code"], fixture["team_b_code"])
    )

    assert set(fixture_team_counts) == team_codes
    assert set(fixture_team_counts.values()) == {3}
