"""Segments router — query and manage customer segments."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.research import ResearchRun
from app.models.segment import Segment
from app.schemas.segment import SegmentCreate, SegmentResponse

router = APIRouter(prefix="/segments", tags=["Segments"])


@router.get("/", response_model=list[SegmentResponse])
def list_segments(
    research_run_id: Optional[int] = Query(None, description="Filter by research run ID"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List segments with optional filter by research run."""
    query = db.query(Segment)

    if research_run_id is not None:
        query = query.filter(Segment.research_run_id == research_run_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{segment_id}", response_model=SegmentResponse)
def get_segment(segment_id: int, db: Session = Depends(get_db)):
    """Get a single segment by ID."""
    segment = db.query(Segment).filter(Segment.id == segment_id).first()
    if segment is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment


@router.post("/", response_model=SegmentResponse, status_code=201)
def create_segment(payload: SegmentCreate, db: Session = Depends(get_db)):
    """Manually create a segment."""
    # Verify research run exists
    run = db.query(ResearchRun).filter(ResearchRun.id == payload.research_run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Research run not found")

    segment = Segment(**payload.model_dump())
    db.add(segment)
    db.commit()
    db.refresh(segment)
    return segment
