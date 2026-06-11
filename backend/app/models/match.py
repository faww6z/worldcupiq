from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("status in ('scheduled', 'live', 'finished', 'postponed')", name="ck_matches_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    match_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    time_utc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    stage: Mapped[str] = mapped_column(String(40))
    group_code: Mapped[str | None] = mapped_column(String(8), ForeignKey("groups.code"), nullable=True, index=True)
    team_a_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team_b_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    venue: Mapped[str | None] = mapped_column(String(160), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(20), index=True)
    score_a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score_b: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    group = relationship("Group", back_populates="matches")
    team_a = relationship("Team", foreign_keys=[team_a_id], back_populates="home_matches")
    team_b = relationship("Team", foreign_keys=[team_b_id], back_populates="away_matches")
    predictions = relationship("Prediction", back_populates="match")

