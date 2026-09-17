"""LaunchLens Backend — Redis Connection Manager."""

from __future__ import annotations

import logging
from typing import Optional

import redis as redis_lib

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Redis client (lazy, singleton) ───────────────────────────────────────
_redis_client: Optional[redis_lib.Redis] = None


def get_redis() -> Optional[redis_lib.Redis]:
    """Return a Redis client, or None if Redis is unavailable.

    Graceful degradation: logs a warning instead of crashing when Redis
    is not running (common during local development).
    """
    global _redis_client  # noqa: PLW0603

    if _redis_client is not None:
        return _redis_client

    try:
        client = redis_lib.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=2,
        )
        client.ping()
        _redis_client = client
        logger.info("Redis connected at %s", settings.REDIS_URL)
        return _redis_client
    except (redis_lib.ConnectionError, redis_lib.TimeoutError, OSError) as exc:
        logger.warning("Redis unavailable (%s) — running without cache", exc)
        return None


def redis_health() -> dict:
    """Check Redis connectivity for the health endpoint."""
    client = get_redis()
    if client is None:
        return {"status": "unavailable"}
    try:
        client.ping()
        return {"status": "connected"}
    except Exception:
        return {"status": "error"}


# ── Cache helpers ────────────────────────────────────────────────────────
def cache_set(key: str, value: str, ttl: int = 300) -> bool:
    """Set a cache key with TTL (seconds). Returns False if Redis is unavailable."""
    client = get_redis()
    if client is None:
        return False
    try:
        client.setex(key, ttl, value)
        return True
    except Exception:
        return False


def cache_get(key: str) -> Optional[str]:
    """Get a cache value. Returns None if Redis is unavailable or key missing."""
    client = get_redis()
    if client is None:
        return None
    try:
        return client.get(key)
    except Exception:
        return None


def cache_delete(key: str) -> bool:
    """Delete a cache key. Returns False if Redis is unavailable."""
    client = get_redis()
    if client is None:
        return False
    try:
        client.delete(key)
        return True
    except Exception:
        return False
