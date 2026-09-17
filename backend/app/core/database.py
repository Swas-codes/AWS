"""LaunchLens Backend — Database Configuration."""

from __future__ import annotations

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# ── Engine setup ─────────────────────────────────────────────────────────
_connect_args: dict = {}
_engine_kwargs: dict = {}

if settings.is_sqlite:
    # SQLite needs check_same_thread=False for FastAPI's threaded access
    _connect_args = {"check_same_thread": False}
else:
    # PostgreSQL connection pooling
    _engine_kwargs = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
    }

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    **_engine_kwargs,
)

# Enable WAL mode and foreign keys for SQLite
if settings.is_sqlite:

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ── Declarative base ────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""


# ── Dependency ───────────────────────────────────────────────────────────
def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
