"""OpenClaw router — API endpoints for managing and triggering OpenClaw discovery agents."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.models.research import ResearchRun
from app.services.openclaw_service import (
    execute_openclaw_research,
    get_openclaw_status,
    run_discovery_agent,
)
from app.services.research_service import create_research_run

router = APIRouter(prefix="/openclaw", tags=["OpenClaw Agent"])


class OpenClawRunRequest(BaseModel):
    product_id: Optional[int] = None
    research_run_id: Optional[int] = None


class OpenClawDiscoverRequest(BaseModel):
    product: Optional[dict] = None
    product_id: Optional[int] = None


@router.get("/status")
def get_status():
    """Get status of the local OpenClaw installation, version, and readiness."""
    return get_openclaw_status()


@router.post("/discover")
async def discover_prospects(
    payload: OpenClawDiscoverRequest,
    db: Session = Depends(get_db),
):
    """Execute OpenClaw reasoning and prospect discovery without writing to database.

    Used directly by n8n orchestrator to retrieve discovered leads, evidence, segments,
    and market reports before orchestrating callbacks.
    """
    product_data = payload.product
    if not product_data and payload.product_id:
        product = db.query(Product).filter(Product.id == payload.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "target_users": product.target_users,
            "problem": product.problem,
        }

    if not product_data:
        raise HTTPException(status_code=400, detail="Must provide product object or product_id")

    discovery = await run_discovery_agent(product_data)
    return {
        "success": True,
        "product": product_data,
        "discovery": discovery,
    }


@router.post("/run")
async def run_openclaw(
    payload: OpenClawRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Trigger an autonomous OpenClaw customer discovery run.

    Accepts either `product_id` (creates a new research run) or `research_run_id` (runs against existing).
    Executes discovery and automatically processes results through the LaunchLens pipeline.
    """
    if not payload.product_id and not payload.research_run_id:
        raise HTTPException(status_code=400, detail="Must provide either product_id or research_run_id")

    if payload.research_run_id:
        run = db.query(ResearchRun).filter(ResearchRun.id == payload.research_run_id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Research run not found")
        product = db.query(Product).filter(Product.id == run.product_id).first()
    else:
        product = db.query(Product).filter(Product.id == payload.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        run = create_research_run(db, product_id=product.id)

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "target_users": product.target_users,
        "problem": product.problem,
    }

    # Execute OpenClaw research
    result = await execute_openclaw_research(
        research_run_id=run.id,
        product_data=product_data,
        db=db,
    )

    return {
        "message": "OpenClaw research completed and ingested",
        "research_run_id": run.id,
        "product_id": product.id,
        "result": result,
    }

