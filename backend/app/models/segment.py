"""Segment model — a customer segment discovered during research."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Segment(Base):
    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    research_run_id: Mapped[int] = mapped_column(
        ForeignKey("research_runs.id"), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    priority_level: Mapped[str | None] = mapped_column(String(20), nullable=True)  # e.g. "high", "medium", "low"
    market_language: Mapped[str | None] = mapped_column(Text, nullable=True)  # words/phrases this segment uses

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    research_run = relationship("ResearchRun", back_populates="segments")
