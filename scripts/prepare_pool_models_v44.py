"""Prepare all changed-pool prompts and tokenize locally; never generate."""
import hashlib
import os
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
from escalation.core import State
from escalation.finite_v6 import load_candidates, ALPHABET
from escalation.io import read, write, digest, now
from escalation.resources import Resources
from escalation.transfer_v41 import restrict, messages, current_config


def main():
    out = Path("results/v44_preflight")
    if out.exists():
        raise ValueError("Preserve preflight")
    before = read("artifacts/resource_ledger_v2.json")
    paths = [Path("reports/protocol_v44_pool_models.md"), Path(__file__).relative_to(ROOT),
        Path("scripts/run_pool_models_v44.py"), Path("tests/synthetic/test_pool_models_v44.py"),
        Path("artifacts/model_manifest_v22.json"), Path("artifacts/study_v22/model_download_plan.json"),
        Path("reports/protocol_v43_pool_ablation.freeze.json"), Path("data/manifest_v41.json")]
    paths += list(Path("src/escalation").glob("*.py"))
    rows = []
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        resource.check()
        os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("models/Qwen2.5-1.5B-Instruct", local_files_only=True, trust_remote_code=False)
        manifest = read("data/manifest_v41.json")
        for spec in manifest["datasets"]:
            c, subset = restrict(load_candidates(spec), spec["fixed_features"])
            if subset != spec["subset"]:
                raise ValueError("Feature domain changed")
            for seed in manifest["seeds"]:
                resource.check()
                key = f"{spec['id']}_{seed}"
                prefix_path = Path(f"results/v41_transfer/prefixes/{key}.json")
                plan_path = Path(f"results/v43_pool_ablation/plans/{key}.json")
                paths += [prefix_path, plan_path]
                old, plan = read(prefix_path), read(plan_path)
                for name, ranked in plan["pools"].items():
                    presented = list(ranked)
                    random.Random(seed + 70000).shuffle(presented)
                    pool = {"ranked": ranked, "mapping": dict(zip(ALPHABET[:20], presented))}
                    prompt = messages(c, State(**old["state"]), pool)
                    n = len(tokenizer.apply_chat_template(prompt, tokenize=True, add_generation_prompt=True))
                    record = {"dataset": spec["id"], "system_group": spec["system_group"], "seed": seed,
                        "pool_name": name, "pool": pool, "prefix_hash": old["prefix_hash"],
                        "messages": prompt, "prompt_hash": digest(prompt), "input_tokens": n,
                        "fallback_rows": plan["partitions"][name]["batch_3nn"]}
                    p = out / "prompts" / f"{key}_{name}.json"
                    write(p, record)
                    paths.append(p)
                    rows.append({"path": str(p), "input_tokens": n, "within_limit": n <= 4096})
        write(out / "summary.json", {"at": now(), "cases": len(rows), "rows": rows,
            "all_fit": all(r["within_limit"] for r in rows), "generation_executed": False,
            "new_model_requests": 0, "new_objective_accesses": 0})
        paths.append(out / "summary.json")
        write("reports/protocol_v44_pool_models.freeze.json", {"at": now(), "exploratory": True,
            "sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}})
    write("artifacts/study_v44/preflight_accounting.json", {"seconds": read("artifacts/resource_ledger_v2.json")["experiment_seconds"] - before["experiment_seconds"], "calls": 0, "accesses": 0})
    print("Prepared", len(rows), "prompts; maximum input tokens", max(r["input_tokens"] for r in rows))


if __name__ == "__main__":
    main()
