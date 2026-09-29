"""Create a deterministic local V41–V44 evidence kit and verify its extraction."""
import hashlib
import json
import os
import subprocess
import sys
import time
import zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
from escalation.io import read, write
from escalation.resources import Resources
from escalation.transfer_v41 import current_config


def main():
    archive = Path("output/llm_escalation_v45_review.zip")
    if archive.exists():
        raise ValueError("Preserve existing archive identity")
    prior = Path("output/llm_escalation_v41_review.zip")
    if hashlib.sha256(prior.read_bytes()).hexdigest() != "84a935ae4373a7299dbf49f14f58434b3528fd893fad026245f426b3e75657c8":
        raise ValueError("Original review archive changed")
    with zipfile.ZipFile(prior) as z:
        content = {name: z.read(name) for name in z.namelist()}
    paths = [Path("scripts/verify_review_bundle_v45.py"), Path(__file__).relative_to(ROOT),
             Path("reports/review_guide_v45.md"), Path("AGENTS.md"), Path("THIRD_PARTY.md"),
             Path("requirements.lock.txt"), Path("pyproject.toml")]
    for version in (42, 43, 44):
        paths += list(Path("reports").glob(f"*v{version}*"))
        paths += list(Path("scripts").glob(f"*v{version}*.py"))
        paths += list(Path("tests/synthetic").glob(f"*v{version}*.py"))
        for folder in Path("results").glob(f"v{version}_*"):
            paths += [p for p in folder.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".csv", ".png", ".svg", ".log")]
        folder = Path(f"artifacts/study_v{version}")
        paths += [p for p in folder.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".log")]
    paths += list(Path("src/escalation").glob("*.py"))
    for path in sorted(set(paths)):
        data = path.read_bytes()
        if str(path) in content and content[str(path)] != data:
            raise ValueError("Would replace older evidence: " + str(path))
        content[str(path)] = data
    content["START_REVIEW.md"] = b"""# Local research results replay: V41 through V44

Start with reports/review_guide_v45.md and reports/models_v44.md.

After extracting this folder, run:

    python3 -I -S scripts/verify_review_bundle_v45.py

Only the Python standard library is required. The verifier checks every bundled
file hash, replays V41 results and checks the V43/V44 acquired-record comparisons.
It makes no model calls, downloads or objective acquisitions. See the guide for
the exact scope. This does not reproduce model logits or independently validate
the omitted original source tables; local source-check receipts are included.

Full datasets, model weights, third-party papers and personal credentials are
absent. This is a LOCAL review artifact, not a published/licensing-cleared data
release. Dataset redistribution permission remains unresolved. Nothing was sent
to Tim Menzies or uploaded. The study remains exploratory and does not establish
useful predictive routing or journal readiness.
"""
    content["bundle_manifest_v45.json"] = json.dumps({"scope": "Local acquired-record replay; no fresh inference",
        "sha256": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(content.items())}}, indent=2).encode()
    before = read("artifacts/resource_ledger_v2.json")
    receipts = []
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        resource.check()
        deadline = time.monotonic() + 75
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name, data in sorted(content.items()):
                info = zipfile.ZipInfo(name, (2026, 9, 25, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, data)
        dest = Path("artifacts/study_v45/clean_extraction")
        dest.mkdir(parents=True, exist_ok=False)
        with zipfile.ZipFile(archive) as z:
            z.extractall(dest)
        interpreters = [str(ROOT / ".venv/bin/python"),
            "/Users/mayankdhingra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]
        for interpreter in interpreters:
            timeout = min(30, deadline-time.monotonic())
            if timeout <= 0:
                raise RuntimeError("Review kit75second bound")
            result = subprocess.run([interpreter, "-I", "-S", str((dest / "scripts/verify_review_bundle_v45.py").resolve())],
                capture_output=True, text=True, timeout=timeout)
            receipts.append({"interpreter": interpreter, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
            write("artifacts/study_v45/replay_attempts.json", receipts)
            if result.returncode:
                raise RuntimeError(result.stderr)
        if json.loads(receipts[0]["stdout"]) != json.loads(receipts[1]["stdout"]):
            raise ValueError("Interpreter discrepancy")
        victim = dest / "results/v44_models/acquisitions.jsonl"
        original = victim.read_bytes()
        try:
            victim.write_bytes(original + b"\n")
            result = subprocess.run([interpreters[0], "-I", "-S", str((dest / "scripts/verify_review_bundle_v45.py").resolve())],
                capture_output=True, text=True, timeout=min(30, max(.1, deadline-time.monotonic())))
            if result.returncode == 0 or "Changed/missing bundle evidence" not in result.stderr:
                raise ValueError("Corruption not rejected")
        finally:
            victim.write_bytes(original)
    after = read("artifacts/resource_ledger_v2.json")
    write("artifacts/study_v45/review_bundle.json", {"path": str(archive), "bytes": archive.stat().st_size,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "files": len(content), "validation": receipts,
        "synthetic_corruption_rejected": True, "seconds": after["experiment_seconds"]-before["experiment_seconds"],
        "new_calls": 0, "new_accesses": 0, "uploaded_or_published": False})
    print("Verified", archive, len(content), "files; two isolated interpreters agree; corruption rejected")


if __name__ == "__main__":
    main()
