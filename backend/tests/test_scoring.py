"""Tests for the deterministic scoring service."""

from app.services.scoring import compute_overall_score


def test_all_signals_present():
    """Score with all signals should produce a weighted average."""
    score = compute_overall_score(
        problem_fit=0.91,
        intent_level=0.72,
        persona_fit=0.87,
        evidence_strength=0.84,
    )
    # 0.35*0.91 + 0.25*0.72 + 0.20*0.87 + 0.20*0.84
    # = 0.3185 + 0.18 + 0.174 + 0.168 = 0.8405
    assert abs(score - 0.8405) < 0.001


def test_all_zeros():
    """Score with all zeros should be 0.0."""
    score = compute_overall_score(
        problem_fit=0.0,
        intent_level=0.0,
        persona_fit=0.0,
        evidence_strength=0.0,
    )
    assert score == 0.0


def test_all_ones():
    """Score with all 1.0 should be 1.0."""
    score = compute_overall_score(
        problem_fit=1.0,
        intent_level=1.0,
        persona_fit=1.0,
        evidence_strength=1.0,
    )
    assert score == 1.0


def test_missing_signals():
    """Missing signals should be treated as 0.0."""
    score = compute_overall_score(problem_fit=1.0)
    # 0.35 * 1.0 + 0 + 0 + 0 = 0.35
    assert abs(score - 0.35) < 0.001


def test_all_none():
    """All None signals should produce 0.0."""
    score = compute_overall_score()
    assert score == 0.0


def test_clamping():
    """Values outside [0, 1] should be clamped."""
    score = compute_overall_score(
        problem_fit=1.5,  # clamped to 1.0
        intent_level=-0.3,  # clamped to 0.0
        persona_fit=0.5,
        evidence_strength=0.5,
    )
    # 0.35*1.0 + 0.25*0.0 + 0.20*0.5 + 0.20*0.5
    # = 0.35 + 0 + 0.10 + 0.10 = 0.55
    assert abs(score - 0.55) < 0.001


def test_scoring_is_deterministic():
    """Same inputs should always produce the same output."""
    kwargs = {
        "problem_fit": 0.82,
        "intent_level": 0.63,
        "persona_fit": 0.74,
        "evidence_strength": 0.91,
    }
    scores = [compute_overall_score(**kwargs) for _ in range(100)]
    assert len(set(scores)) == 1  # All identical
