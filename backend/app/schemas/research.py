"""Research schemas for request validation and response serialization."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Request schemas ──────────────────────────────────────────────────────
class ResearchCreate(BaseModel):
    product_id: int


class ResearchProgressUpdate(BaseModel):
    """Partial progress update sent by n8n during a running research job."""
    progress: Optional[int] = Field(None, ge=0, le=100)
    sources_analyzed: Optional[int] = None
    results_found: Optional[int] = None
    relevant_results: Optional[int] = None
    leads_found: Optional[int] = None
    segments_found: Optional[int] = None


class LeadPayload(BaseModel):
    """A lead inside a callback payload."""
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
    evidence: list[EvidencePayload] = Field(default_factory=list)


class EvidencePayload(BaseModel):
    """An evidence item inside a lead payload."""
    content: str
    source_url: Optional[str] = None
    signal_type: Optional[str] = None
    strength: Optional[float] = Field(None, ge=0.0, le=1.0)


class SegmentPayload(BaseModel):
    """A segment inside a callback payload."""
    name: str
    description: Optional[str] = None
    estimated_size: Optional[int] = None
    priority_level: Optional[str] = None
    market_language: Optional[str] = None


class ReportPayload(BaseModel):
    """Research report inside a callback payload."""
    summary: Optional[str] = None
    top_customer_segments: Optional[list[Any]] = None
    top_pain_points: Optional[list[Any]] = None
    market_language: Optional[list[Any]] = None
    recommended_next_steps: Optional[list[Any]] = None


class ResearchCallbackPayload(BaseModel):
    """Full callback payload sent by n8n/OpenClaw when research completes or updates.

    Includes `event_id` for idempotency.
    """
    research_run_id: int
    event_id: str = Field(..., description="Unique event ID for idempotency")
    status: str = Field(..., description="queued | running | completed | failed")
    progress: Optional[int] = Field(None, ge=0, le=100)

    # Statistics
    sources_analyzed: Optional[int] = None
    results_found: Optional[int] = None
    relevant_results: Optional[int] = None

    # Results (typically sent with status=completed)
    leads: list[LeadPayload] = Field(default_factory=list)
    segments: list[SegmentPayload] = Field(default_factory=list)
    report: Optional[ReportPayload] = None

    error_message: Optional[str] = None


# ── Response schemas ─────────────────────────────────────────────────────
class ResearchRunResponse(BaseModel):
    id: int
    product_id: int
    status: str
    progress: int
    sources_analyzed: int
    results_found: int
    relevant_results: int
    leads_found: int
    segments_found: int
    n8n_execution_id: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ResearchRunDetailResponse(ResearchRunResponse):
    """Extended response including nested leads, segments, and report."""
    pass


# Update forward references for nested models
LeadPayload.model_rebuild()
