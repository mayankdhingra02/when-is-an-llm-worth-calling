"""Evaluation-only functions; acquired labels never become controller inputs."""
from collections import Counter
from fractions import Fraction as F
import math

from .selection_reference_v42 import gain
from .selection_v8 import parse_ids


def unique_requests(records):
    result = {}
    for row in records:
        key = row["request_id"]
        if type(key) is not int or key in result:
            raise ValueError("Invalid/duplicate request ID")
        result[key] = row
    return result


def observed_total(records, field):
    values = [r.get(field) for r in records]
    if any(v is None for v in values):
        return None
    if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in values):
        raise ValueError("Invalid observed usage")
    return sum(values)


def selected_rows(response, prompt, arm):
    try:
        if response["status"] != "response":
            raise ValueError("Failed request")
        selected = parse_ids(response["raw_output"], prompt["pool"])
    except ValueError:
        if arm["fallback"] is None:
            raise ValueError("Failed/invalid response has no recorded fallback")
        return prompt["fallback_rows"]
    if arm["fallback"] is not None:
        raise ValueError("Unjustified fallback for valid model response")
    return selected


def contrast(reference, treatment, ceiling, direction):
    """Signed capture preserves harmful selection; zero opportunity is undefined."""
    if direction not in ("-", "+"):
        raise ValueError("Unknown target direction")
    if (treatment < ceiling if direction == "-" else treatment > ceiling):
        raise ValueError("Treatment exceeds measured pool ceiling")
    g = gain(reference, treatment, direction)
    h = gain(reference, ceiling, direction)
    return {"relative_gain": g, "ceiling_gain": h,
            "signed_capture": g / h if h > 0 else None,
            "positive_capture": max(F(0), g) / h if h > 0 else None,
            "attains_ceiling": treatment == ceiling}


def aggregate(rows, expected_groups, seeds_per_group=5):
    counts = Counter(r["system_group"] for r in rows)
    if set(counts) != set(expected_groups) or set(counts.values()) != {seeds_per_group}:
        raise ValueError("Incomplete family denominator")
    family = {g: sum(F(r["exact"]["relative_gain"]) for r in rows if r["system_group"] == g) / seeds_per_group
              for g in sorted(expected_groups)}
    effects = [F(r["exact"]["relative_gain"]) for r in rows]
    capture = [F(r["exact"]["signed_capture"]) for r in rows if r["exact"]["signed_capture"] is not None]
    positive_headroom = sum(max(F(0), F(r["exact"]["ceiling_gain"])) for r in rows)
    positive_gains = sum(max(F(0), g) for g in effects)
    return {"cases": len(rows), "families": len(family),
            "family_means": {g: float(v) for g, v in family.items()},
            "equal_family_mean": float(sum(family.values()) / len(family)),
            "wins": sum(g > 0 for g in effects), "ties": sum(g == 0 for g in effects),
            "harms": sum(g < 0 for g in effects),
            "ceiling_attainment": sum(r["attains_ceiling"] for r in rows),
            "positive_headroom_cases": len(capture),
            "mean_signed_capture_on_positive_headroom_cases": float(sum(capture) / len(capture)) if capture else None,
            "hindsight_positive_gain_capture_ratio": float(positive_gains / positive_headroom) if positive_headroom else None,
            "capture_is_outcome_informed_not_deployable": True}
