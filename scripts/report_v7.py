"""Report only actually executed v7 stages, preserving blocked denominators."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read

def main():
    s=read('results/v7/summary.json');v=read('artifacts/study_v7/verification.json');l=read('artifacts/resource_ledger_v2.json');complete=s['complete'];authorization=read('configs/authorization_v7.json')
    tests=Path('artifacts/study_v7/tests_after_approval.log').read_text().strip().splitlines()[-1]
    diagnostics=read('results/v7/proposal_diagnostics.json') if complete else None
    model_runtime=read('results/v7/model_runtime.json') if complete else {}
    report='''# V7: development-only prefix-copy exclusion

This is a versioned exploratory response to v6's observed copying behavior, not a fresh held-out routing evaluation. Only MySQL, lrzip and Brotli development groups enter, with all five original seeds and exactly the same ten-label prefixes. No controller is retrained and no held-out outcomes are used in this analysis.

The sole model intervention is decoding-time exclusion of the original ten feature strings. Prompts, model/revision, CPU/float32, greedy decoding, candidate domains, ten-proposal batch, projection and budgets match v6. A corresponding uniform-random control samples exactly from the domain complement of those same strings. Repeated novel proposals within a batch remain possible. Zero original-prefix copies is enforced by construction, not a scientific success criterion.

'''
    if complete:
        report+='**Both new arms completed: 15 constrained local-LLM continuations and 15 matched random controls.** These are development-only measurements, not validation of generalization.\n\n'
        for baseline,r in s['paired_gain_summary'].items():
            report+=f"Against {baseline}: mean normalized-loss gain {r['mean_gain']:.6f}, material help {r['material_help']}/15, material harm {r['material_harm']}/15 (fixed .02 margin).\n\n"
    else:
        report+='**The full LLM arm is incomplete.** Counts and reasons remain in `results/v7/progress.json`; no complete-case LLM quality comparison is reported. The 15 matched controls remain available.\n\n'
    if complete:
        old=diagnostics['totals']['original'];new=diagnostics['totals']['excluded']
        report+=f"The exclusion constraint removed original-prefix copying ({old['prefix_copies']}/{old['count']} → {new['prefix_copies']}/{new['count']} on the same 15 cases), but did not establish improved optimization. Only {new['valid_recorded_configurations']}/{new['count']} raw proposals matched an available recorded configuration; the rest needed projection. Absence from the table does not prove a configuration is invalid in the real software. Within-batch repetition increased from {old['within_batch_repetitions']} to {new['within_batch_repetitions']}. These are post-hoc descriptive diagnostics, not a new selected treatment.\n\n"
    columns=['classical','original_llm','uniform_original','uniform_excluded']+(['llm_excluded'] if complete else [])
    report+='| Family | '+ ' | '.join(columns)+' |\n|---|'+ '|'.join('---:' for _ in columns)+'|\n'
    for r in s['systems']:report+='| '+r['system_group']+' | '+' | '.join(f'{r[c]:.6f}' for c in columns)+' |\n'
    report+='\nValues are mean normalized loss over five seeds per development family; lower is better. Original arms are immutable v6 records, not new collection. The new conditioned-uniform sampler has the correct conditional distribution, but the same seed does not imply identical random draws to the old coordinate-wise sampler. Differences between those random controls are not an isolated causal estimate of exclusion.\n\n![Development comparison](../results/v7/comparison.png)\n\n![Paired gains](../results/v7/paired_gains.png)\n\n'
    c=s['collection']
    report+='| Arm | Completed / intended | Projections | Acquired-row collisions | Fallback acquisitions |\n|---|---:|---:|---:|---:|\n'
    for row in s['reliability']:
        report+=f"| {row['arm']} | {row['completed_or_fallback']}/{row['intended']} | {row['projected']} | {row['collision']} | {row['fallback']} |\n"
    report+='\n'
    if complete:
        report+=f"Actual model startup/load wall time was {model_runtime['startup_wall_seconds']:.3f} seconds, separate from request time. Hypothetically deploying just the new LLM continuation across these 15 cases would require 15 × 20 = 300 logical objective acquisitions (including prefixes) and 15 requests. This is distinct from the new research acquisitions below, which cover both new branches while reusing historical prefixes.\n\n"
    report+=f'''Actual v7 collection: **{c['new_objective_accesses']} new objective acquisitions**, **{c['model_attempts']} local-model attempts**, {c['input_tokens']} observed input tokens and {c['output_tokens']} output tokens, {c['request_wall_seconds']:.3f} request wall seconds. External spending is USD 0. All prefix, classical and original LLM costs remain part of historical research collection. The full intended ablation costs 300 new acquisitions and 15 real model calls; each new continuation has logical budget 20 including its shared prefix.

Verification passed: deterministic proposal/projection replay, source labels, inclusive 20-label budgets, original prefix hashes, development-only allocation, model/token evidence for any executed requests, and prior scientific freezes. Tests actually ran: **{tests}**. Fifteen additional real-tokenizer traversals were synthetic syntax checks, not model inference or research outcomes.\n
The ledger is **{l['requests']}/{authorization['request_cap']} requests used**, with {1800-l['experiment_seconds']:.3f} seconds remaining under the unchanged 1800-second runtime limit. The user explicitly approved cap 100 → 113 with the reply `approve`, granting 13 additional attempts beyond the two then remaining. The authorization and preflight are snapshotted in `results/v7/authorization_at_inference_start.json`. No paid inference, new weights, cloud or runtime-limit increase was used. `configs/authorization_v7.json` records the approval.\n
The scientific protocol and 97 code/input files were frozen before the new controls in `reports/protocol_v7.freeze.json`. Raw acquired labels and branch states are in `results/v7/`; all 30 intended new branch slots remain in `progress.json`. `artifacts/study_v7/` holds tests, tokenizer checks, actual commands, blocked preflight and verification. Source snapshots and versioned cached baselines support reproducibility; no old results were overwritten.\n
Remaining limits: only three development families; no new test data; small constrained model; binary empirical feature tables; single-target quality tradeoffs; retrospective/adaptive choice of this ablation following v6. Valid novel syntax may still project to configurations selected mainly by geometry. A positive development result would require a frozen follow-up on genuinely untouched families.\n
```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 preflight
# Completed cases are reused; no automatic repeat or new allowance:
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 llm
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
.venv/bin/python scripts/diagnose_v7.py
.venv/bin/python scripts/report_v7.py
```

The most important next experiment is a development-only comparison of selecting existing unevaluated candidate rows against generating new feature strings, with a matched random-selection control. This would separate model ranking from nearest-row projection. It is not implemented or run here, and new model calls require new explicit allowance because the approved 113 attempts are exhausted. A stronger model and untouched-system generalization remain untested.\n\nNo background job is left running. No paper, email, remote push or publication occurred.
'''
    Path('reports/pilot_report_v7.md').write_text(report);print('Wrote v7 report; full ablation complete:',complete)
if __name__=='__main__':main()
