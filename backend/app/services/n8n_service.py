"""n8n webhook dispatch service.

Sends research jobs to n8n for orchestration. n8n then coordinates with
OpenClaw for the actual research, reasoning, and signal extraction.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def trigger_research_webhook(
    research_run_id: int,
    product_data: dict[str, Any],
    callback_url: str,
) -> dict[str, Any]:
    """Dispatch a research job to n8n via webhook.

    Args:
        research_run_id: The ID of the research run to process.
        product_data: Product details (name, description, target_users, problem).
        callback_url: The URL n8n should POST results back to.

    Returns:
        Response from n8n, or a mock response if n8n is unavailable.
    """
    payload = {
        "research_run_id": research_run_id,
        "product": product_data,
        "callback_url": callback_url,
        "callback_secret": settings.N8N_CALLBACK_SECRET,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                settings.N8N_WEBHOOK_URL,
                json=payload,
            )
            response.raise_for_status()

            result = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"status": "accepted"}
            logger.info(
                "n8n webhook triggered for research_run_id=%d: %s",
                research_run_id,
                result,
            )
            return {"success": True, "n8n_response": result}

    except httpx.ConnectError:
        logger.warning(
            "n8n unreachable at %s — research_run_id=%d will remain queued",
            settings.N8N_WEBHOOK_URL,
            research_run_id,
        )
        return {"success": False, "error": "n8n_unreachable", "mock": True}

    except httpx.HTTPStatusError as exc:
        logger.error(
            "n8n returned %d for research_run_id=%d: %s",
            exc.response.status_code,
            research_run_id,
            exc.response.text,
        )
        return {"success": False, "error": f"n8n_http_{exc.response.status_code}"}

    except Exception as exc:
        logger.error(
            "Unexpected error triggering n8n for research_run_id=%d: %s",
            research_run_id,
            exc,
        )
        return {"success": False, "error": str(exc)}
