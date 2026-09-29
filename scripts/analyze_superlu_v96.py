"""Zero-acquisition replay and descriptive report of the V96 diagnostic."""
import json, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
from scipy.io import mmread
from escalation.numerical_v94 import linear_certificate
from collect_smollm_v47 import read, write, sha
from superlu_v96_common import jobs, classify

def lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

def main():
    raw = ROOT / 'results/v96_superlu'; out = ROOT / 'results/v96_analysis'
    out.mkdir(exist_ok=True)
    for name, digest in read(ROOT / 'reports/protocol_v96.freeze.json')['sha256'].items():
        assert sha(ROOT / name) == digest, name
    intended = read(raw / 'intended.json'); outcomes = lines(raw / 'outcomes.jsonl')
    charges = lines(raw / 'charges.jsonl'); lifecycle = read(raw / 'lifecycle.json')
    assert intended == jobs() and len(outcomes) == 40
    assert [r['key'] for r in outcomes] == [r['key'] for r in intended]
    assert [r['key'] for r in charges] == [r['key'] for r in outcomes if r['status'] != 'unattempted']
    assert len(charges) == lifecycle['charged_acquisitions'] <= 40
    assert lifecycle['seconds'] <= 300
    a = mmread(ROOT / 'data/native_v94/orsreg_1.mtx').tocsc()
    truth = 1. + (np.arange(a.shape[0]) % 17) / 17.; b = a @ truth
    starts = returns = verified = 0
    checks = []; counts = []
    for row, job in zip(outcomes, intended):
        for key in job: assert row[key] == job[key]
        path = raw / 'evaluations' / (row['key'] + '.json')
        events = lines(path.with_suffix('.attempts.jsonl'))
        if row['status'] == 'unattempted':
            assert not events and not path.exists(); continue
        request = read(raw / 'requests' / (row['key'] + '.json'))
        assert all(request[k] == v for k,v in job.items())
        record = read(path) if path.exists() else None
        assert classify(row['exit_code'],row['guard'],record) == row['status']
        assert events[0]['defaults'] == [20,10]
        begun = [e for e in events if e['status'] == 'started']
        done = [e for e in events if e['status'] == 'returned']
        assert [e['rep'] for e in begun] == list(range(len(begun)))
        assert [e['rep'] for e in done] == list(range(len(done)))
        assert len(done) <= len(begun) <= 3
        starts += len(begun); returns += len(done)
        for event in done:
            rep = event['rep']; vec = path.with_name(path.stem + f'_x{rep}.npy')
            cert = linear_certificate(a,b,np.load(vec,allow_pickle=False),truth)
            assert cert == event['certificate'] and cert['valid']
            checks.append(dict(key=row['key'],rep=rep,certificate=cert,vector_sha256=sha(vec)))
            verified += 1
        if row['status'] == 'valid':
            assert len(done) == 3 and record['measurements'] == [
                {k:e[k] for k in ['rep','seconds','certificate']} for e in done]
    for base in [0,1]:
        for panel in [16,20,21,32]:
            selected = [r for r in outcomes if r['key'].startswith(f'b{base}_') and r['configuration'][3] == panel]
            c = Counter(r['status'] for r in selected)
            counts.append(dict(base=base,panel=panel,intended=len(selected),valid=c['valid'],
                failures=sum(v for k,v in c.items() if k not in ['valid','unattempted']),unattempted=c['unattempted']))
    summary = dict(scope='exploratory reliability diagnosis; no new independent system',
        acquisitions=len(charges),valid=sum(r['status']=='valid' for r in outcomes),
        failures=sum(r['status'] not in ['valid','unattempted'] for r in outcomes),
        physical_starts=starts,physical_returns=returns,started_without_return=starts-returns,
        planned_not_started=3*len(charges)-starts,recertified_vectors=verified,
        lifecycle_seconds=lifecycle['seconds'],counts=counts,
        new_model_requests=0,new_recorded_table_reads=0,source_download_bytes=16060,
        cumulative_download_bytes=9870221104,remaining_download_bytes=867197136)
    write(out / 'summary.json',summary); write(out / 'solution_checks.json',checks)
    table = '\n'.join(f"| {r['base']} | {r['panel']} | {r['valid']}/{r['intended']} | {r['failures']} | {r['unattempted']} |" for r in counts)
    report = f'''# V96: solver reliability diagnosis

**Result:** {summary['valid']}/40 worker acquisitions passed; {summary['failures']}/40 failed.
All failures were at panel size32 in the COLAMD base. Panels16,20,21 had30/30
valid workers. Panel21's successful exits do not establish memory safety.
The original V94 dataset and results are unchanged.

| Base | Panel size | Valid / intended | Failed | Unattempted |
|---|---:|---:|---:|---:|
{table}

Base0: MMD_AT_PLUS_A, pivot.1, relax4. Base1: COLAMD, pivot.01, relax1.
Both were chosen from prior failures before this diagnostic. All other settings,
matrix and RHS were held fixed; five separate processes per condition.
The 40-condition order was frozen with seed96000. Crashed processes were not retried.

The source mechanism is documented in `reports/source_audit_v96.md`:
StatInit allocates21 histogram entries using default panel20/relax10;
the factorization can index this array using a larger supplied panel size.
All40 workers independently read the same defaults from the installed native
binary. The three observed bus errors occurred inside `splu`, as recorded by
faulthandler. This supports the setting-dependent reliability concern, but does
not trace the offending native instruction or prove that every V94 failure has
the same cause. Allocator layout and added diagnostic writes can affect crashes.

The V94 configuration domain therefore includes a source-identified memory-unsafe
path. Its SuperLU timing and failure results must be interpreted as observations
of that exact wrapper/domain, not as a clean solver comparison or a general LLM
reliability estimate. A correct returned numerical solution does not exclude
memory corruption. Do not delete failed or panel32 acquisitions retrospectively:
that changes the optimizer trajectory and cannot reconstruct a safe-domain run.
HiGHS is a separate implementation and is not implicated by this finding.

## Collection and verification

New charged diagnostic configuration acquisitions:40, separate from V94's500.
Physical solves:{starts} starts, {returns} returns; {starts-returns} started without
return, {3*len(charges)-starts} planned but not started. Independently recertified
{verified} saved solution vectors, including any returned before a later worker
failure. Stage wall time:{lifecycle['seconds']:.6f}s. New inference requests0,
recorded-table reads0, external spendUSD0. Downloaded16,060 source bytes.

Raw evidence: `results/v96_superlu/` (intended conditions, pre-launch charges,
requests, per-solve journals, vectors, stderr, exits and lifecycle).
Derived evidence: `results/v96_analysis/summary.json`, `solution_checks.json`.
Protocol: `reports/protocol_v96.md` and immutable SHA256 freeze.

Replay with `.venv/bin/python scripts/analyze_superlu_v96.py`; this reads saved
vectors only and performs no new solver or LLM calls. The collection runner
refuses an existing output directory. For a fresh replication use a separately
declared output workspace and count every acquisition.

## Research consequence

This is useful threat-to-validity evidence, not a positive router finding or
evidence of journal acceptance. The previous negative findings remain saved,
but broad claims based on the affected SuperLU domain should be narrowed.
Next: freeze a new optimization study with a source-justified restricted
SuperLU domain and retain the original study as a sensitivity case; label the
repeat exploratory because the system is now exposed. Independently reproduce
the unaffected HiGHS result on a second machine when available. More independent
systems and useful LLM benefit variation are still needed for the original
benefit-prediction hypothesis.
'''
    (ROOT / 'reports/superlu_v96.md').write_text(report)
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
