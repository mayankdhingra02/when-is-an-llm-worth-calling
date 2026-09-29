"""Independent stdlib source/budget/arithmetic audit of real V44 outputs.

No project optimizer imports and no unacquired objective parsing. This verifies
records and arithmetic, not model logits or a separate hardware replication.
"""
import argparse
import csv
import hashlib
import json
import math
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify(root=ROOT):
    started = time.monotonic()
    def load(path):
        return json.loads((root / path).read_text())
    def records(path):
        return [json.loads(s) for s in (root / path).read_text().splitlines()]
    summary = load("results/v44_model_analysis/summary.json")
    manifest = load("data/manifest_v41.json")
    specs = {d["id"]: d for d in manifest["datasets"]}
    events = records("results/v44_models/acquisitions.jsonl")
    requests = records("results/v44_models/requests.jsonl")
    starts = records("results/v44_models/request_starts.jsonl")
    expected = {(d, seed, pool) for d in specs for seed in manifest["seeds"]
                for pool in ("uniform20", "retained10_diverse10")}
    identity = lambda r: (r["dataset"], r["seed"], r["pool_name"])
    assert len(events) == 600 and len(requests) == len(starts) == 60
    assert len({r["request_id"] for r in requests}) == 60
    assert {identity(r) for r in requests} == expected
    assert {r["request_id"] for r in requests} == {r["request_id"] for r in starts}
    for p in ("reports/protocol_v44_pool_models.freeze.json", "reports/analysis_addendum_v44.freeze.json"):
        for name, sha in load(p)["sha256"].items():
            assert hashlib.sha256((root / name).read_bytes()).hexdigest() == sha, name
    counts = Counter(identity(e) for e in events)
    assert set(counts) == expected and set(counts.values()) == {10}
    wanted = {(e["dataset"], e["source_line"]) for e in events}
    source = {}
    for name, spec in specs.items():
        with (root / spec["path"]).open(newline="") as stream:
            for line, row in enumerate(csv.DictReader(stream, delimiter=spec["delimiter"]), 2):
                if (name, line) not in wanted:
                    continue
                source[(name, line)] = row[spec["primary_objective"]]
    assert set(source) == wanted
    for e in events:
        assert e["namespace"] == "measured_v44_llm"
        assert e["raw_target"] == source[(e["dataset"], e["source_line"])]
        assert specs[e["dataset"]]["subset"]["source_lines"][e["row_id"]] == e["source_line"]
    assert len(summary["paired"]) == 240 and len(summary["exact_random_comparisons"]) == 60
    for request in requests:
        dataset, seed, pool = identity(request)
        key = f"{dataset}_{seed}"
        prompt = load(f"results/v44_preflight/prompts/{key}_{pool}.json")
        prefix = load(f"results/v41_transfer/prefixes/{key}.json")
        arm = load(f"results/v44_models/arms/{key}_{pool}.json")
        case_events = [e for e in events if identity(e) == identity(request)]
        assert arm["request_id"] == request["request_id"]
        assert request["messages"] == prompt["messages"]
        assert arm["state"]["ids"][:10] == prefix["state"]["ids"]
        assert arm["state"]["labels"][:10] == prefix["state"]["labels"]
        assert len(set(arm["state"]["ids"])) == 20
        assert arm["state"]["ids"][10:] == [e["row_id"] for e in case_events]
        assert [y[0] for y in arm["state"]["labels"][10:]] == [float(e["raw_target"]) for e in case_events]
        assert arm["logical_evaluations"] == 20 and arm["actual_new_accesses"] == 10
        if arm["fallback"] is None:
            assert request["status"] == "response"
            ids = request["raw_output"].strip().splitlines()
            assert len(ids) == len(set(ids)) == 10
            selected = [prompt["pool"]["mapping"][i] for i in ids]
        else:
            selected = prompt["fallback_rows"]
        assert selected == arm["state"]["ids"][10:]
        direction = specs[dataset]["direction"]
        best = min if direction == "-" else max
        def gain(reference, treatment):
            return (reference - treatment) / reference if direction == "-" else (treatment - reference) / reference
        prefix_best = best(F(str(y[0])) for y in prefix["state"]["labels"])
        model = best([prefix_best, *[F(e["raw_target"]) for e in case_events]])
        coverage = [e for e in records("results/v43_pool_ablation/acquisitions.jsonl")
                    if e["dataset"] == dataset and e["seed"] == seed and e["pool"] == pool]
        values = {e["row_id"]: F(e["raw_target"]) for e in coverage}
        assert set(values) == set(prompt["pool"]["ranked"])
        ceiling = best([prefix_best, *values.values()])
        references = {"pool_ceiling": ceiling}
        for name, path in (
            ("own_pool_batch3nn", f"results/v43_pool_ablation/arms/{key}_{pool}_batch_3nn.json"),
            ("original_batch3nn", f"results/v41_transfer/arms/{key}_batch_3nn.json"),
            ("full_sequential3nn", f"results/v41_transfer/arms/{key}_full_sequential_3nn.json")):
            references[name] = best(F(str(y[0])) for y in load(path)["state"]["labels"])
        paired = [r for r in summary["paired"] if (r["dataset"], r["seed"], r["pool"]) == (dataset, seed, pool)]
        assert len(paired) == 4 and {r["reference"] for r in paired} == set(references)
        for r in paired:
            ref = references[r["reference"]]
            g, h = gain(ref, model), gain(ref, ceiling)
            assert F(r["reference_best"]) == ref and F(r["model_best"]) == model and F(r["ceiling_best"]) == ceiling
            assert F(r["exact"]["relative_gain"]) == g and F(r["exact"]["ceiling_gain"]) == h
            for name, value in (("signed_capture", g/h if h > 0 else None),
                                ("positive_capture", max(F(0), g)/h if h > 0 else None)):
                assert r["exact"][name] == (str(value) if value is not None else None)
            assert r["attains_ceiling"] == (model == ceiling)
        # Independent finite order-statistic count; V43 already exhaustively
        # verified each of these 60 pool distributions by subset enumeration.
        ordered = sorted(values.values(), reverse=direction == "+")
        count = Counter()
        for rank in range(11):
            count[best([prefix_best, ordered[rank]])] += math.comb(19-rank, 9)
        denominator = math.comb(20, 10)
        assert sum(count.values()) == denominator
        expected_gain = sum(n * gain(target, model) for target, n in count.items()) / denominator
        random = [r for r in summary["exact_random_comparisons"] if (r["dataset"], r["seed"], r["pool"]) == (dataset, seed, pool)]
        assert len(random) == 1 and F(random[0]["exact"]["expected_relative_gain"]) == expected_gain
        if time.monotonic() - started > 25:
            raise RuntimeError("Independent verifier25second limit")
    assert len(summary["summaries"]) == 8
    for s in summary["summaries"]:
        paired = [r for r in summary["paired"] if r["reference"] == s["reference"] and r["pool"] == s["pool"]]
        assert len(paired) == 30
        g = [F(r["exact"]["relative_gain"]) for r in paired]
        assert abs(float(sum(g)/30) - s["equal_family_mean"]) < 1e-14
        assert [sum(v > 0 for v in g), sum(v == 0 for v in g), sum(v < 0 for v in g)] == [s["wins"], s["ties"], s["harms"]]
        assert s["ceiling_attainment"] == sum(r["attains_ceiling"] for r in paired)
        for family, mean in s["family_means"].items():
            family_g = [F(r["exact"]["relative_gain"]) for r in paired if r["system_group"] == family]
            assert len(family_g) == 5 and abs(float(sum(family_g)/5) - mean) < 1e-14
        captures = [F(r["exact"]["signed_capture"]) for r in paired if r["exact"]["signed_capture"] is not None]
        assert len(captures) == s["positive_headroom_cases"]
        expected_capture = float(sum(captures)/len(captures)) if captures else None
        assert expected_capture == s["mean_signed_capture_on_positive_headroom_cases"]
        headroom = sum(max(F(0), F(r["exact"]["ceiling_gain"])) for r in paired)
        ratio = float(sum(max(F(0), v) for v in g) / headroom) if headroom else None
        assert ratio == s["hindsight_positive_gain_capture_ratio"]
    for field in ("input_tokens", "output_tokens"):
        expected_total = None if any(r.get(field) is None for r in requests) else sum(r[field] for r in requests)
        assert summary["collection_cost"][field] == expected_total
    return {"real_model_cases": 60, "verified_acquisitions": 600, "unique_source_rows": len(source),
            "exact_paired_comparisons": 240, "exact_random_comparisons": 60, "aggregate_contrasts": 8,
            "seconds": time.monotonic()-started, "new_calls": 0, "new_accesses": 0,
            "model_logits_recomputed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(verify(args.root), indent=2))
