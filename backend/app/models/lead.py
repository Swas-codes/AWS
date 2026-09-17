"""Lead model — a potential customer discovered during research."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    research_run_id: Mapped[int] = mapped_column(
        ForeignKey("research_runs.id"), nullable=False, index=True
    )

    # Discovery info
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)  # e.g. "reddit", "github"
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Classification
    customer_segment: Mapped[str | None] = mapped_column(String(255), nullable=True)
    problem_detected: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Scoring signals (floats 0.0–1.0, extracted by OpenClaw, scored by FastAPI)
    pain_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    intent_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    problem_fit: Mapped[float | None] = mapped_column(Float, nullable=True)
    persona_fit: Mapped[float | None] = mapped_column(Float, nullable=True)
    evidence_strength: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Deterministic overall score computed by FastAPI scoring service
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Actionable output
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    outreach_angle: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    research_run = relationship("ResearchRun", back_populates="leads")
    evidence = relationship("Evidence", back_populates="lead", cascade="all, delete-orphan")
