"""Portable standard-library replay from acquired records, without source tables.

Hashes establish consistency of this package, not authenticity against omitted
source data or a signature from an independent party. Local source-check
receipts are included separately. No inference, download or target acquisition.
"""
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def records(path):
    return [json.loads(s) for s in (ROOT / path).read_text().splitlines()]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gain(reference, treatment, direction):
    return (reference-treatment)/reference if direction == "-" else (treatment-reference)/reference


def best(state, direction):
    return (min if direction == "-" else max)(F(str(y[0])) for y in state["labels"])


def main():
    manifest = read("bundle_manifest_v45.json")
    for relative, sha in manifest["sha256"].items():
        p = Path(relative)
        require(not p.is_absolute() and ".." not in p.parts, "Unsafe manifest path")
        target = ROOT / p
        require(target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == sha,
                "Changed/missing bundle evidence: " + relative)
    prior = subprocess.run([sys.executable, "-I", "-S", str(ROOT / "scripts/verify_model_results_v41.py")],
                           capture_output=True, text=True, timeout=30)
    require(prior.returncode == 0, "V41 replay failed: " + prior.stderr)
    specifications = {d["id"]: d for d in read("data/manifest_v41.json")["datasets"]}
    acquired, journal_counts = {}, {}
    for path, expected, namespace in (
        ("results/v41_transfer/acquisitions.jsonl", 2400, "measured_v41"),
        ("results/v41_models/acquisitions.jsonl", 600, "measured_v41_llm"),
        ("results/v43_pool_ablation/acquisitions.jsonl", 1200, "measured_v43"),
        ("results/v44_models/acquisitions.jsonl", 600, "measured_v44_llm")):
        events = records(path)
        require(len(events) == expected, "Journal denominator")
        journal_counts[path] = len(events)
        for e in events:
            require(e["namespace"] == namespace, "Synthetic/unknown event namespace")
            require(specifications[e["dataset"]]["subset"]["source_lines"][e["row_id"]] == e["source_line"], "Source identity mapping")
            key = (e["dataset"], e["seed"], e["row_id"])
            value = F(e["raw_target"])
            require(value > 0 and (key not in acquired or acquired[key] == value), "Conflicting acquired outcomes")
            acquired[key] = value
    v43 = read("results/v43_pool_ablation/summary.json")
    v44 = read("results/v44_model_analysis/summary.json")
    require(len(v43["rows"]) == 120 and len(v44["paired"]) == 240, "Comparison denominator")
    for r in v43["rows"]:
        key = f"{r['dataset']}_{r['seed']}"
        direction = specifications[r["dataset"]]["direction"]
        choose = min if direction == "-" else max
        prefix = read(f"results/v41_transfer/prefixes/{key}.json")["state"]
        plan = read(f"results/v43_pool_ablation/plans/{key}.json")
        values = [acquired[(r["dataset"], r["seed"], i)] for i in plan["pools"][r["pool"]]]
        batch = read(f"results/v43_pool_ablation/arms/{key}_{r['pool']}_batch_3nn.json")["state"]
        ref = best(read(f"results/v41_transfer/arms/{key}_{r['reference']}.json")["state"], direction)
        ceiling = choose([best(prefix, direction), *values])
        require(F(r["exact"]["batch_gain"]) == gain(ref, best(batch, direction), direction), "V43batch arithmetic")
        require(F(r["exact"]["ceiling_gain"]) == gain(ref, ceiling, direction), "V43ceiling arithmetic")
    for r in v44["paired"]:
        key = f"{r['dataset']}_{r['seed']}"
        direction = specifications[r["dataset"]]["direction"]
        choose = min if direction == "-" else max
        prefix = read(f"results/v41_transfer/prefixes/{key}.json")["state"]
        prompt = read(f"results/v44_preflight/prompts/{key}_{r['pool']}.json")
        arm = read(f"results/v44_models/arms/{key}_{r['pool']}.json")
        require(arm["state"]["ids"][:10] == prefix["ids"] and arm["state"]["labels"][:10] == prefix["labels"], "Paired prefix")
        require(len(set(arm["state"]["ids"])) == 20 and arm["logical_evaluations"] == 20 and arm["actual_new_accesses"] == 10, "Paired budget")
        for row, y in zip(arm["state"]["ids"], arm["state"]["labels"]):
            require(float(acquired[(r["dataset"], r["seed"], row)]) == y[0], "Acquired arm labels")
        ceiling = choose([best(prefix, direction), *[acquired[(r["dataset"], r["seed"], i)] for i in prompt["pool"]["ranked"]]])
        target = best(arm["state"], direction)
        if r["reference"] == "pool_ceiling":
            ref = ceiling
        else:
            path = {"own_pool_batch3nn": f"results/v43_pool_ablation/arms/{key}_{r['pool']}_batch_3nn.json",
                    "original_batch3nn": f"results/v41_transfer/arms/{key}_batch_3nn.json",
                    "full_sequential3nn": f"results/v41_transfer/arms/{key}_full_sequential_3nn.json"}[r["reference"]]
            ref = best(read(path)["state"], direction)
        require(F(r["reference_best"]) == ref and F(r["model_best"]) == target and F(r["ceiling_best"]) == ceiling, "V44target arithmetic")
        require(F(r["exact"]["relative_gain"]) == gain(ref, target, direction), "V44gain arithmetic")
        require(F(r["exact"]["ceiling_gain"]) == gain(ref, ceiling, direction), "V44headroom arithmetic")
    require(len(v44["exact_random_comparisons"]) == 60, "Random comparator denominator")
    for r in v44["exact_random_comparisons"]:
        key = f"{r['dataset']}_{r['seed']}"
        direction = specifications[r["dataset"]]["direction"]
        choose = min if direction == "-" else max
        prefix = best(read(f"results/v41_transfer/prefixes/{key}.json")["state"], direction)
        prompt = read(f"results/v44_preflight/prompts/{key}_{r['pool']}.json")
        values = sorted([acquired[(r["dataset"], r["seed"], i)] for i in prompt["pool"]["ranked"]], reverse=direction == "+")
        model = best(read(f"results/v44_models/arms/{key}_{r['pool']}.json")["state"], direction)
        expected = sum(math.comb(19-i, 9) * gain(choose([prefix, value]), model, direction) for i, value in enumerate(values[:11])) / math.comb(20, 10)
        require(F(r["exact"]["expected_relative_gain"]) == expected, "Exact uniform expectation")
    for s in v44["summaries"]:
        rows = [r for r in v44["paired"] if r["pool"] == s["pool"] and r["reference"] == s["reference"]]
        require(len(rows) == 30, "Aggregate denominator")
        effects = [F(r["exact"]["relative_gain"]) for r in rows]
        require(abs(float(sum(effects)/30) - s["equal_family_mean"]) < 1e-14, "V44aggregate arithmetic")
        require([sum(g > 0 for g in effects), sum(g == 0 for g in effects), sum(g < 0 for g in effects)] == [s["wins"], s["ties"], s["harms"]], "Win/tie/harm counts")
    requests = records("results/v44_models/requests.jsonl")
    require(len(requests) == len({r["request_id"] for r in requests}) == 60, "Request denominator")
    require(sum(r["input_tokens"] for r in requests) == v44["collection_cost"]["input_tokens"], "Input usage total")
    require(sum(r["output_tokens"] for r in requests) == v44["collection_cost"]["output_tokens"], "Output usage total")
    print(json.dumps({"files_verified": len(manifest["sha256"]), "v41_replay": json.loads(prior.stdout),
        "recorded_acquisition_events": sum(journal_counts.values()), "v43_comparisons_replayed": 120,
        "v44_comparisons_replayed": 240, "v44_exact_random_references": 60, "v44_aggregate_contrasts": 8,
        "scope": "Acquired-record consistency and arithmetic only; no source-table authenticity, model logits, fresh inference or independent hardware replication"}, indent=2))


if __name__ == "__main__":
    main()
