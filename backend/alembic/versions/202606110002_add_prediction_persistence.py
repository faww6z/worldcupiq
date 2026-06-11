"""add prediction persistence

Revision ID: 202606110002
Revises: 202606110001
Create Date: 2026-06-11 00:00:01.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "202606110002"
down_revision: Union[str, None] = "202606110001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

json_type = sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql")


def upgrade() -> None:
    op.create_table(
        "model_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_version", sa.String(length=80), nullable=False),
        sa.Column("run_type", sa.String(length=60), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metrics_json", json_type, nullable=True),
    )
    op.create_index("ix_model_runs_model_version", "model_runs", ["model_version"])
    op.create_index("ix_model_runs_run_type", "model_runs", ["run_type"])
    op.create_index("ix_model_runs_status", "model_runs", ["status"])

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("model_version", sa.String(length=80), nullable=False),
        sa.Column("team_a_win_prob", sa.Float(), nullable=False),
        sa.Column("draw_prob", sa.Float(), nullable=False),
        sa.Column("team_b_win_prob", sa.Float(), nullable=False),
        sa.Column("expected_goals_a", sa.Float(), nullable=False),
        sa.Column("expected_goals_b", sa.Float(), nullable=False),
        sa.Column("predicted_score_a", sa.Integer(), nullable=False),
        sa.Column("predicted_score_b", sa.Integer(), nullable=False),
        sa.Column("confidence_label", sa.String(length=40), nullable=False),
        sa.Column("explanation_json", json_type, nullable=False),
        sa.Column("scoreline_probs_json", json_type, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"]),
        sa.UniqueConstraint("match_id", "model_version", name="uq_predictions_match_model"),
    )
    op.create_index("ix_predictions_match_id", "predictions", ["match_id"])
    op.create_index("ix_predictions_model_version", "predictions", ["model_version"])


def downgrade() -> None:
    op.drop_index("ix_predictions_model_version", table_name="predictions")
    op.drop_index("ix_predictions_match_id", table_name="predictions")
    op.drop_table("predictions")
    op.drop_index("ix_model_runs_status", table_name="model_runs")
    op.drop_index("ix_model_runs_run_type", table_name="model_runs")
    op.drop_index("ix_model_runs_model_version", table_name="model_runs")
    op.drop_table("model_runs")

