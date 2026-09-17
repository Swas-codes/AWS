"""ResearchRun model — tracks an asynchronous research job with progress."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ResearchRun(Base):
    __tablename__ = "research_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)

    # Status: pending → queued → running → completed | failed
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)

    # Progress tracking (updated via callbacks from n8n/OpenClaw)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0–100
    sources_analyzed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    results_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    relevant_results: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leads_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    segments_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # n8n integration
    n8n_execution_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product = relationship("Product", back_populates="research_runs")
    leads = relationship("Lead", back_populates="research_run", cascade="all, delete-orphan")
    segments = relationship("Segment", back_populates="research_run", cascade="all, delete-orphan")
    report = relationship(
        "ResearchReport", back_populates="research_run", uselist=False, cascade="all, delete-orphan"
    )
