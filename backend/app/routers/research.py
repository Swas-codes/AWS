"""Research router — async research runs, status polling, callback ingestion.

Key flows:
    POST /         → create & dispatch research run (returns immediately)
    GET  /         → list all research runs
    GET  /{id}     → poll status + progress
    POST /{id}/callback → secured + idempotent n8n/OpenClaw result ingestion
    GET  /{id}/leads    → leads for a specific run
    GET  /{id}/segments → segments for a specific run
    GET  /{id}/report   → research report for a specific run
"""

from __future__ import annotations

import json
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.lead import Lead
from app.models.product import Product
from app.models.research import ResearchRun
from app.models.segment import Segment
from app.schemas.lead import LeadResponse
from app.schemas.report import ResearchReportResponse
from app.schemas.research import ResearchCallbackPayload, ResearchCreate, ResearchRunResponse
from app.schemas.segment import SegmentResponse
from app.services.callback_service import process_callback, validate_callback_secret
from app.services.research_service import create_research_run, start_research

router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/", response_model=ResearchRunResponse, status_code=201)
async def trigger_research(payload: ResearchCreate, db: Session = Depends(get_db)):
    """Trigger a new research run for a product.

    Creates the run, sets status to 'queued', dispatches to n8n,
    and returns immediately. Frontend polls GET /{id} for progress.
    """
    # Verify product exists
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Create and dispatch
    run = create_research_run(db, payload.product_id)
    await start_research(db, run, product)

    db.refresh(run)
    return run


@router.get("/", response_model=list[ResearchRunResponse])
def list_research_runs(
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List research runs with optional filters."""
    query = db.query(ResearchRun)

    if product_id is not None:
        query = query.filter(ResearchRun.product_id == product_id)
    if status is not None:
        query = query.filter(ResearchRun.status == status)

    return query.order_by(ResearchRun.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{run_id}", response_model=ResearchRunResponse)
def get_research_run(run_id: int, db: Session = Depends(get_db)):
    """Get a research run with current progress — designed for polling."""
    run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Research run not found")
    return run


@router.post("/{run_id}/callback")
def research_callback(
    run_id: int,
    payload: ResearchCallbackPayload,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Receive research results from n8n/OpenClaw.

    Secured with bearer token and idempotent via event_id.
    """
    # Authenticate
    validate_callback_secret(authorization)

    # Validate run_id matches payload
    if payload.research_run_id != run_id:
        raise HTTPException(
            status_code=400,
            detail=f"URL run_id ({run_id}) does not match payload research_run_id ({payload.research_run_id})",
        )

    # Process the callback
    result = process_callback(db, payload)
    return result


@router.get("/{run_id}/leads", response_model=list[LeadResponse])
def get_research_leads(
    run_id: int,
    min_score: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum overall score"),
    db: Session = Depends(get_db),
):
    """Get all leads for a research run, optionally filtered by minimum score."""
    # Verify run exists
    run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Research run not found")

    query = db.query(Lead).filter(Lead.research_run_id == run_id)

    if min_score is not None:
        query = query.filter(Lead.overall_score >= min_score)

    return query.order_by(Lead.overall_score.desc()).all()


@router.get("/{run_id}/segments", response_model=list[SegmentResponse])
def get_research_segments(run_id: int, db: Session = Depends(get_db)):
    """Get all segments for a research run."""
    run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Research run not found")

    return db.query(Segment).filter(Segment.research_run_id == run_id).all()


@router.get("/{run_id}/report", response_model=ResearchReportResponse)
def get_research_report(run_id: int, db: Session = Depends(get_db)):
    """Get the research report for a completed run."""
    run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Research run not found")

    if run.report is None:
        raise HTTPException(status_code=404, detail="Report not available yet")

    # Deserialize JSON text fields for the response
    report = run.report
    response_data = {
        "id": report.id,
        "research_run_id": report.research_run_id,
        "summary": report.summary,
        "top_customer_segments": _parse_json(report.top_customer_segments),
        "top_pain_points": _parse_json(report.top_pain_points),
        "market_language": _parse_json(report.market_language),
        "recommended_next_steps": _parse_json(report.recommended_next_steps),
        "created_at": report.created_at,
    }
    return response_data


def _parse_json(value: str | None):
    """Safely parse a JSON string, returning None on failure."""
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value
