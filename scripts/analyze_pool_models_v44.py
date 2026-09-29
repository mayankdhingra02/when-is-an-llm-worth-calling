"""Validate and analyze real V44 evidence; no inference or synthetic responses."""
import csv
import hashlib
import os
import sys
import time
from fractions import Fraction as F
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
from escalation.io import read, write, lines, digest, now
from escalation.core import State
from escalation.pool_analysis_v44 import unique_requests, observed_total, contrast, aggregate, selected_rows
from escalation.resources import Resources
from escalation.transfer_v41 import current_config
from escalation.selection_v8 import parse_ids
from escalation.selection_reference_v42 import best, random_distribution, compare
from escalation.grammar_v8 import CandidateIDGrammar

CONTEXT = ("dataset", "system_group", "seed", "pool_name", "model_size", "namespace",
           "split", "prefix_hash", "grammar_mode", "prompt_version")


def verify_seal(path):
    seal = read(path)
    for name, expected in seal["sha256"].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise ValueError("Frozen input changed: " + name)
    return seal


def main():
    source, out = Path("results/v44_models"), Path("results/v44_model_analysis")
    if not (source / "started.json").exists():
        raise RuntimeError("No real V44 collection; no measured analysis created")
    if out.exists():
        raise ValueError("Preserve prior analysis; inspect before any recovery")
    seal = verify_seal("reports/analysis_addendum_v44.freeze.json")
    verify_seal("reports/protocol_v44_pool_models.freeze.json")
    if seal["at"] >= read(source / "started.json")["at"]:
        raise ValueError("Analysis freeze must precede collection")
    manifest = read("data/manifest_v41.json")
    groups = {d["system_group"] for d in manifest["datasets"]}
    pools = ("uniform20", "retained10_diverse10")
    expected = {(d["id"], seed, pool) for d in manifest["datasets"] for seed in manifest["seeds"] for pool in pools}
    before = read("artifacts/resource_ledger_v2.json")
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        resource.check()
        deadline = time.monotonic() + 30
        starts = unique_requests(lines(source / "request_starts.jsonl"))
        responses = unique_requests(lines(source / "requests.jsonl"))
        if not set(responses) <= set(starts) or len(starts) > 60:
            raise ValueError("Request provenance/denominator mismatch")
        identity = lambda r: (r["dataset"], r["seed"], r["pool_name"])
        observed = {identity(r) for r in starts.values()}
        if not observed <= expected or len(observed) != len(starts):
            raise ValueError("Duplicate/off-protocol case")
        events = lines(source / "acquisitions.jsonl")
        if len(events) > 600 or any(identity(e) not in observed for e in events):
            raise ValueError("Off-protocol acquisitions")
        missing = sorted(set(starts) - set(responses))
        progress = read(source / "progress.json")
        cost = {"intended_cases": 60, "request_attempts": len(starts), "response_records": len(responses),
            "missing_responses": missing, "intended_cases_without_request": len(expected - observed),
            "errors": sum(r["status"] != "response" for r in responses.values()),
            "recorded_accesses": len(events), "prior_v43_collection_accesses": 1200, "prior_v41_collection_accesses": 3000,
            "input_tokens": None if missing else observed_total(list(responses.values()), "input_tokens"),
            "output_tokens": None if missing else observed_total(list(responses.values()), "output_tokens"),
            "request_wall_seconds": None if missing else observed_total(list(responses.values()), "wall_seconds"),
            "stage_accounting": read("artifacts/study_v44/model_accounting.json"), "external_spend_usd": 0}
        write(out / "collection_cost.json", cost)
        if not progress["complete"] or missing or observed != expected or len(events) != 600:
            write(out / "incomplete.json", {"intended_cases": 60, "primary_aggregate_computed": False, "progress": progress})
            print("Incomplete intended collection; no primary quality aggregate")
            return
        runtime = read(source / "model_runtime.json")
        model_manifest = read("artifacts/model_manifest_v22.json")
        if (runtime["model_id"], runtime["revision"], runtime["provider"]) != (model_manifest["model_id"], model_manifest["revision"], "local_transformers"):
            raise ValueError("Wrong model provenance")
        if runtime["device"] != "cpu" or runtime["dtype"] != "torch.float32":
            raise ValueError("Wrong frozen inference execution mode")
        os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("models/Qwen2.5-1.5B-Instruct", local_files_only=True, trust_remote_code=False)
        grammar = CandidateIDGrammar(tokenizer)
        paired, random_rows, deployment, token_checks = [], [], [], []
        for spec in manifest["datasets"]:
            for seed in manifest["seeds"]:
                key = f"{spec['id']}_{seed}"
                old = read(f"results/v41_transfer/prefixes/{key}.json")
                for pool in pools:
                    resource.check()
                    if time.monotonic() > deadline:
                        raise RuntimeError("V44 analysis30second limit")
                    prompt = read(f"results/v44_preflight/prompts/{key}_{pool}.json")
                    arm = read(source / "arms" / f"{key}_{pool}.json")
                    if arm["prefix_hash"] != old["prefix_hash"] or arm["namespace"] != "measured_v44_llm":
                        raise ValueError("Arm prefix/provenance mismatch")
                    start, response = starts[arm["request_id"]], responses[arm["request_id"]]
                    for request in (start, response):
                        if identity(request) != (spec["id"], seed, pool) or request["system_group"] != spec["system_group"]:
                            raise ValueError("Wrong case identity")
                        if request["namespace"] != "measured_v44_llm" or request["split"] != "exposed_exploratory":
                            raise ValueError("Synthetic/unknown research namespace")
                        if request["model_size"] != "1.5" or request["grammar_mode"] != "candidate_order_v19" or request["prompt_version"] != "candidate_ids_v8_pool_ablation_v44":
                            raise ValueError("Wrong frozen model interface")
                        if request["messages"] != prompt["messages"] or request["prefix_hash"] != old["prefix_hash"]:
                            raise ValueError("Prompt/prefix identity")
                        if request["model_id"] != runtime["model_id"] or request["revision"] != runtime["revision"] or request["provider"] != "local_transformers" or request["parameters"] != {"do_sample": False, "max_new_tokens": 20}:
                            raise ValueError("Changed model/parameters")
                        context = {k: request[k] for k in CONTEXT}
                        cache = digest({"messages": request["messages"], "model": request["model_id"], "revision": request["revision"],
                            "parameters": request["parameters"], "context": context, "parser_projection": request["prompt_version"],
                            "grammar_domains": None, "grammar_mode": request["grammar_mode"]})
                        if cache != request["cache_key"]:
                            raise ValueError("Request cache provenance")
                    case_events = [e for e in events if identity(e) == (spec["id"], seed, pool)]
                    if len(case_events) != 10 or any(e["namespace"] != "measured_v44_llm" for e in case_events):
                        raise ValueError("Acquisition denominator/namespace")
                    coverage = [e for e in lines("results/v43_pool_ablation/acquisitions.jsonl") if e["dataset"] == spec["id"] and e["seed"] == seed and e["pool"] == pool]
                    covered = {e["row_id"]: F(e["raw_target"]) for e in coverage}
                    state = State(**old["state"])
                    for e in case_events:
                        if e["source_line"] != spec["subset"]["source_lines"][e["row_id"]] or F(e["raw_target"]) != covered[e["row_id"]]:
                            raise ValueError("Recorded source mismatch")
                        state.observe(e["row_id"], [float(e["raw_target"])], (spec["direction"],))
                    if state.record() != arm["state"] or arm["logical_evaluations"] != 20 or arm["actual_new_accesses"] != 10:
                        raise ValueError("Paired state/budget mismatch")
                    selected = selected_rows(response, prompt, arm)
                    if selected != state.ids[10:] or (arm["fallback"] is None and response["status"] != "response"):
                        raise ValueError("Proposal/fallback replay")
                    if response["status"] == "response":
                        text = tokenizer.apply_chat_template(response["messages"], tokenize=False, add_generation_prompt=True)
                        generated = response["generated_token_ids"]
                        if len(tokenizer(text)["input_ids"]) != response["input_tokens"] or response["input_tokens"] > 4096:
                            raise ValueError("Input-token accounting")
                        if hashlib.sha256(text.encode()).hexdigest() != response["rendered_prompt_sha256"]:
                            raise ValueError("Rendered prompt hash")
                        if len(generated) != response["output_tokens"] or len(generated) > 20 or tokenizer.decode(generated, skip_special_tokens=True) != response["raw_output"]:
                            raise ValueError("Output-token accounting")
                        grammar_error = None
                        try:
                            replayed = grammar.replay(generated)
                        except ValueError as exc:
                            grammar_error = str(exc)
                            if arm["fallback"] is None:
                                raise ValueError("Invalid grammar without fallback") from exc
                        if grammar_error is None and (replayed != response["selection_trace"] or grammar.sha256 != response["grammar_sha256"] or grammar.schedule != response["grammar_schedule"]):
                            raise ValueError("Grammar trace")
                        token_checks.append({"request_id": response["request_id"], "token_accounting_verified": True,
                            "grammar_valid": grammar_error is None, "grammar_error": grammar_error})
                    else:
                        token_checks.append({"request_id": response["request_id"], "token_accounting_verified": False,
                            "reason": "Request failed; retain observed usage only"})
                    prefix_best = best([F(str(y[0])) for y in old["state"]["labels"]], spec["direction"])
                    target = best([prefix_best, *[covered[i] for i in selected]], spec["direction"])
                    dist = random_distribution([covered[i] for i in prompt["pool"]["ranked"]], prefix_best, spec["direction"])
                    baseline_paths = {"own_pool_batch3nn": f"results/v43_pool_ablation/arms/{key}_{pool}_batch_3nn.json",
                        "original_batch3nn": f"results/v41_transfer/arms/{key}_batch_3nn.json",
                        "full_sequential3nn": f"results/v41_transfer/arms/{key}_full_sequential_3nn.json"}
                    references = {name: best([F(str(y[0])) for y in read(path)["state"]["labels"]], spec["direction"]) for name, path in baseline_paths.items()}
                    references["pool_ceiling"] = dist["ceiling"]
                    for name, value in references.items():
                        result = contrast(value, target, dist["ceiling"], spec["direction"])
                        paired.append({"dataset": spec["id"], "system_group": spec["system_group"], "seed": seed, "pool": pool,
                            "reference": name, "reference_best": str(value), "model_best": str(target), "ceiling_best": str(dist["ceiling"]),
                            "attains_ceiling": result["attains_ceiling"], "fallback": arm["fallback"] is not None,
                            "exact": {k: str(v) if v is not None else None for k, v in result.items() if k != "attains_ceiling"}})
                    random_result = compare(dist, target, spec["direction"])
                    random_rows.append({"dataset": spec["id"], "system_group": spec["system_group"], "seed": seed, "pool": pool,
                        **{k: float(v) for k, v in random_result.items()}, "exact": {k: str(v) for k, v in random_result.items()}})
                    deployment.append({"dataset": spec["id"], "seed": seed, "pool": pool, "logical_evaluations": 20, "requests": 1,
                        "prefix_seconds": old["prefix_seconds"], "observed_request_seconds": response.get("wall_seconds"),
                        "input_tokens": response.get("input_tokens"), "output_tokens": response.get("output_tokens"),
                        "shared_startup_seconds": runtime.get("startup_wall_seconds"), "startup_amortization_cases": 60,
                        "scope": "Modeled trace reuse; objective-access and scheduler overhead excluded; no live deployment measured"})
        summaries = [{"pool": pool, "reference": ref, **aggregate([r for r in paired if r["pool"] == pool and r["reference"] == ref], groups)}
                     for pool in pools for ref in ("own_pool_batch3nn", "original_batch3nn", "full_sequential3nn", "pool_ceiling")]
        random_summaries = []
        for pool in pools:
            family = {g: sum(F(r["exact"]["expected_relative_gain"]) for r in random_rows if r["pool"] == pool and r["system_group"] == g) / 5 for g in sorted(groups)}
            random_summaries.append({"pool": pool, "family_means": {g: float(v) for g, v in family.items()},
                "equal_family_mean": float(sum(family.values()) / len(family)), "scope": "Exact conditional uniform-subset reference"})
        write(out / "summary.json", {"at": now(), "scope": "Exploratory exposed-system real-model assay; not a validated router",
            "intended_cases": 60, "completed_cases": 60, "paired": paired, "summaries": summaries,
            "exact_random_comparisons": random_rows, "exact_random_summaries": random_summaries,
            "token_checks": token_checks, "collection_cost": cost, "modeled_always_call_deployment": deployment,
            "fallbacks": sum(r["fallback"] for r in paired if r["reference"] == "own_pool_batch3nn")})
        flat = [{**{k: v for k, v in r.items() if k != "exact"}, **r["exact"]} for r in paired]
        with (out / "paired_cases.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=flat[0]); writer.writeheader(); writer.writerows(flat)
    after = read("artifacts/resource_ledger_v2.json")
    write("artifacts/study_v44/analysis_accounting.json", {"seconds": after["experiment_seconds"] - before["experiment_seconds"], "new_calls": 0, "new_accesses": 0})
    print("Verified60real cases and240paired comparisons")


if __name__ == "__main__":
    main()
