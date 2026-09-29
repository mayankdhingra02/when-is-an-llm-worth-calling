"""Real-model collector, disabled until an exact new bounded approval exists."""
import hashlib
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.io import read, write, append, digest, now
from escalation.order_probe_v19 import StageResources
from escalation.provider_v22 import LargerProvider
from escalation.resources import Resources
from escalation.selection_v8 import parse_ids
from escalation.transfer_v41 import restrict, IndexedOracle, current_config


def authorized_config(authorization, freeze_hash):
    required = {"granted": True, "additional_requests": 60, "request_cap": 350,
        "runtime_cap_seconds": 3600, "stage_seconds": 450, "max_new_vectors": 600,
        "new_downloads": 0, "external_spend_usd": 0, "request_retries": 0,
        "protocol_freeze_sha256": freeze_hash}
    if any(authorization.get(k) != v for k, v in required.items()) or not authorization.get("user_authorization"):
        raise PermissionError("V44 requires exact new approval:60local requests,290->350,450s stage within3600s,USD0")
    cfg = current_config()
    cfg["inference"].update(max_new_model_requests=350, max_output_tokens_per_request=20,
                            request_timeout_seconds=30, max_retries_per_request=0)
    if cfg["inference"]["allow_paid_api"] or cfg["inference"]["max_external_spend_usd"] != 0:
        raise PermissionError("Paid inference disabled")
    return cfg


def main():
    freeze = Path("reports/protocol_v44_pool_models.freeze.json")
    auth = read("configs/authorization_v44.json")
    cfg = authorized_config(auth, hashlib.sha256(freeze.read_bytes()).hexdigest())
    for path, h in read(freeze)["sha256"].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest() != h:
            raise ValueError("Changed frozen input: " + path)
    out = Path("results/v44_models")
    if out.exists():
        raise ValueError("Preserve prior attempt; no implicit restart")
    preflight = read("results/v44_preflight/summary.json")
    if not preflight["all_fit"] or preflight["cases"] != 60:
        raise ValueError("Preflight incomplete")
    before = read("artifacts/resource_ledger_v2.json")
    if before["requests"] != 290:
        raise ValueError("Expected290-call starting ledger")
    acquired, stop = 0, None
    statuses = {r["path"]: "unattempted" for r in preflight["rows"]}
    with Resources(cfg, "artifacts/resource_ledger_v2.json") as resource:
        if resource.remaining() < 465:
            raise RuntimeError("Need450second stage and cleanup reserve")
        stage = StageResources(resource, 450)
        write(out / "started.json", {"at": now(), "cases": 60, "baseline_ledger": before})
        try:
            with LargerProvider(cfg, stage, out / "requests.jsonl") as model:
                for spec in read("data/manifest_v41.json")["datasets"]:
                    c, subset = restrict(load_candidates(spec), spec["fixed_features"])
                    if subset != spec["subset"]:
                        raise ValueError("Changed feature domain")
                    for job in preflight["rows"]:
                        p = read(job["path"])
                        if p["dataset"] != spec["id"]:
                            continue
                        stage.check()
                        key = f"{spec['id']}_{p['seed']}"
                        old = read(f"results/v41_transfer/prefixes/{key}.json")
                        state = State(**old["state"])
                        if digest(state.record()) != p["prefix_hash"] or digest(p["messages"]) != p["prompt_hash"]:
                            raise ValueError("Prefix/prompt binding")
                        context = {"dataset": spec["id"], "system_group": spec["system_group"],
                            "seed": p["seed"], "pool_name": p["pool_name"], "model_size": "1.5",
                            "namespace": "measured_v44_llm", "split": "exposed_exploratory",
                            "prefix_hash": p["prefix_hash"], "grammar_mode": "candidate_order_v19",
                            "prompt_version": "candidate_ids_v8_pool_ablation_v44"}
                        statuses[job["path"]] = "started"
                        response = model.request(p["messages"], context)
                        fallback = None
                        try:
                            if response["status"] != "response":
                                raise ValueError("Failed request")
                            selected = parse_ids(response["raw_output"], p["pool"])
                        except Exception as exc:
                            fallback = str(exc)
                            selected = p["fallback_rows"]
                        oracle = IndexedOracle(spec, c, old["state"],
                            lambda e: append(out / "acquisitions.jsonl", {**context, **e, "at": now()}))
                        for row in selected:
                            stage.check()
                            if acquired >= 600:
                                raise RuntimeError("600access cap")
                            acquired += 1
                            state.observe(row, oracle.acquire(row), c.directions)
                            write(out / "checkpoints" / f"{key}_{p['pool_name']}.json", state.record())
                        write(out / "arms" / f"{key}_{p['pool_name']}.json", {**context,
                            "state": state.record(), "status": "completed", "fallback": fallback,
                            "request_id": response["request_id"], "logical_evaluations": 20,
                            "actual_new_accesses": oracle.new_accesses})
                        statuses[job["path"]] = "completed"
                        print(key, p["pool_name"], "completed", flush=True)
        except Exception as exc:
            stop = f"{type(exc).__name__}: {exc}"
        finally:
            write(out / "progress.json", {"complete": all(v == "completed" for v in statuses.values()) and stop is None,
                "statuses": statuses, "stop_reason": stop, "charged_access_attempts": acquired})
    after = read("artifacts/resource_ledger_v2.json")
    write("artifacts/study_v44/model_accounting.json", {"calls": after["requests"] - before["requests"],
        "seconds": after["experiment_seconds"] - before["experiment_seconds"], "recorded_access_attempts": acquired,
        "external_spend_usd": 0})
    if stop:
        raise RuntimeError(stop)


if __name__ == "__main__":
    main()
