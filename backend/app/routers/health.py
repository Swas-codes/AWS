"""Health check router — verifies API, database, and Redis status."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.redis import redis_health

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Overall health check endpoint.

    Returns:
        status: "healthy" if all systems are operational
        database: connection status
        redis: connection status
    """
    # Database check
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"error: {exc}"

    # Redis check
    redis_status = redis_health()

    overall = "healthy" if db_status == "connected" else "degraded"

    return {
        "status": overall,
        "service": "LaunchLens Backend",
        "database": db_status,
        "redis": redis_status.get("status", "unknown"),
    }
