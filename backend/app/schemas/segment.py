"""Segment schemas for request validation and response serialization."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SegmentCreate(BaseModel):
    research_run_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    estimated_size: Optional[int] = None
    priority_level: Optional[str] = None
    market_language: Optional[str] = None


class SegmentResponse(BaseModel):
    id: int
    research_run_id: int
    name: str
    description: Optional[str] = None
    estimated_size: Optional[int] = None
    priority_level: Optional[str] = None
    market_language: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
