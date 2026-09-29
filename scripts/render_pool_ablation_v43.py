"""Reproduce V43 figure and complete flat results from measured records."""
import csv
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache/matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))
from escalation.io import read, write
from escalation.resources import Resources
from escalation.transfer_v41 import current_config


def main():
    before = read("artifacts/resource_ledger_v2.json")
    with Resources(current_config(), "artifacts/resource_ledger_v2.json") as resource:
        resource.check()
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        out = Path("results/v43_pool_ablation")
        summary = read(out / "summary.json")
        v42 = read("results/v42_selection_reference/summary.json")
        old = [r for r in v42["ceiling_comparisons"] if r["reference"] == "full_sequential_3nn"]
        values = [[0., 100 * sum(r["ceiling_gain"] for r in old) / 30,
                   100 * sum(max(0, r["ceiling_gain"]) for r in old) / 30]]
        # The original actual batch control comes from saved V41 acquired arms.
        from fractions import Fraction as F
        gains = []
        m = read("data/manifest_v41.json")
        for d in m["datasets"]:
            choose = min if d["direction"] == "-" else max
            for seed in m["seeds"]:
                targets = []
                for mode in ("batch_3nn", "full_sequential_3nn"):
                    a = read(f"results/v41_transfer/arms/{d['id']}_{seed}_{mode}.json")
                    targets.append(choose(F(str(y[0])) for y in a["state"]["labels"]))
                treatment, reference = targets
                gains.append(float((reference-treatment)/reference if d["direction"] == "-" else (treatment-reference)/reference))
        values[0][0] = 100 * sum(gains) / 30
        for pool in ("uniform20", "retained10_diverse10"):
            batch = next(r for r in summary["summaries"] if r["pool"] == pool and r["reference"] == "full_sequential_3nn" and r["endpoint"] == "batch_gain")
            ceiling = next(r for r in summary["summaries"] if r["pool"] == pool and r["reference"] == "full_sequential_3nn" and r["endpoint"] == "ceiling_gain")
            values.append([100*batch["equal_family_mean"], 100*ceiling["equal_family_mean"], 100*ceiling["positive_part_hindsight_mean"]])
        fig, axes = plt.subplots(1, 2, figsize=(11, 5))
        labels = ["Original shortlist", "Uniform20", "Retained10 + diverse10"]
        for j, (label, color) in enumerate((("Actual batch3NN", "#31688e"), ("Perfect selector*", "#b77724"))):
            positions = [i + (j-.5)*.32 for i in range(3)]
            bars = axes[0].bar(positions, [v[j] for v in values], width=.31, color=color, label=label)
            axes[0].bar_label(bars, fmt="%+.2f", padding=3, fontsize=9)
        axes[0].set_xticks(range(3), labels, rotation=12)
        axes[0].set_ylim(-3.5, .4)
        axes[0].axhline(0, color="#777777", linewidth=.7)
        axes[0].set_ylabel("Mean gain vs full-domain sequential3NN (%)")
        axes[0].set_title("Using each continuation on every case")
        axes[0].legend(loc="lower left", fontsize=9)
        bars = axes[1].bar(labels, [v[2] for v in values], color="#777777")
        axes[1].bar_label(bars, fmt="%.3f", padding=4)
        axes[1].set_ylim(0, 3.2)
        axes[1].tick_params(axis="x", labelrotation=12)
        axes[1].set_ylabel("Mean positive ceiling gain (%)")
        axes[1].set_title("Perfect selection AND perfect routing*")
        fig.suptitle("V43: wider candidate pools create opportunity, not an achieved LLM gain")
        fig.text(.5, .015, "*Outcome-informed, nondeployable diagnostics. Six exposed families; no new model calls.", ha="center", fontsize=10)
        fig.tight_layout(rect=(0,.055,1,.98))
        fig.savefig(out / "pool_ablation.png", dpi=170)
        fig.savefig(out / "pool_ablation.svg")
        plt.close(fig)
        flat = [{k: v for k, v in r.items() if k not in ("exact", "candidate_targets")} for r in summary["rows"]]
        with (out / "comparisons.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=flat[0])
            writer.writeheader()
            writer.writerows(flat)
    write("artifacts/study_v43/render_accounting.json", {"seconds": read("artifacts/resource_ledger_v2.json")["experiment_seconds"] - before["experiment_seconds"], "calls": 0, "new_accesses": 0})


if __name__ == "__main__":
    main()
