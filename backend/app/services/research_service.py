"""Research service — orchestrates the async research pipeline.

Flow:
    POST /research → create ResearchRun → set status=queued → dispatch to n8n → return immediately
    n8n/OpenClaw does the work → callbacks update progress/results → status=completed
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.redis import cache_set
from app.models.product import Product
from app.models.research import ResearchRun
from app.services.n8n_service import trigger_research_webhook

logger = logging.getLogger(__name__)


def create_research_run(db: Session, product_id: int) -> ResearchRun:
    """Create a new research run in 'pending' state."""
    run = ResearchRun(
        product_id=product_id,
        status="pending",
        progress=0,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    logger.info("Created research run id=%d for product_id=%d", run.id, product_id)
    return run


async def start_research(db: Session, research_run: ResearchRun, product: Product) -> dict:
    """Transition research run to 'queued' and dispatch to n8n.

    Returns immediately — the actual research happens asynchronously.
    """
    # Transition to queued
    research_run.status = "queued"
    research_run.started_at = datetime.now(timezone.utc)
    db.commit()

    # Cache the job state in Redis
    cache_set(
        f"research:{research_run.id}:status",
        "queued",
        ttl=3600,
    )

    # Build callback URL
    callback_url = f"{_get_base_url()}/api/research/{research_run.id}/callback"

    # Dispatch to n8n
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "target_users": product.target_users,
        "problem": product.problem,
    }

    result = await trigger_research_webhook(
        research_run_id=research_run.id,
        product_data=product_data,
        callback_url=callback_url,
    )

    # If n8n accepted, update execution ID
    if result.get("success"):
        n8n_response = result.get("n8n_response", {})
        if isinstance(n8n_response, dict):
            research_run.n8n_execution_id = n8n_response.get("executionId")
    else:
        # n8n was unreachable — run stays in queued, will be retried or processed manually
        logger.warning(
            "n8n dispatch failed for research_run_id=%d: %s",
            research_run.id,
            result.get("error"),
        )

    db.commit()

    return {
        "research_run_id": research_run.id,
        "status": research_run.status,
        "n8n_dispatch": result,
    }


def _get_base_url() -> str:
    """Determine the base URL for callback construction."""
    if settings.ENVIRONMENT == "production":
        # In production, this should come from a proper config
        return "https://api.launchlens.com"
    return "http://localhost:8000"
