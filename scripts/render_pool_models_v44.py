"""Render fixed V44 contrasts; do not select favorable cases or references."""
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
        summary = read("results/v44_model_analysis/summary.json")
        pools = ("uniform20", "retained10_diverse10")
        names = ("Uniform20", "Retained10 + diverse10")
        fig, axes = plt.subplots(1, 2, figsize=(11, 5))
        all_means = []
        for j, (reference, label, color) in enumerate((
            ("own_pool_batch3nn", "Own-pool batch3NN", "#31688e"),
            ("full_sequential3nn", "Full-domain sequential3NN", "#b77724"))):
            means = [100 * next(r["equal_family_mean"] for r in summary["summaries"] if r["pool"] == pool and r["reference"] == reference) for pool in pools]
            all_means += means
            bars = axes[0].bar([i + (j-.5)*.32 for i in range(2)], means, width=.31, label=label, color=color)
            axes[0].bar_label(bars, fmt="%+.3f%%", padding=5)
        axes[0].set_xticks(range(2), names)
        axes[0].axhline(0, color="#666666", linewidth=.8)
        axes[0].set_ylim(min(0, min(all_means))-1.2, max(0, max(all_means))+1.6)
        axes[0].set_ylabel("Equal-family mean relative gain (%)")
        axes[0].set_title("Real1.5B model compared with cheap controls")
        axes[0].legend(loc="upper left", fontsize=9)
        attained = [next(r["ceiling_attainment"] for r in summary["summaries"] if r["pool"] == pool and r["reference"] == "own_pool_batch3nn") for pool in pools]
        bars = axes[1].bar(names, attained, color="#527a3d")
        axes[1].bar_label(bars, labels=[f"{n}/30" for n in attained], padding=4)
        axes[1].set_ylim(0, 34)
        axes[1].set_ylabel("Cases attaining their pool's best available target")
        axes[1].set_title("Outcome-informed ceiling attainment")
        fig.suptitle("V44: real-model selection on two changed candidate pools")
        fig.text(.5, .018, "Six exposed families × five seeds per pool. Exploratory; no validated routing claim.", ha="center", fontsize=10)
        fig.tight_layout(rect=(0,.06,1,.97))
        out = Path("results/v44_model_analysis")
        fig.savefig(out / "model_pool_comparison.png", dpi=170)
        fig.savefig(out / "model_pool_comparison.svg")
        plt.close(fig)
    write("artifacts/study_v44/render_accounting.json", {"seconds": read("artifacts/resource_ledger_v2.json")["experiment_seconds"] - before["experiment_seconds"], "new_calls": 0, "new_accesses": 0})


if __name__ == "__main__":
    main()
