"""Lead and Evidence schemas for request validation and response serialization."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Evidence schemas ─────────────────────────────────────────────────────
class EvidenceCreate(BaseModel):
    content: str = Field(..., min_length=1)
    source_url: Optional[str] = None
    signal_type: Optional[str] = None
    strength: Optional[float] = Field(None, ge=0.0, le=1.0)


class EvidenceResponse(BaseModel):
    id: int
    lead_id: int
    content: str
    source_url: Optional[str] = None
    signal_type: Optional[str] = None
    strength: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Lead schemas ─────────────────────────────────────────────────────────
class LeadCreate(BaseModel):
    research_run_id: int
    source: Optional[str] = None
    source_url: Optional[str] = None
    author: Optional[str] = None
    customer_segment: Optional[str] = None
    problem_detected: Optional[str] = None
    pain_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    intent_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    problem_fit: Optional[float] = Field(None, ge=0.0, le=1.0)
    persona_fit: Optional[float] = Field(None, ge=0.0, le=1.0)
    evidence_strength: Optional[float] = Field(None, ge=0.0, le=1.0)
    reason: Optional[str] = None
    outreach_angle: Optional[str] = None


class LeadResponse(BaseModel):
    id: int
    research_run_id: int
    source: Optional[str] = None
    source_url: Optional[str] = None
    author: Optional[str] = None
    customer_segment: Optional[str] = None
    problem_detected: Optional[str] = None
    pain_level: Optional[float] = None
    intent_level: Optional[float] = None
    problem_fit: Optional[float] = None
    persona_fit: Optional[float] = None
    evidence_strength: Optional[float] = None
    overall_score: Optional[float] = None
    reason: Optional[str] = None
    outreach_angle: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadDetailResponse(LeadResponse):
    """Lead response including nested evidence."""
    evidence: list[EvidenceResponse] = []
