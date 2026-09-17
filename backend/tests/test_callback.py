"""Tests for the callback service — auth, idempotency, and ingestion.

These tests focus on the callback_service module directly,
complementing the integration tests in test_research.py.
"""

import pytest
from fastapi import HTTPException

from app.services.callback_service import validate_callback_secret


def test_validate_missing_header():
    """Missing authorization header should raise 401."""
    with pytest.raises(HTTPException) as exc_info:
        validate_callback_secret(None)
    assert exc_info.value.status_code == 401


def test_validate_invalid_format():
    """Non-Bearer format should raise 401."""
    with pytest.raises(HTTPException) as exc_info:
        validate_callback_secret("Basic abc123")
    assert exc_info.value.status_code == 401


def test_validate_wrong_secret():
    """Wrong secret should raise 401."""
    with pytest.raises(HTTPException) as exc_info:
        validate_callback_secret("Bearer wrong-secret-value")
    assert exc_info.value.status_code == 401


def test_validate_correct_secret():
    """Correct secret should pass without raising."""
    # N8N_CALLBACK_SECRET is set to 'test-secret' in conftest.py
    validate_callback_secret("Bearer test-secret")  # Should not raise


def test_validate_empty_bearer():
    """Bearer with no token should raise 401."""
    with pytest.raises(HTTPException) as exc_info:
        validate_callback_secret("Bearer ")
    assert exc_info.value.status_code == 401
