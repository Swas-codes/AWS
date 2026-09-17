"""Product schemas for request validation and response serialization."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Request schemas ──────────────────────────────────────────────────────
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_users: Optional[str] = None
    problem: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    target_users: Optional[str] = None
    problem: Optional[str] = None


# ── Response schemas ─────────────────────────────────────────────────────
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    target_users: Optional[str] = None
    problem: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
