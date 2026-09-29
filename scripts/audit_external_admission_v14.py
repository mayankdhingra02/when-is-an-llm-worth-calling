"""Replay pinned external configuration coverage; no upstream code execution."""
import hashlib
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.external_admission_v14 import coverage_audit, metadata_rows


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ledger=ROOT/'artifacts/resource_ledger_v2.json';before=digest(ledger)
    freeze=json.loads((ROOT/'reports/protocol_v14_external_admission.freeze.json').read_text())
    for name,expected in freeze['sha256'].items():assert digest(ROOT/name)==expected,name
    base=ROOT/'artifacts/sources/admission_v14/nk2242696__compression-codec-benchmark/docs/results/standard-2026-07'
    manifest=json.loads((base/'manifest.json').read_text())
    with (base/'raw.csv').open(newline='') as handle:
        result=coverage_audit(metadata_rows(handle),manifest)
    assert result['raw_rows']==540 and result['measured_rows']==450 and result['warmup_rows']==90
    assert result['contexts']==90 and result['datasets']==15 and len(result['codecs'])==6
    assert all(r['distinct_measured_configurations']==1 for r in result['records'])
    assert all(r['repetitions_per_measured_configuration']==[5] for r in result['records'])
    assert result['contexts_supporting_budget']==0
    assert not result['clean_execution_revision_identified']
    assert digest(ledger)==before
    out=ROOT/'results/v14_external_admission';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    verification={'verified':True,'frozen_files':len(freeze['sha256']),
                  'raw_rows':result['raw_rows'],'measured_rows':result['measured_rows'],
                  'warmup_rows':result['warmup_rows'],'contexts':result['contexts'],
                  'contexts_supporting_budget_20':0,'metrics_converted_or_aggregated':False,
                  'ledger_unchanged_sha256':before,'new_model_calls':0,'new_optimizer_acquisitions':0}
    (ROOT/'artifacts/study_v14/verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    print(json.dumps(verification,indent=2))


if __name__=='__main__':main()
