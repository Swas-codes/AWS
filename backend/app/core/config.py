"""LaunchLens Backend — Core Configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file.

    DATABASE_URL is **required** — the app will not start without it.
    No silent fallback to SQLite; the developer must choose explicitly.
    """

    # ── Database (required) ──────────────────────────────────────────────
    DATABASE_URL: str

    # ── Redis (optional — graceful degradation) ──────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── n8n Integration ──────────────────────────────────────────────────
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook/launchlens-research"
    N8N_CALLBACK_SECRET: str = "change-me-to-a-strong-secret"

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # ── Environment ──────────────────────────────────────────────────────
    ENVIRONMENT: str = "development"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_sqlite(self) -> bool:
        """Check if the configured database is SQLite."""
        return self.DATABASE_URL.startswith("sqlite")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
