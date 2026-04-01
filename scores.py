"""Procedural score generation for Big Bird's Leadership Index.

Distribution per D009:
  50% normal real numbers (random decimals/integers)
  25% irrational compositions (π, e, √n, φ, ln(n), etc.)
  25% wild/nonsensical expressions (imaginary vectors, trig combos, set theory)

Every score is procedurally constructed — no fixed pool, no two structurally
identical. No consecutive duplicates.
"""

import logging
import math
import random

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Last-score tracking (R014: no consecutive duplicates)
# ---------------------------------------------------------------------------
_last_score: str | None = None


def _generate_normal() -> str:
    """Generate a normal-ish real number score."""
    kind = random.choice(["decimal", "integer", "negative_decimal", "fraction_like"])
    if kind == "decimal":
        return f"{random.uniform(0.01, 999.99):.{random.randint(1, 6)}f}"
    elif kind == "integer":
        return str(random.randint(-500, 5000))
    elif kind == "negative_decimal":
        return f"-{random.uniform(0.01, 99.99):.{random.randint(2, 5)}f}"
    else:
        a, b = random.randint(1, 99), random.randint(2, 99)
        return f"{a}/{b}"


def _generate_irrational() -> str:
    """Generate a composition of irrational constants."""
    constants = ["π", "e", "φ", "√2", "√3", "√5", "√7"]
    ops = [" + ", " - ", " × ", " / ", "·"]
    functions = ["ln", "log₂", "√"]

    kind = random.choice(["product", "sum", "function", "power", "nested"])
    if kind == "product":
        c1, c2 = random.sample(constants, 2)
        n = random.randint(2, 13)
        return f"{n}{random.choice(ops).strip()}{c1}"
    elif kind == "sum":
        c1, c2 = random.sample(constants, 2)
        op = random.choice([" + ", " - "])
        return f"{c1}{op}{c2}"
    elif kind == "function":
        fn = random.choice(functions)
        c = random.choice(constants)
        n = random.randint(2, 20)
        return f"{fn}({n}{random.choice(ops).strip()}{c})"
    elif kind == "power":
        c = random.choice(constants)
        n = random.randint(2, 7)
        return f"{c}^{n}"
    else:
        c1, c2 = random.sample(constants, 2)
        return f"√({c1}·{c2})"


def _generate_wild() -> str:
    """Generate a wild/nonsensical mathematical expression."""
    kind = random.choice([
        "imaginary", "trig", "undefined", "set_theory",
        "vector", "integral", "matrix_det", "limit",
    ])
    if kind == "imaginary":
        a = random.randint(1, 50)
        b = random.randint(1, 99)
        return f"{a} + {b}i"
    elif kind == "trig":
        fns = ["sin", "cos", "tan", "arctan"]
        f1, f2 = random.sample(fns, 2)
        a, b = random.randint(1, 12), random.randint(1, 12)
        return f"{f1}({a}) + i·{f2}({b})"
    elif kind == "undefined":
        options = [
            f"{random.randint(1, 99)}/0",
            f"∞ - ∞",
            f"0^0 × {random.randint(2, 50)}",
            f"lim(n→∞) (-1)^n × {random.randint(2, 20)}",
        ]
        return random.choice(options)
    elif kind == "set_theory":
        options = [
            f"ℵ₀ + {random.randint(1, 99)}",
            f"ℵ₁ / ℵ₀",
            f"|ℝ| × {random.choice(['π', 'e', 'φ'])}",
            f"ω^ω + {random.randint(1, 50)}",
        ]
        return random.choice(options)
    elif kind == "vector":
        dims = random.randint(2, 4)
        components = [str(random.randint(-20, 20)) for _ in range(dims)]
        return f"⟨{', '.join(components)}⟩"
    elif kind == "integral":
        a, b = sorted(random.sample(range(-10, 10), 2))
        var = random.choice(["x", "θ", "λ"])
        return f"∫[{a},{b}] {var}² d{var}"
    elif kind == "matrix_det":
        vals = [str(random.randint(-9, 9)) for _ in range(4)]
        return f"det|{vals[0]} {vals[1]}; {vals[2]} {vals[3]}|"
    else:  # limit
        c = random.choice(["π", "e", "∞", "0"])
        n = random.randint(2, 12)
        return f"lim(x→{c}) x^{n}/x!"


def generate_score() -> str:
    """Generate a procedural Leadership Index score.

    50% normal, 25% irrational, 25% wild. Never repeats consecutively.
    """
    global _last_score

    for _ in range(20):  # safety bound to prevent infinite loop
        roll = random.random()
        if roll < 0.50:
            score = _generate_normal()
        elif roll < 0.75:
            score = _generate_irrational()
        else:
            score = _generate_wild()

        if score != _last_score:
            _last_score = score
            logger.info("[SCORE] Generated: %s", score)
            return score

    # Extremely unlikely fallback
    score = f"UNDEFINED_{random.randint(1000, 9999)}"
    _last_score = score
    logger.warning("[SCORE] Fell through to fallback: %s", score)
    return score


def reset_last_score() -> None:
    """Reset the last-score tracker (useful for testing)."""
    global _last_score
    _last_score = None
