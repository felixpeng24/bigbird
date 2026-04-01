"""Tests for scores.py — procedural Leadership Index score generation."""

import pytest

from scores import generate_score, reset_last_score, _generate_normal, _generate_irrational, _generate_wild


@pytest.fixture(autouse=True)
def _reset():
    """Reset last-score tracker between tests."""
    reset_last_score()
    yield
    reset_last_score()


class TestGenerateScore:
    """generate_score produces valid, non-repeating scores."""

    def test_returns_string(self):
        score = generate_score()
        assert isinstance(score, str)
        assert len(score) > 0

    def test_no_consecutive_duplicates(self):
        """Generate 100 scores — none should repeat consecutively."""
        scores = [generate_score() for _ in range(100)]
        for i in range(1, len(scores)):
            assert scores[i] != scores[i - 1], f"Consecutive duplicate at index {i}: {scores[i]}"

    def test_variety(self):
        """100 scores should have reasonable variety (at least 50 unique)."""
        scores = {generate_score() for _ in range(100)}
        assert len(scores) >= 50, f"Only {len(scores)} unique scores in 100 generations"

    def test_distribution_rough(self):
        """Check that all three generators produce non-empty strings."""
        for _ in range(20):
            assert len(_generate_normal()) > 0
            assert len(_generate_irrational()) > 0
            assert len(_generate_wild()) > 0


class TestGenerateNormal:
    """_generate_normal produces number-like strings."""

    def test_returns_string(self):
        for _ in range(20):
            s = _generate_normal()
            assert isinstance(s, str)
            assert len(s) > 0


class TestGenerateIrrational:
    """_generate_irrational produces expressions with math constants."""

    def test_contains_math_symbols(self):
        math_chars = set("πeφ√")
        found_any = False
        for _ in range(30):
            s = _generate_irrational()
            if any(c in s for c in math_chars):
                found_any = True
        assert found_any, "Expected at least one irrational score to contain π, e, φ, or √"


class TestGenerateWild:
    """_generate_wild produces exotic mathematical expressions."""

    def test_returns_string(self):
        for _ in range(30):
            s = _generate_wild()
            assert isinstance(s, str)
            assert len(s) > 0

    def test_variety_of_wild(self):
        """Wild scores should not all be identical."""
        scores = {_generate_wild() for _ in range(30)}
        assert len(scores) >= 5
