"""One-shot, stage-capped preparation, classical collection and analysis."""
import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.io import read, write, append, lines, now
from escalation.pool_ablation_v43 import pools, partition
from escalation.resources import Resources
from escalation.selection_reference_v42 import best, gain, random_distribution
from escalation.transfer_v41 import restrict, IndexedOracle, current_config

OUT = Path("results/v43_pool_ablation")
ART = Path("artifacts/study_v43")
FREEZE = Path("reports/protocol_v43_pool_ablation.freeze.json")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_freeze():
    for p, h in read(FREEZE)["sha256"].items():
        if sha(p) != h:
            raise ValueError("Changed frozen input: " + p)


def check(resource):
    resource.check()
    elapsed = resource.d["experiment_seconds"] - read(ART / "baseline_ledger.json")["experiment_seconds"]
    if elapsed >= 120:
        raise RuntimeError("V43 total120-second cap")


def prepare():
    if OUT.exists() or FREEZE.exists():
        raise ValueError("Preserve existing experiment")
    write(ART / "baseline_ledger.json", read("artifacts/resource_ledger_v2.json"))
    manifest = read("data/manifest_v41.json")
    paths = [Path("data/manifest_v41.json"), Path("reports/protocol_v43_pool_ablation.md"),
             Path(__file__).relative_to(ROOT), Path("scripts/verify_pool_ablation_v43.py")]
    paths += list(Path("src/escalation").glob("*.py"))
    paths += [Path("tests/synthetic/test_pool_ablation_v43.py")]
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        if resource.remaining() < 125:
            raise RuntimeError("Need full V43 reserve")
        for spec in manifest["datasets"]:
            check(resource)
            if sha(spec["path"]) != spec["sha256"]:
                raise ValueError("Source hash mismatch")
            paths.append(Path(spec["path"]))
            c, subset = restrict(load_candidates(spec), spec["fixed_features"])
            if subset != spec["subset"]:
                raise ValueError("Changed feature domain")
            for seed in manifest["seeds"]:
                key = f"{spec['id']}_{seed}"
                path = Path(f"results/v41_transfer/prefixes/{key}.json")
                old = read(path)
                p = State(**old["state"])
                alternatives = pools(c, p, old["pool"]["ranked"], seed)
                record = {"dataset": spec["id"], "system_group": spec["system_group"],
                          "seed": seed, "prefix_hash": old["prefix_hash"], "pools": alternatives,
                          "partitions": {name: partition(c, p, rows) for name, rows in alternatives.items()}}
                target = OUT / "plans" / f"{key}.json"
                write(target, record)
                paths += [path, target]
                for mode in ("batch_3nn", "full_sequential_3nn"):
                    paths.append(Path(f"results/v41_transfer/arms/{key}_{mode}.json"))
        paths.append(Path("results/v42_selection_reference/summary.json"))
        write(FREEZE, {"at": now(), "exploratory": True,
                       "sha256": {str(p): sha(p) for p in sorted(set(paths))}})
    print("Frozen30prefixes/60newpools; zero new objective accesses", flush=True)


def collect():
    if (OUT / "started.json").exists():
        raise ValueError("No implicit retry/overwrite")
    verify_freeze()
    manifest = read("data/manifest_v41.json")
    intended = [f"{d['id']}_{seed}_{pool}_{arm}" for d in manifest["datasets"]
                for seed in manifest["seeds"] for pool in ("uniform20", "retained10_diverse10")
                for arm in ("batch_3nn", "coverage_complement")]
    write(OUT / "started.json", {"at": now(), "intended_arms": intended,
                                 "max_accesses": 1200, "max_collection_seconds": 90})
    stop = None
    acquired = 0
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        deadline = time.monotonic() + 90
        try:
            for spec in manifest["datasets"]:
                c, subset = restrict(load_candidates(spec), spec["fixed_features"])
                if subset != spec["subset"]:
                    raise ValueError("Changed feature domain")
                for seed in manifest["seeds"]:
                    key = f"{spec['id']}_{seed}"
                    old = read(f"results/v41_transfer/prefixes/{key}.json")
                    plan = read(OUT / "plans" / f"{key}.json")
                    for pool, arms in plan["partitions"].items():
                        for arm, ids in arms.items():
                            context = {"dataset": spec["id"], "system_group": spec["system_group"],
                                       "seed": seed, "pool": pool, "arm": arm,
                                       "namespace": "measured_v43", "split": "exposed_exploratory"}
                            oracle = IndexedOracle(spec, c, old["state"],
                                lambda e: append(OUT / "acquisitions.jsonl", {**context, **e, "at": now()}))
                            state = State(**old["state"]).clone()
                            started = time.perf_counter()
                            for row in ids:
                                check(resource)
                                if time.monotonic() >= deadline or acquired >= 1200:
                                    raise RuntimeError("V43collection cap")
                                acquired += 1
                                state.observe(row, oracle.acquire(row), c.directions)
                            write(OUT / "arms" / f"{key}_{pool}_{arm}.json", {
                                **context, "state": state.record(), "prefix_hash": old["prefix_hash"],
                                "logical_evaluations": 20, "actual_new_accesses": oracle.new_accesses,
                                "seconds": time.perf_counter() - started})
                    print(key, "four classical/coverage arms completed", flush=True)
        except Exception as exc:
            stop = f"{type(exc).__name__}: {exc}"
        finally:
            statuses = {k: (OUT / "arms" / f"{k}.json").exists() for k in intended}
            write(OUT / "progress.json", {"complete": all(statuses.values()) and stop is None,
                  "statuses": statuses, "stop_reason": stop, "charged_attempts": acquired,
                  "recorded_accesses": len(lines(OUT / "acquisitions.jsonl"))})
    if stop:
        raise RuntimeError(stop)


