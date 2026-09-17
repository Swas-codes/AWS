"""ResearchReport model — structured summary of a completed research run."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ResearchReport(Base):
    __tablename__ = "research_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    research_run_id: Mapped[int] = mapped_column(
        ForeignKey("research_runs.id"), unique=True, nullable=False, index=True
    )

    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # JSON-serialized lists stored as text (compatible with both PostgreSQL and SQLite)
    top_customer_segments: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    top_pain_points: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    market_language: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    recommended_next_steps: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    research_run = relationship("ResearchRun", back_populates="report")
