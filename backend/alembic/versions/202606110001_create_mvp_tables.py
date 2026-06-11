"""create mvp tables

Revision ID: 202606110001
Revises:
Create Date: 2026-06-11 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "202606110001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=8), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_groups_code", "groups", ["code"])

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=8), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("group_code", sa.String(length=8), nullable=True),
        sa.Column("confederation", sa.String(length=40), nullable=True),
        sa.Column("is_host", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["group_code"], ["groups.code"]),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_teams_code", "teams", ["code"])
    op.create_index("ix_teams_group_code", "teams", ["group_code"])

    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("match_code", sa.String(length=32), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("time_utc", sa.DateTime(timezone=True), nullable=True),
        sa.Column("stage", sa.String(length=40), nullable=False),
        sa.Column("group_code", sa.String(length=8), nullable=True),
        sa.Column("team_a_id", sa.Integer(), nullable=False),
        sa.Column("team_b_id", sa.Integer(), nullable=False),
        sa.Column("venue", sa.String(length=160), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("score_a", sa.Integer(), nullable=True),
        sa.Column("score_b", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("status in ('scheduled', 'live', 'finished', 'postponed')", name="ck_matches_status"),
        sa.ForeignKeyConstraint(["group_code"], ["groups.code"]),
        sa.ForeignKeyConstraint(["team_a_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["team_b_id"], ["teams.id"]),
        sa.UniqueConstraint("match_code"),
    )
    op.create_index("ix_matches_date", "matches", ["date"])
    op.create_index("ix_matches_group_code", "matches", ["group_code"])
    op.create_index("ix_matches_match_code", "matches", ["match_code"])
    op.create_index("ix_matches_status", "matches", ["status"])


def downgrade() -> None:
    op.drop_index("ix_matches_status", table_name="matches")
    op.drop_index("ix_matches_match_code", table_name="matches")
    op.drop_index("ix_matches_group_code", table_name="matches")
    op.drop_index("ix_matches_date", table_name="matches")
    op.drop_table("matches")
    op.drop_index("ix_teams_group_code", table_name="teams")
    op.drop_index("ix_teams_code", table_name="teams")
    op.drop_table("teams")
    op.drop_index("ix_groups_code", table_name="groups")
    op.drop_table("groups")