def analyze():
    verify_freeze()
    if (OUT / "summary.json").exists():
        raise ValueError("Preserve analysis")
    if not read(OUT / "progress.json")["complete"]:
        raise ValueError("Incomplete denominator")
    rows = []
    manifest = read("data/manifest_v41.json")
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        events = lines(OUT / "acquisitions.jsonl")
        values = {}
        for e in events:
            key = (e["dataset"], e["seed"], e["row_id"])
            value = F(e["raw_target"])
            if key in values and values[key] != value:
                raise ValueError("Conflicting acquired outcome")
            values[key] = value
        original = read("results/v42_selection_reference/summary.json")
        for spec in manifest["datasets"]:
            for seed in manifest["seeds"]:
                check(resource)
                key = f"{spec['id']}_{seed}"
                old = read(f"results/v41_transfer/prefixes/{key}.json")
                prefix = best([F(str(y[0])) for y in old["state"]["labels"]], spec["direction"])
                plan = read(OUT / "plans" / f"{key}.json")
                for pool, ids in plan["pools"].items():
                    targets = [values[(spec["id"], seed, i)] for i in ids]
                    dist = random_distribution(targets, prefix, spec["direction"])
                    batch_ids = plan["partitions"][pool]["batch_3nn"]
                    actual = best([prefix, *[values[(spec["id"], seed, i)] for i in batch_ids]], spec["direction"])
                    for reference in ("batch_3nn", "full_sequential_3nn"):
                        baseline = read(f"results/v41_transfer/arms/{key}_{reference}.json")
                        reference_best = best([F(str(y[0])) for y in baseline["state"]["labels"]], spec["direction"])
                        original_ceiling = next(r for r in original["ceiling_comparisons"]
                            if r["dataset"] == spec["id"] and r["seed"] == seed and r["reference"] == reference)
                        exact = {"batch_gain": gain(reference_best, actual, spec["direction"]),
                            "ceiling_gain": gain(reference_best, dist["ceiling"], spec["direction"]),
                            "original_ceiling_gain": F(original_ceiling["exact_ceiling_gain"]),
                            "uniform_expected_gain": sum(count * gain(reference_best, target, spec["direction"])
                                 for target, count in dist["counts"].items()) / dist["denominator"]}
                        rows.append({"dataset": spec["id"], "system_group": spec["system_group"], "seed": seed,
                            "pool": pool, "reference": reference, "direction": spec["direction"],
                            "reference_best": str(reference_best), "batch_best": str(actual),
                            "ceiling_best": str(dist["ceiling"]), "prefix_best": str(prefix),
                            "candidate_targets": list(map(str, targets)),
                            **{k: float(v) for k, v in exact.items()}, "exact": {k: str(v) for k, v in exact.items()}})
        summaries = []
        for pool in ("uniform20", "retained10_diverse10"):
            for reference in ("batch_3nn", "full_sequential_3nn"):
                group = [r for r in rows if r["pool"] == pool and r["reference"] == reference]
                for endpoint in ("batch_gain", "ceiling_gain", "uniform_expected_gain"):
                    by_family = {g: sum(F(r["exact"][endpoint]) for r in group if r["system_group"] == g)/5
                                 for g in sorted({r["system_group"] for r in group})}
                    effects = [F(r["exact"][endpoint]) for r in group]
                    summaries.append({"pool": pool, "reference": reference, "endpoint": endpoint,
                        "equal_family_mean": float(sum(by_family.values())/len(by_family)),
                        "family_means": {g: float(v) for g, v in by_family.items()},
                        "wins": sum(v > 0 for v in effects), "ties": sum(v == 0 for v in effects),
                        "harms": sum(v < 0 for v in effects),
                        "positive_part_hindsight_mean": float(sum(max(F(0), v) for v in effects)/len(effects)),
                        "cases_above_margin": {str(m): sum(v > F(str(m)) for v in effects) for m in (0, .01, .05)}})
        write(OUT / "summary.json", {"at": now(), "scope": "Exposed-system classical candidate-pool ablation; no new LLM experiment",
              "rows": rows, "summaries": summaries, "new_model_calls": 0, "new_recorded_accesses": 1200,
              "prior_v41_collection_accesses": 3000, "new_physical_trials": 0})
    write(ART / "accounting.json", {"seconds": read("artifacts/resource_ledger_v2.json")["experiment_seconds"] -
        read(ART / "baseline_ledger.json")["experiment_seconds"], "calls": 0, "recorded_accesses": 1200,
        "new_physical_trials": 0, "external_spend_usd": 0})
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "collect": collect, "analyze": analyze}[sys.argv[1]]()
