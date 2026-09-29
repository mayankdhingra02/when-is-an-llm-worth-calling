"""Regenerate descriptive Redis evidence; no inference or new outcome access."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'artifacts/.mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read(p):return json.loads(p.read_text())
def main():
    out=ROOT/'results/v61_redis_screen';s=read(out/'summary.json');p=read(ROOT/'results/v61_redis_physical/summary.json');v=read(ROOT/'artifacts/study_v61/verification.json');assert v['verified']
    rows=[];fig,axes=plt.subplots(1,2,figsize=(11,4.8))
    for ax,w in zip(axes,s['workloads']):
        table=read(out/('redis_'+w['workload'])/'table.json')
        with (out/('redis_'+w['workload'])/'settings.csv').open('w') as f:
            writer=csv.writer(f);writer.writerow(['id','configuration','median_ms','cv','valid_repetitions'])
            for t in table:writer.writerow([t['config_id'],json.dumps(t['configuration']),t['median_ms'],t['cv'],t['valid_repetitions']])
        counts={m:sum(c['best_ms'][m]==w['minimum_ms'] for c in w['cases']) for m in ['random','nn','rf_lcb']}
        for m,label,marker in [('random','Random','o'),('nn','3NN','s'),('rf_lcb','RF-LCB (primary)','^')]:
            vals=[100*(c['best_ms'][m]-w['minimum_ms'])/c['best_ms'][m] for c in w['cases']]
            ax.plot(range(5),vals,marker=marker,label=label)
        ax.axhline(w['threshold_percent'],color='brown',ls=':',label='Frozen threshold')
        ax.set(title=w['workload'],xticks=range(5),xticklabels=[c['seed'] for c in w['cases']],xlabel='Seed (one family)',ylabel='Remaining recorded headroom (%)');ax.legend(fontsize=8)
        cvs=[t['cv'] for t in table if t['valid_repetitions']==3]
        rows.append({**w,'median_valid_cv_percent':100*statistics.median(cvs),'exact_minimum_counts':counts,'max_rf_headroom_percent':max(c['primary_rf_headroom_percent'] for c in w['cases'])})
    fig.suptitle('Redis: the preselected RF-LCB comparator leaves little opportunity')
    fig.text(.5,.01,'80 configurations, three physical repetitions, 20 outcomes per arm; generated development workloads on one host.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.045,1,.94));fig.savefig(out/'headroom.png',dpi=160);fig.savefig(out/'headroom.svg');plt.close(fig)
    (out/'descriptive_summary.json').write_text(json.dumps(rows,indent=2)+'\n')
    tab='\n'.join(f"| {w['workload']} | {w['minimum_ms']:.3f} | {w['median_valid_cv_percent']:.3f}% | {w['threshold_percent']:.3f}% | {w['exact_minimum_counts']['rf_lcb']}/5 | {w['max_rf_headroom_percent']:.3f}% | {w['gate_case_count']}/5 |" for w in rows)
    report=f'''# V60/V61 — correctness-checked Redis development result

**The preselected RF-LCB continuation reaches the recorded minimum in 9/10 cases;
its largest remaining gap is 0.068%. Neither workload passes the frozen opportunity
gate. No LLM calls are justified on this grid under this protocol.** This extends
the classical evidence to a new software family; it is not a new model experiment,
independent-family router validation, equivalence proof, or journal-readiness claim.

## What actually ran

Six feasibility invocations passed, followed by all 480 intended grid invocations,
all valid with no retries, resource failures or unattempted cases. Physical grid
collection took {p['stage_seconds']:.6f} seconds under its 900-second cap. Two generated
read workloads, 80 configurations each, three repetitions; all belong to Redis.
Thirty classical arms ran with five fixed seeds, saved shared prefixes of 10,
20 inclusive outcomes per arm, and 400 charged recorded aggregate accesses.
Offline selection took {s['runtime_seconds']:.6f} seconds. Primary RF-LCB was specified
before grid timings; random and 3NN are reported controls. Full-table scoring came
only after all decisions. The portfolio is diagnostic only and not the primary gate.

| Workload | Best median ms | Median CV | Threshold | RF exact minimum | Max RF headroom | Gate cases |
|---|---:|---:|---:|---:|---:|---:|
{tab}

![Preselected comparator](../results/v61_redis_screen/headroom.png)

## Correctness, provenance and costs

Redis 7.2.11 was compiled from owner commit
`d4c381df7a729c06a5207c4f18d804febe956dc4`, with project-local binaries, libc,
and the installed macOS 15.5 SDK. The source tarball and all binary hashes are
saved. The existing user Redis 8.2.3 was queried for its version only, not used.
[Owner release README](https://github.com/redis/redis/blob/d4c381df7a729c06a5207c4f18d804febe956dc4/README.md)
and [COPYING](https://github.com/redis/redis/blob/d4c381df7a729c06a5207c4f18d804febe956dc4/COPYING)
provide build and BSD-3 source-license evidence. No system service was installed.

The volatile-cache contract fixes persistence off, no replication, no eviction,
private Unix sockets, and a 256 MiB server memory ceiling. It does not represent
a durable database service. Each trial loads 256 hashes with 128 field-specific
64-byte values; complete contents are checked before and after execution. The
owner C benchmark is adapted to validate every non-prefix reply before counting it.
All {v['validated_benchmark_replies']:,} benchmark replies (including warmups) passed.
Original C source, exact patch, adapted binary, request counts and logs are retained.
Four separate synthetic native-client fixtures accept correct bytes and reject
wrong bytes, nil and wrong types with exit42; none enters research aggregates.

The client uses 50 connections and pipeline16, avoiding the simple synchronous
single-client measurement problem described in [Redis benchmark guidance](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/).
Nevertheless results describe this client/server/Unix-socket setup. They are not
production throughput or server-only time. Fixed warmup10000 and measured100000
requests per trial; V61 times process exit with a dedicated waiter, including client
startup and reply validation. V60 used Python timeout waiting, which can quantize
short runtimes; its feasibility timings are not pooled into V61 medians.

Actual new research cost is 486 physical server invocations, 400 recorded accesses,
all warmups, data loading and correctness checks. Full-grid table collection is
research overhead. A hypothetical deployed 20-outcome arm would require 60 physical
trials under the median-of-three recipe, plus setup/admission cost. No new model
requests or external spend; hardware, electricity and agent/user costs are unknown.
Peak sampled worker/server/client RSS was {v['max_sampled_rss_bytes']:,} bytes.
The RSS watchdog is sampled, not a hard OS bound; Redis's memory option does not
cap all process overhead. All dedicated servers were shut down with exit0.

## Verification and limits

Independent replay checked all frozen hashes, 486 physical receipts, known-answer
data hashes, every recorded benchmark count, configurations, timing derivation,
400 source labels, 30 arm budgets/prefixes, and 360 reconstructed classical choices.
All 393 Python tests pass. The figure was visually reviewed. Native-client synthetic
controls are stored separately under artifacts/synthetic_v61_reply_guard/.

One new software family, two generated HGET workloads, one host, tiny in-memory
working set, client overhead, three repetitions and noisy recorded minima limit
external validity. Parameter settings may share execution mechanisms; the 80 rows
are not 80 independent mechanisms. No formal significance or equivalence claim.
These short read workloads do not establish results for durable writes, large
working sets, other request mixes, networks or models. Redis is now development;
all related versions/tasks/seeds must remain grouped in future splits.

An identifier audit scanned 5,556 saved research JSON/JSONL/manifests (78,536,465
bytes). Matches were confined to admission/manifests and new Redis feasibility;
no unexplained historical matches. This is not proof of untouched outcomes: deleted,
external, unidentified-alias and unstructured records remain blind spots. Original
MongoDB/Storm tables remain reserved and semantically unadmitted.

## Reproduction and next decision

Raw logs and full denominators: results/v60_redis_feasibility/ and
results/v61_redis_physical/. Tables/prefixes/arms/journals/CSV/figures:
results/v61_redis_screen/. Build/source/verification receipts: artifacts/study_v60/
and artifacts/study_v61/. Frozen protocols and executable source are retained.

```sh
.venv/bin/python scripts/verify_redis_v61.py
.venv/bin/python scripts/report_redis_v61.py
.venv/bin/python -m pytest -q tests
```

Collectors and primary analysis are one-shot; do not delete to rerun or retune this
exposed grid. The next independent-family design should target application decisions
with materially expensive outcomes and a fixed correctness contract. Passing that
screen would still not prove model benefit. Any fresh LLM allowance requires a
concrete bounded protocol; existing cumulative request count remains 1,976.
'''
    (ROOT/'reports/redis_v60_v61.md').write_text(report)
    print('Generated Redis report and PNG/SVG figure')
if __name__=='__main__':main()
