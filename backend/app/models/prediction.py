from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

json_type = JSON().with_variant(postgresql.JSONB(astext_type=Text()), "postgresql")


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (
        UniqueConstraint("match_id", "model_version", name="uq_predictions_match_model"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), index=True)
    model_version: Mapped[str] = mapped_column(String(80), index=True)
    team_a_win_prob: Mapped[float] = mapped_column(Float)
    draw_prob: Mapped[float] = mapped_column(Float)
    team_b_win_prob: Mapped[float] = mapped_column(Float)
    expected_goals_a: Mapped[float] = mapped_column(Float)
    expected_goals_b: Mapped[float] = mapped_column(Float)
    predicted_score_a: Mapped[int] = mapped_column(Integer)
    predicted_score_b: Mapped[int] = mapped_column(Integer)
    confidence_label: Mapped[str] = mapped_column(String(40))
    explanation_json: Mapped[list[str]] = mapped_column(json_type)
    scoreline_probs_json: Mapped[list[dict[str, Any]]] = mapped_column(json_type)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    match = relationship("Match", back_populates="predictions")

