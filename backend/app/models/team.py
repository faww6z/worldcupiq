from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    group_code: Mapped[str | None] = mapped_column(String(8), ForeignKey("groups.code"), nullable=True, index=True)
    confederation: Mapped[str | None] = mapped_column(String(40), nullable=True)
    is_host: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    group = relationship("Group", back_populates="teams")
    home_matches = relationship("Match", foreign_keys="Match.team_a_id", back_populates="team_a")
    away_matches = relationship("Match", foreign_keys="Match.team_b_id", back_populates="team_b")

