"""Evidence model — raw evidence supporting a lead."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False, index=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    signal_type: Mapped[str | None] = mapped_column(String(100), nullable=True)  # e.g. "pain", "intent", "frustration"
    strength: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0.0–1.0

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    lead = relationship("Lead", back_populates="evidence")
