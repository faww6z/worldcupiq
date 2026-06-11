from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Group, Match, Prediction, Team

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SEED_DIR = REPO_ROOT / "data" / "seed"


@dataclass
class SeedResult:
    groups: int = 0
    teams: int = 0
    matches: int = 0


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "y"}


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _parse_int(value: str) -> int | None:
    if value == "":
        return None
    return int(value)


def seed_groups(db: Session, seed_dir: Path) -> int:
    changed = 0
    for row in _read_csv(seed_dir / "groups.csv"):
        group = db.scalar(select(Group).where(Group.code == row["code"]))
        if group is None:
            group = Group(code=row["code"], name=row["name"])
            db.add(group)
            changed += 1
        else:
            group.name = row["name"]
    db.flush()
    return changed


def seed_teams(db: Session, seed_dir: Path) -> int:
    changed = 0
    rows = _read_csv(seed_dir / "teams.csv")
    seeded_codes = {row["code"] for row in rows}
    seeded_group_codes = {row["group_code"] for row in rows if row["group_code"]}

    for row in rows:
        team = db.scalar(select(Team).where(Team.code == row["code"]))
        values = {
            "name": row["name"],
            "group_code": row["group_code"] or None,
            "confederation": row["confederation"] or None,
            "is_host": _parse_bool(row["is_host"]),
        }
        if team is None:
            team = Team(code=row["code"], **values)
            db.add(team)
            changed += 1
        else:
            for key, value in values.items():
                setattr(team, key, value)

    stale_grouped_teams = db.scalars(
        select(Team).where(Team.group_code.in_(seeded_group_codes), ~Team.code.in_(seeded_codes))
    ).all()
    for team in stale_grouped_teams:
        team.group_code = None

    db.flush()
    return changed


def seed_matches(db: Session, seed_dir: Path) -> int:
    changed = 0
    rows = _read_csv(seed_dir / "fixtures.csv")
    seeded_match_codes = {row["match_code"] for row in rows}
    team_by_code = {team.code: team for team in db.scalars(select(Team)).all()}
    stale_matches = db.scalars(
        select(Match).where(
            Match.stage == "group",
            Match.match_code.like("WC2026-G%"),
            ~Match.match_code.in_(seeded_match_codes),
        )
    ).all()
    stale_match_ids = [match.id for match in stale_matches]
    if stale_match_ids:
        for prediction in db.scalars(select(Prediction).where(Prediction.match_id.in_(stale_match_ids))).all():
            db.delete(prediction)
        for match in stale_matches:
            db.delete(match)
        db.flush()

    for row in rows:
        team_a = team_by_code[row["team_a_code"]]
        team_b = team_by_code[row["team_b_code"]]
        match = db.scalar(select(Match).where(Match.match_code == row["match_code"]))
        values = {
            "date": _parse_date(row["date"]),
            "time_utc": _parse_datetime(row["time_utc"]),
            "stage": row["stage"],
            "group_code": row["group_code"] or None,
            "team_a_id": team_a.id,
            "team_b_id": team_b.id,
            "venue": row["venue"] or None,
            "city": row["city"] or None,
            "status": row["status"],
            "score_a": _parse_int(row["score_a"]),
            "score_b": _parse_int(row["score_b"]),
        }
        if match is None:
            match = Match(match_code=row["match_code"], **values)
            db.add(match)
            changed += 1
        else:
            for key, value in values.items():
                setattr(match, key, value)
    db.flush()
    return changed


def seed_all(db: Session | None = None, seed_dir: Path = DEFAULT_SEED_DIR) -> SeedResult:
    owns_session = db is None
    if db is None:
        db = SessionLocal()

    try:
        result = SeedResult(
            groups=seed_groups(db, seed_dir),
            teams=seed_teams(db, seed_dir),
            matches=seed_matches(db, seed_dir),
        )
        db.commit()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        if owns_session:
            db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed WorldCupIQ MVP data.")
    parser.add_argument("--seed-dir", type=Path, default=DEFAULT_SEED_DIR)
    args = parser.parse_args()
    result = seed_all(seed_dir=args.seed_dir)
    print(f"Seeded groups={result.groups} teams={result.teams} matches={result.matches}")


if __name__ == "__main__":
    main()
