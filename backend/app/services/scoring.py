"""Deterministic scoring service.

OpenClaw extracts raw signal values (0.0–1.0) for each dimension.
FastAPI computes the deterministic overall_score using fixed weights,
making the scoring explainable, reproducible, and auditable.
"""

from __future__ import annotations

# ── Weight configuration ─────────────────────────────────────────────────
SCORING_WEIGHTS = {
    "problem_fit": 0.35,
    "intent_level": 0.25,
    "persona_fit": 0.20,
    "evidence_strength": 0.20,
}


def compute_overall_score(
    problem_fit: float | None = None,
    intent_level: float | None = None,
    persona_fit: float | None = None,
    evidence_strength: float | None = None,
) -> float:
    """Compute a deterministic overall score (0.0–1.0) from signal dimensions.

    Missing dimensions are treated as 0.0 — the weights still sum to 1.0
    so that scores remain comparable even when some signals are absent.

    Formula:
        overall = 0.35 * problem_fit
                + 0.25 * intent_level
                + 0.20 * persona_fit
                + 0.20 * evidence_strength
    """
    pf = _clamp(problem_fit)
    il = _clamp(intent_level)
    pef = _clamp(persona_fit)
    es = _clamp(evidence_strength)

    score = (
        SCORING_WEIGHTS["problem_fit"] * pf
        + SCORING_WEIGHTS["intent_level"] * il
        + SCORING_WEIGHTS["persona_fit"] * pef
        + SCORING_WEIGHTS["evidence_strength"] * es
    )

    return round(score, 4)


def _clamp(value: float | None, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp a value to [min_val, max_val], treating None as 0.0."""
    if value is None:
        return 0.0
    return max(min_val, min(max_val, float(value)))
