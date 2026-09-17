"""ResearchReport schemas for request validation and response serialization."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ResearchReportCreate(BaseModel):
    research_run_id: int
    summary: Optional[str] = None
    top_customer_segments: Optional[list[Any]] = None
    top_pain_points: Optional[list[Any]] = None
    market_language: Optional[list[Any]] = None
    recommended_next_steps: Optional[list[Any]] = None


class ResearchReportResponse(BaseModel):
    id: int
    research_run_id: int
    summary: Optional[str] = None
    top_customer_segments: Optional[list[Any]] = None
    top_pain_points: Optional[list[Any]] = None
    market_language: Optional[list[Any]] = None
    recommended_next_steps: Optional[list[Any]] = None
    created_at: datetime

    model_config = {"from_attributes": True}
