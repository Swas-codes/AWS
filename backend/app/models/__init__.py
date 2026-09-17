"""LaunchLens Backend — Models package.

Import all models here so that SQLAlchemy / Alembic can discover them
from a single import of `app.models`.
"""

from app.models.evidence import Evidence
from app.models.lead import Lead
from app.models.product import Product
from app.models.report import ResearchReport
from app.models.research import ResearchRun
from app.models.segment import Segment

__all__ = [
    "Evidence",
    "Lead",
    "Product",
    "ResearchReport",
    "ResearchRun",
    "Segment",
]
