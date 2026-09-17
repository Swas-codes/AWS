"""Callback service — handles n8n/OpenClaw callback ingestion.

Key properties:
    - **Authenticated**: validates N8N_CALLBACK_SECRET bearer token
    - **Idempotent**: stores processed event_ids, rejects duplicates
    - **Batch**: ingests leads, segments, evidence, and report in one transaction
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.redis import cache_get, cache_set
from app.models.evidence import Evidence
from app.models.lead import Lead
from app.models.report import ResearchReport
from app.models.research import ResearchRun
from app.models.segment import Segment
from app.schemas.research import ResearchCallbackPayload
from app.services.scoring import compute_overall_score

logger = logging.getLogger(__name__)

# ── Processed event tracking (in-memory fallback when Redis is unavailable) ──
_processed_events: set[str] = set()


def validate_callback_secret(authorization: Optional[str]) -> None:
    """Validate the Bearer token against the configured callback secret.

    Raises HTTPException 401 if the token is missing or invalid.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    if parts[1] != settings.N8N_CALLBACK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid callback secret")


def is_event_processed(event_id: str) -> bool:
    """Check if an event_id has already been processed (idempotency)."""
    # Try Redis first
    cached = cache_get(f"callback:event:{event_id}")
    if cached is not None:
        return True

    # Fallback to in-memory set
    return event_id in _processed_events


def mark_event_processed(event_id: str) -> None:
    """Mark an event_id as processed."""
    cache_set(f"callback:event:{event_id}", "1", ttl=86400)  # 24h TTL
    _processed_events.add(event_id)


def process_callback(db: Session, payload: ResearchCallbackPayload) -> dict:
    """Process a callback payload from n8n/OpenClaw.

    Steps:
        1. Check idempotency (event_id already processed? → return 200)
        2. Load the research run
        3. Update progress/status
        4. Insert leads with computed scores + evidence
        5. Insert segments
        6. Insert report (if provided)
        7. Update run statistics
        8. Mark event as processed

    Returns a summary dict.
    """
    # 1. Idempotency check
    if is_event_processed(payload.event_id):
        logger.info("Duplicate callback event_id=%s — skipping", payload.event_id)
        return {"status": "duplicate", "event_id": payload.event_id}

    # 2. Load research run
    run = db.query(ResearchRun).filter(ResearchRun.id == payload.research_run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail=f"Research run {payload.research_run_id} not found")

    # 3. Update status and progress
    run.status = payload.status
    if payload.progress is not None:
        run.progress = payload.progress

    if payload.sources_analyzed is not None:
        run.sources_analyzed = payload.sources_analyzed
    if payload.results_found is not None:
        run.results_found = payload.results_found
    if payload.relevant_results is not None:
        run.relevant_results = payload.relevant_results

    if payload.error_message:
        run.error_message = payload.error_message

    if payload.status == "completed":
        run.completed_at = datetime.now(timezone.utc)
        run.progress = 100
    elif payload.status == "running" and run.started_at is None:
        run.started_at = datetime.now(timezone.utc)

    # 4. Insert leads with deterministic scoring
    leads_created = 0
    for lead_data in payload.leads:
        # Compute deterministic overall_score
        overall_score = compute_overall_score(
            problem_fit=lead_data.problem_fit,
            intent_level=lead_data.intent_level,
            persona_fit=lead_data.persona_fit,
            evidence_strength=lead_data.evidence_strength,
        )

        lead = Lead(
            research_run_id=run.id,
            source=lead_data.source,
            source_url=lead_data.source_url,
            author=lead_data.author,
            customer_segment=lead_data.customer_segment,
            problem_detected=lead_data.problem_detected,
            pain_level=lead_data.pain_level,
            intent_level=lead_data.intent_level,
            problem_fit=lead_data.problem_fit,
            persona_fit=lead_data.persona_fit,
            evidence_strength=lead_data.evidence_strength,
            overall_score=overall_score,
            reason=lead_data.reason,
            outreach_angle=lead_data.outreach_angle,
        )
        db.add(lead)
        db.flush()  # Get lead.id for evidence

        # Insert evidence for this lead
        for ev_data in lead_data.evidence:
            ev = Evidence(
                lead_id=lead.id,
                content=ev_data.content,
                source_url=ev_data.source_url,
                signal_type=ev_data.signal_type,
                strength=ev_data.strength,
            )
            db.add(ev)

        leads_created += 1

    # 5. Insert segments
    segments_created = 0
    for seg_data in payload.segments:
        seg = Segment(
            research_run_id=run.id,
            name=seg_data.name,
            description=seg_data.description,
            estimated_size=seg_data.estimated_size,
            priority_level=seg_data.priority_level,
            market_language=seg_data.market_language,
        )
        db.add(seg)
        segments_created += 1

    # 6. Insert report
    if payload.report:
        report = ResearchReport(
            research_run_id=run.id,
            summary=payload.report.summary,
            top_customer_segments=json.dumps(payload.report.top_customer_segments) if payload.report.top_customer_segments else None,
            top_pain_points=json.dumps(payload.report.top_pain_points) if payload.report.top_pain_points else None,
            market_language=json.dumps(payload.report.market_language) if payload.report.market_language else None,
            recommended_next_steps=json.dumps(payload.report.recommended_next_steps) if payload.report.recommended_next_steps else None,
        )
        db.add(report)

    # 7. Update run statistics
    run.leads_found = run.leads_found + leads_created
    run.segments_found = run.segments_found + segments_created

    db.commit()

    # 8. Mark event as processed
    mark_event_processed(payload.event_id)

    logger.info(
        "Processed callback event_id=%s for research_run_id=%d: %d leads, %d segments",
        payload.event_id,
        run.id,
        leads_created,
        segments_created,
    )

    return {
        "status": "processed",
        "event_id": payload.event_id,
        "research_run_id": run.id,
        "leads_created": leads_created,
        "segments_created": segments_created,
        "report_created": payload.report is not None,
    }
