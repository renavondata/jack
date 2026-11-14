"""BRIEF-C2b's represented gains and four interleaved EXP3 instances.

The hash draw assumes the specified honest deterministic signer; its frequencies
are a diagnostic, never a proof against a key custodian grinding signatures.
"""
from fractions import Fraction
import hashlib
import math

ROSTER = (("reviewer", "openai/gpt-5.4-mini"), ("builder", "openai/gpt-5.4-mini"),
          ("reviewer", "openai/gpt-6-astra-fast"))
K, HORIZON, D = len(ROSTER), 84, 3
GRID = 2 ** 256
GAMMA = min(1, math.sqrt(K * math.log(K) / ((math.e - 1) * HORIZON)))
ETA = GAMMA / K


def gain(ns):
    """Six outcome probabilities; callers impute a missing event as n=1."""
    if len(ns) != 6 or any(type(n) is not int or not 1 <= n <= 999 for n in ns):
        raise ValueError("a round needs six per-mille outcome probabilities")
    return Fraction(math.fsum(math.log(n) for n in ns) / 6 / math.log(999))


def cuts(gains):
    if len(gains) != K or any(not isinstance(g, Fraction) or g < 0 for g in gains):
        raise ValueError("three exact cumulative gains required")
    weights = [math.exp(ETA * g) for g in gains]
    probabilities = [(1 - GAMMA) * w / sum(weights) + GAMMA / K for w in weights]
    return (0, *(math.floor(sum(probabilities[:k]) * GRID) for k in range(1, K)), GRID)


def select(boundaries, u):
    """Integer intervals cover every grid point, including the maximal hash."""
    if (len(boundaries) != K + 1 or boundaries[0] != 0 or boundaries[-1] != GRID or
            any(type(c) is not int for c in boundaries) or
            any(a >= b for a, b in zip(boundaries, boundaries[1:])) or type(u) is not int or not 0 <= u < GRID):
        raise ValueError("invalid draw grid")
    arm = next(k for k in range(K) if boundaries[k] <= u < boundaries[k + 1])
    return arm, Fraction(boundaries[arm + 1] - boundaries[arm], GRID)


def draw(gains, sigma):
    if not isinstance(sigma, bytes) or len(sigma) != 64:
        raise ValueError("sigma must be the 64 raw Ed25519 signature bytes")
    boundaries = cuts(gains)
    u = int.from_bytes(hashlib.sha256(sigma).digest(), "big")
    arm, propensity = select(boundaries, u)
    return dict(arm=arm, propensity=propensity, cuts=boundaries, u=u)


def update(gains, arm, represented_gain, saved_propensity):
    if (len(gains) != K or type(arm) is not int or not 0 <= arm < K or
            not isinstance(represented_gain, Fraction) or not 0 <= represented_gain <= 1 or
            not isinstance(saved_propensity, Fraction) or not 0 < saved_propensity <= 1):
        raise ValueError("invalid EXP3 feedback")
    return tuple(g + represented_gain / saved_propensity if k == arm else g for k, g in enumerate(gains))


def success_rate(outcomes):
    """Only settled rounds are supplied; deadline-imputed rounds supply a zero."""
    if any(type(y) is not int or y not in (0, 1) for y in outcomes):
        raise ValueError("settled binary successes required")
    q = 1000 * Fraction(sum(outcomes) + 1, len(outcomes) + 2)
    return max(1, min(999, (2 * q.numerator + q.denominator) // (2 * q.denominator)))
