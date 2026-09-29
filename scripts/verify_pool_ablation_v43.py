"""Independent stdlib acquired-source, paired-budget and exact arithmetic audit."""
import csv
import hashlib
import itertools
import json
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(p):
    return json.loads((ROOT / p).read_text())


def verify():
    started = time.monotonic()
    root = "results/v43_pool_ablation/"
    manifest = load("data/manifest_v41.json")
    summary = load(root + "summary.json")
    for p, h in load("reports/protocol_v43_pool_ablation.freeze.json")["sha256"].items():
        assert hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h, p
    events = [json.loads(s) for s in (ROOT / root / "acquisitions.jsonl").read_text().splitlines()]
    assert len(events) == 1200
    specs = {s["id"]: s for s in manifest["datasets"]}
    seen = set()
    targets = {}
    counts = Counter()
    for e in events:
        assert e["namespace"] == "measured_v43" and e["split"] == "exposed_exploratory"
        s = specs[e["dataset"]]
        assert e["system_group"] == s["system_group"] and e["seed"] in manifest["seeds"]
        assert s["subset"]["source_lines"][e["row_id"]] == e["source_line"]
        k = (e["dataset"], e["seed"], e["pool"], e["arm"])
        assert (*k, e["row_id"]) not in seen
        seen.add((*k, e["row_id"]))
        counts[k] += 1
        source_key = (e["dataset"], e["source_line"])
        assert source_key not in targets or targets[source_key] == e["raw_target"]
        targets[source_key] = e["raw_target"]
    assert len(counts) == 120 and set(counts.values()) == {10}
    source_checks = 0
    for name, s in specs.items():
        with (ROOT / s["path"]).open(newline="") as stream:
            for line, row in enumerate(csv.DictReader(stream, delimiter=s["delimiter"]), 2):
                k = (name, line)
                if k not in targets:
                    continue
                assert row[s["primary_objective"]] == targets[k]
                source_checks += 1
    assert source_checks == len(targets)
    for name, s in specs.items():
        for seed in manifest["seeds"]:
            key = f"{name}_{seed}"
            old = load(f"results/v41_transfer/prefixes/{key}.json")
            plan = load(root + f"plans/{key}.json")
            assert plan["prefix_hash"] == old["prefix_hash"]
            for pool, parts in plan["partitions"].items():
                assert len(set(plan["pools"][pool])) == 20
                assert set(parts["batch_3nn"]).isdisjoint(parts["coverage_complement"])
                assert set(sum(parts.values(), [])) == set(plan["pools"][pool])
                for arm, ids in parts.items():
                    result = load(root + f"arms/{key}_{pool}_{arm}.json")
                    assert result["state"]["ids"] == old["state"]["ids"] + ids
                    assert result["state"]["labels"][:10] == old["state"]["labels"]
                    assert result["logical_evaluations"] == 20 and result["actual_new_accesses"] == 10
                    assert len(set(result["state"]["ids"])) == 20
                    recorded = [e for e in events if (e["dataset"], e["seed"], e["pool"], e["arm"]) == (name, seed, pool, arm)]
                    assert [e["row_id"] for e in recorded] == ids
                    assert [float(e["raw_target"]) for e in recorded] == [y[0] for y in result["state"]["labels"][10:]]
    assert len(summary["rows"]) == 120 and len(summary["summaries"]) == 12
    enumerated = 0
    distributions = {}
    for r in summary["rows"]:
        k = (r["dataset"], r["seed"], r["pool"])
        direction = r["direction"]
        choose = min if direction == "-" else max
        def effect(reference, treatment):
            return (reference - treatment) / reference if direction == "-" else (treatment - reference) / reference
        values = list(map(F, r["candidate_targets"]))
        prefix = F(r["prefix_best"])
        s = specs[r["dataset"]]
        plan = load(root + f"plans/{r['dataset']}_{r['seed']}.json")
        assert values == [F(targets[(r["dataset"], s["subset"]["source_lines"][i])]) for i in plan["pools"][r["pool"]]]
        ceiling = choose([prefix, *values])
        selected = [plan["pools"][r["pool"]].index(i) for i in plan["partitions"][r["pool"]]["batch_3nn"]]
        actual = choose([prefix, *[values[i] for i in selected]])
        baseline = load(f"results/v41_transfer/arms/{r['dataset']}_{r['seed']}_{r['reference']}.json")
        ref = choose([F(str(y[0])) for y in baseline["state"]["labels"]])
        assert ref == F(r["reference_best"]) and ceiling == F(r["ceiling_best"]) and actual == F(r["batch_best"])
        assert effect(ref, actual) == F(r["exact"]["batch_gain"])
        assert effect(ref, ceiling) == F(r["exact"]["ceiling_gain"])
        if k not in distributions:
            ordered = sorted(set([prefix, *values]), reverse=direction == "+")
            ranks = {v: i for i, v in enumerate(ordered)}
            clipped = [min(ranks[prefix], ranks[v]) for v in values]
            count = Counter(min(subset) for subset in itertools.combinations(clipped, 10))
            distributions[k] = {ordered[rank]: n for rank, n in count.items()}
            assert sum(count.values()) == 184756
            enumerated += 184756
        expected = sum(n * effect(ref, v) for v, n in distributions[k].items()) / 184756
        assert expected == F(r["exact"]["uniform_expected_gain"])
        if time.monotonic() - started > 25:
            raise RuntimeError("25-second independent verification cap")
    for s in summary["summaries"]:
        group = [r for r in summary["rows"] if r["pool"] == s["pool"] and r["reference"] == s["reference"]]
        effects = [F(r["exact"][s["endpoint"]]) for r in group]
        assert len(group) == 30
        assert abs(float(sum(effects) / 30) - s["equal_family_mean"]) < 1e-14
        assert [sum(v > 0 for v in effects), sum(v == 0 for v in effects), sum(v < 0 for v in effects)] == [s["wins"], s["ties"], s["harms"]]
        assert abs(float(sum(max(F(0), v) for v in effects) / 30) - s["positive_part_hindsight_mean"]) < 1e-14
        for margin, n in s["cases_above_margin"].items():
            assert n == sum(v > F(margin) for v in effects)
        for g, mean in s["family_means"].items():
            family = [F(r["exact"][s["endpoint"]]) for r in group if r["system_group"] == g]
            assert len(family) == 5 and abs(float(sum(family) / 5) - mean) < 1e-14
    return {"verified_events": len(events), "unique_source_rows": len(targets), "arms": 120,
            "comparisons": 120, "summaries": 12, "exact_distributions": 60,
            "hypothetical_subsets_enumerated_not_new_experiments": enumerated,
            "seconds": time.monotonic() - started, "source_objective_cells_parsed_only_if_acquired": True}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
