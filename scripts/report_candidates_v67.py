"""Verified three-system screen, costs and primary opportunity decision."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'artifacts/.mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def read(p):return json.loads(p.read_text())
def main():
    out=ROOT/'results/v67_candidates_screen';s=read(out/'summary.json');physical=read(ROOT/'results/v67_candidates_physical/summary.json')
    verification=read(ROOT/'artifacts/study_v67/verification.json');assert verification['verified']
    fig,axes=plt.subplots(1,3,figsize=(13,4.8));rows=[]
    for ax,w in zip(axes,s['workloads']):
        folder=out/(w['family']+'_fixed');table=read(folder/'table.json')
        with (folder/'settings.csv').open('w',newline='') as stream:
            writer=csv.writer(stream);writer.writerow(['id','configuration','median_penalized_ms','valid_repetitions','cv'])
            for t in table:writer.writerow([t['config_id'],json.dumps(t['configuration']),t['median_ms'],t['valid_repetitions'],t['cv']])
        for method,label,marker in [('random','Random','o'),('nn','3NN','s'),('rf_lcb','RF-LCB (primary)','^')]:
            vals=[100*(c['best_ms'][method]-w['minimum_ms'])/c['best_ms'][method] for c in w['cases']]
            ax.plot(range(5),vals,marker=marker,label=label)
        if w['threshold_percent'] is not None:ax.axhline(w['threshold_percent'],ls=':',color='brown',label='Frozen threshold')
        ax.set(title=w['family'],xlabel='Seed',ylabel='Remaining recorded headroom (%)',xticks=range(5),xticklabels=[c['seed'] for c in w['cases']]);ax.legend(fontsize=7)
        cvs=[t['cv'] for t in table if t['valid_repetitions']==3]
        rows.append({**w,'median_valid_cv_percent':100*statistics.median(cvs) if cvs else None,'valid_physical_trials':sum(t['valid_repetitions'] for t in table),'rf_exact_minimum_cases':sum(c['best_ms']['rf_lcb']==w['minimum_ms'] for c in w['cases']),'nn_exact_minimum_cases':sum(c['best_ms']['nn']==w['minimum_ms'] for c in w['cases']),'prefix_exact_minimum_cases':sum(c['prefix_best_ms']==w['minimum_ms'] for c in w['cases']),'random_exact_minimum_cases':sum(c['best_ms']['random']==w['minimum_ms'] for c in w['cases'])})
    fig.suptitle('Three new development systems: opportunity after 20 classical evaluations')
    fig.text(.5,.01,'One generated workload per system, 48 settings, three physical repetitions. No LLM responses in this screen.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.045,1,.94));fig.savefig(out/'headroom.png',dpi=160);fig.savefig(out/'headroom.svg');plt.close(fig)
    (out/'descriptive_summary.json').write_text(json.dumps(rows,indent=2)+'\n')
    tab='\n'.join(f"| {w['family']} | {w['valid_physical_trials']}/144 | {w['minimum_ms']:.3f} | {w['threshold_percent']:.3f}% | {w['gate_case_count']}/5 | {'pass' if w['gate_passed'] else 'stop'} |" for w in rows)
    eligible=[w['family'] for w in rows if w['gate_passed']]
    decision=('Prepare a separately frozen real-model assay for '+', '.join(eligible)+', including all five seeds per admitted system.') if eligible else 'None passes the frozen gate. Stop model collection on these grids under this protocol.'
    report=f'''# V66/V67 — three-system correctness and opportunity result

**{decision}** This is a screening decision, not demonstrated model benefit.

RF-LCB and3NN each reach the recorded minimum in
{sum(w['rf_exact_minimum_cases'] for w in rows)}/15 and
{sum(w['nn_exact_minimum_cases'] for w in rows)}/15 cases, respectively. The shared
prefix already reaches it in {sum(w['prefix_exact_minimum_cases'] for w in rows)}/15;
random continuation reaches it in {sum(w['random_exact_minimum_cases'] for w in rows)}/15.
Thus this result is not specific to one selected surrogate. These are exact minima
of the measured48-row tables, not proof of the fastest physically possible setting.

All nine admission trials passed independent correctness checks. The full screen
attempted {physical['attempted']}/432 configuration trials, with {physical['valid']} valid and
{physical['resource_noncompletion']} resource noncompletions; {physical['unattempted']} unattempted.
Collection took {physical['stage_seconds']:.3f}s under the1,800s cap. Forty-five classical
arms used600charged recorded acquisitions, five fixed seeds, identical saved
ten-observation prefixes and twenty-inclusive arm budgets. Analysis took
{s['runtime_seconds']:.3f}s. No new model request, output repair or paid spending.

| System | Valid physical trials | Recorded best ms | Frozen threshold | RF gate cases | Decision |
|---|---:|---:|---:|---:|---|
{tab}

![Classical opportunity](../results/v67_candidates_screen/headroom.png)

## Implementation and correctness

DuckDB1.3.2 uses the official PyPI macOS ARM Python3.10 wheel, isolated under the
project runtime; its SHA matches registry metadata. The binary identifies commit
0b83e5d2f6. A fixed integer join/aggregation on2^22 fact rows and4,096dimension rows
must match independently computed sums/counts in all256groups. Objective is first
query execution plus materialization after loading; setup cost is separately
included in actual collection wall time. External access and automatic extension
installation/loading are disabled. Declared variables are threads, memory limit
and perfect-hash threshold. [Pinned owner source](https://github.com/duckdb/duckdb/tree/v1.3.2)
documents the system; live binary settings were inspected without performance queries.

GNU sort9.7 is built from the [owner release](https://ftp.gnu.org/gnu/coreutils/).
One fixed affine permutation of2^20padded integer lines must reproduce the exact
independent sorted-output SHA under LC_ALL=C. Whole native-process time includes
input/output. Parallelism, initial buffer size and merge batch size vary. Source
documentation distinguishes buffer hints from hard memory limits. The owner
signature file is retained but not independently key-verified; HTTPS provenance
and exact artifact/binary hashes are recorded. No system binary was substituted.

OpenJPEG2.5.3 is built from [owner commit210a8a5](https://github.com/uclouvain/openjpeg/tree/210a8a5690d0da66f02d49420d7176a21ef409dc).
Fixed1024x1024 eight-bit generated pixels are losslessly encoded and decoded;
every pixel and shape must match. Objective is whole encoder-process time.
Decoder validation time and compressed size are retained separately. Code-block
size, resolution levels, tile size and threads vary; no irreversible transform,
quality loss or post-hoc size constraint. Optional PNG/TIFF/color dependencies
were disabled for this PGM/J2K task. Algorithm sources were not patched.

Owner licenses: DuckDB MIT, GNU coreutils GPL3+, OpenJPEG BSD2. README/build/source
options were inspected before execution. The initial missing wheel platform tag,
incorrect SDK path and missing GNU generated-header prerequisite were diagnosed
and corrected; failure logs and original build script are preserved. These are
build corrections, not discarded measured trials. Builds remain local; no install
of a system service, remote publication, cloud resource or author contact.

## Interface work and what it does not prove

The new finite-domain proposal interface constructs a grammar containing exactly
the remaining legal full configuration vectors. It removes observed and already
proposed rows before each completion and independently checks returned bytes.
Requests are charged before transport; errors terminate without repair/retry.
Classical policies can receive the same eligible configurations. Ten selections
would require ten generation requests, an explicit extra cost. Synthetic tests
exercise pending requests, caps, failure handling, duplicate domains, numeric
aliases, escaping and100randomized domain traversals. These are synthetic contract
checks, not fabricated model responses, real runtime-grammar validation or evidence
that a model makes useful choices. V65 results remain unchanged.

## Verification, costs and limits

Independent verification reconstructs all432 trial schedules and receipts, retained
answer files, exact sorted outputs, decoded pixels, table medians/CVs,600label
charges and540classical choices. {verification['application_invocations_with_decoder_validation']}
application invocations are represented in the grid, including decoder validation;
admission adds12application invocations for9configuration trials. Python workers,
source downloads, builds and tests are additional overhead, not free evaluations.
Output correctness is checked independently, but timings are source-instrumented
measurements on one host, not externally certified timestamps.

The RF gate was fixed before full-grid outcomes: remaining improvement to recorded
minimum at least max(5%,twice median valid CV percentage) in2/5seeds. Random/3NN
results are reported regardless of their ranking. Hindsight portfolio is diagnostic
only. No significance, equivalence or practical deployment gain is inferred from
this heuristic. A deployment20-outcome arm would require60configuration trials
under the median-of-three recipe; full-table research collection is separate.

Three new development groups, each with one generated workload and three repetitions,
are not sufficient for a generalizable learned-router claim. No production workload,
held-out system evaluation or cross-machine replication was added. The identifier
audit found no matches in7,725saved research JSON/JSONL/manifests but cannot certify
deleted/external/unidentified history. These outcomes are now exposed. Do not tune
failed grids until they pass or describe these results as Q2 readiness.
Each arm evaluates20/48settings (41.7% of the finite domain); this substantial
coverage and the regular low-dimensional grids limit conclusions about larger,
irregular configuration spaces. Three repetitions do not identify noise-free
physical optima, and the query/encoding/ordering jobs are short on this host.

Raw results: results/v66_candidate_feasibility/ and results/v67_candidates_physical/.
Tables, prefixes, arms, ledgers, CSV and figures: results/v67_candidates_screen/.
Protocols, freezes, sources/builds and independent verification receipts are saved.

```sh
.venv/bin/python scripts/verify_candidates_v66.py
.venv/bin/python scripts/verify_candidates_v67.py
.venv/bin/python scripts/report_candidates_v67.py
```

{decision} No inference allowance follows automatically from this screen.
'''
    (ROOT/'reports/candidates_v66_v67.md').write_text(report);print(decision)
if __name__=='__main__':main()
