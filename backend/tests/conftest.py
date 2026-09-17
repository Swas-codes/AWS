"""Test fixtures for LaunchLens backend tests.

Uses SQLite in-memory database for fast, isolated tests.
"""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# Set test DATABASE_URL before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./test_launchlens.db"
os.environ["ENVIRONMENT"] = "test"
os.environ["N8N_CALLBACK_SECRET"] = "test-secret"

from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

# ── Test database ────────────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test_launchlens.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(test_engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override the get_db dependency for tests."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ── Fixtures ─────────────────────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once per test session."""
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Clean up test database file
    if os.path.exists("test_launchlens.db"):
        os.remove("test_launchlens.db")


@pytest.fixture(autouse=True)
def clean_tables():
    """Clean all tables between tests for isolation."""
    yield
    db = TestSessionLocal()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    finally:
        db.close()


@pytest.fixture
def client():
    """FastAPI TestClient."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Database session for direct DB access in tests."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
