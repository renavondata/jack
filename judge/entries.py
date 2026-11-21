"""Shared log folds and the verbs' clock, used by the trusted evaluator."""
import datetime
import fractions

from kernel import check


def read_log(path):
    with open(path, "rb") as f:
        return check.read_lines(f.read())


def now():
    """The verb's clock, UTC, in SPEC §4's form; the kernel never reads one."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolution_rates(es):
    """C1's prequential Laplace base: every resolution, pooled by type, in seq order."""
    forecasts, seen = {}, {}
    for e in sorted(es, key=lambda e: e["seq"]):
        if e["type"] == "forecast":
            forecasts[e["seq"]] = e
        if e["type"] == "resolution":
            f = forecasts[e["body"]["forecast"]]
            typ = f["body"].get("type", "free")
            s, n = seen.get(typ, (0, 0))
            yield e, f, fractions.Fraction(s + 1, n + 2), (s, n)
            seen[typ] = (s + e["body"]["outcome"], n + 1)
