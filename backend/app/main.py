"""LaunchLens Backend — FastAPI Application Entry Point.

Architecture:
    React Frontend → FastAPI Backend → PostgreSQL + Redis → n8n → OpenClaw
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import health, leads, openclaw, products, research, segments

# ── Logging ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup/shutdown) ──────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    On startup:
        - In development, auto-creates database tables (convenience).
          In production, use Alembic migrations instead.
    """
    # Import all models so metadata is populated
    import app.models  # noqa: F401

    if settings.ENVIRONMENT == "development":
        logger.info("Development mode — auto-creating database tables")
        Base.metadata.create_all(bind=engine)
    else:
        logger.info("Production mode — skipping auto-create (use Alembic)")

    logger.info("LaunchLens Backend started (env=%s)", settings.ENVIRONMENT)
    yield
    logger.info("LaunchLens Backend shutting down")


# ── FastAPI App ──────────────────────────────────────────────────────────
app = FastAPI(
    title="LaunchLens API",
    description=(
        "AI-powered pre-launch customer discovery backend. "
        "Manages products, research runs, leads, evidence, segments, and reports. "
        "Integrates with n8n for orchestration and OpenClaw for agentic research."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from pathlib import Path
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# ── Static Files & Frontend ─────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ── Register routers ────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(health.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(research.router, prefix="/api")
app.include_router(leads.router, prefix="/api")
app.include_router(segments.router, prefix="/api")
app.include_router(openclaw.router, prefix="/api")


# ── Dashboard & Root endpoints ──────────────────────────────────────────
@app.get("/dashboard", include_in_schema=False)
def dashboard():
    """Serve the LaunchLens web dashboard."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(index_file)
    return {"message": "Frontend not found"}


@app.get("/")
def root(request: Request):
    """API root — serves web dashboard for browsers and JSON info for API clients."""
    accept = request.headers.get("accept", "")
    index_file = FRONTEND_DIR / "index.html"
    if "text/html" in accept and index_file.is_file():
        return FileResponse(index_file)

    return {
        "service": "LaunchLens API",
        "version": "0.1.0",
        "docs": "/docs",
        "dashboard": "/dashboard",
        "health": "/health",
    }

