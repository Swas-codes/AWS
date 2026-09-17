"""Leads router — query and manage discovered leads."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.evidence import Evidence
from app.models.lead import Lead
from app.models.research import ResearchRun
from app.schemas.lead import EvidenceCreate, EvidenceResponse, LeadCreate, LeadDetailResponse, LeadResponse
from app.services.scoring import compute_overall_score

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/", response_model=list[LeadResponse])
def list_leads(
    min_score: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum overall score"),
    segment: Optional[str] = Query(None, description="Filter by customer segment"),
    source: Optional[str] = Query(None, description="Filter by source (e.g. reddit, github)"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List leads with optional filters."""
    query = db.query(Lead)

    if min_score is not None:
        query = query.filter(Lead.overall_score >= min_score)
    if segment is not None:
        query = query.filter(Lead.customer_segment.ilike(f"%{segment}%"))
    if source is not None:
        query = query.filter(Lead.source == source)

    return query.order_by(Lead.overall_score.desc()).offset(skip).limit(limit).all()


@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a single lead with its evidence."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.post("/", response_model=LeadResponse, status_code=201)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    """Manually create a lead (useful for testing or manual entry)."""
    # Verify research run exists
    run = db.query(ResearchRun).filter(ResearchRun.id == payload.research_run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Research run not found")

    # Compute deterministic score
    overall_score = compute_overall_score(
        problem_fit=payload.problem_fit,
        intent_level=payload.intent_level,
        persona_fit=payload.persona_fit,
        evidence_strength=payload.evidence_strength,
    )

    lead = Lead(**payload.model_dump(), overall_score=overall_score)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.post("/{lead_id}/evidence", response_model=EvidenceResponse, status_code=201)
def add_evidence(lead_id: int, payload: EvidenceCreate, db: Session = Depends(get_db)):
    """Add evidence to an existing lead."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    evidence = Evidence(lead_id=lead_id, **payload.model_dump())
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence
