"""Post-collection evidence audit. Does not acquire objectives or invoke models."""
import csv,hashlib,json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.resources import Resources

def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,v):(ROOT/p).write_text(json.dumps(v,indent=2)+'\n')
def main():
    before=read('artifacts/resource_ledger_v2.json')
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Audit allowance unavailable')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        freezes=[]
        for p in sorted((ROOT/'reports').glob('*.freeze.json')):
            hashes=json.loads(p.read_text()).get('sha256',{})
            for name,h in hashes.items():assert sha(name)==h,(p,name)
            freezes.append({'path':str(p.relative_to(ROOT)),'references':len(hashes)})
        physical=lines('results/v17_measurements/trials.jsonl')
        charges=lines('results/v17_measurements/acquisitions.jsonl')
        planned=read('results/v17_measurements/schedule.json')
        assert len(physical)==len(charges)==len(planned)==846
        for p,c,s in zip(physical,charges,planned):
            assert p['status']=='ok' and p['roundtrip_equal'] is True
            assert all(p[k]==c[k]==s[k] for k in ['trial_id','setting','repetition'])
            assert c['charged_physical_vector']==1
            assert sha(p['compressed_path'])==p['compressed_sha256']
            assert (ROOT/p['compressed_path']).stat().st_size==p['compressed_bytes']
        with (ROOT/'results/v17_measurements/configuration_summary.csv').open() as f:rows=list(csv.DictReader(f))
        assert len(rows)==282
        for row in rows:
            actual=[p for p in physical if p['setting']['config_id']==row['config_id']]
            assert len(actual)==3 and row['successful_trials']=='3'
            assert float(row['median_compression_ms'])==statistics.median(p['compression_ns']/1e6 for p in actual)
            assert int(row['compressed_bytes'])==actual[0]['compressed_bytes']
        assert sha('results/v17_measurements/configuration_summary.csv')==read('artifacts/study_v17/recorded_table_binding.json')['sha256']
        lookup=lines('results/v17_classical/acquisitions.jsonl');assert len(lookup)==450 and all(r['charged_recorded_vector']==1 for r in lookup)
        assert read('artifacts/study_v17/verification.json')['verified'] is True
        assert read('results/v17_classical/progress.json')['completed_arms']==30
        assert read('results/v17_classical/summary.json')['new_model_requests']==0
        assert before['requests']==128
        checks={'verified':True,'scope':'Post-collection hash/median/denominator checks; choice replay recorded separately in verification.json; not a new codec rerun', 'physical_payloads_verified':846,'recorded_accesses':450,'freeze_maps':freezes,'freeze_references':sum(f['references'] for f in freezes),'tests_log':'artifacts/study_v17/precollection_tests.log'}
        write('artifacts/study_v17/final_checks.json',checks)
        resource.checkpoint()
    ledger=read('artifacts/resource_ledger_v2.json');assert ledger['requests']==128 and ledger['active_since'] is None
    prior=read('artifacts/study_v17/baseline_ledger.json');downloads=read('artifacts/download_ledger.json')
    accounting={'new_physical_trials':846,'new_recorded_table_accesses':450,'total_physical_trials':1134,'total_recorded_table_accesses':5408,'combined_count_distinct_cost_types':6542,
      'new_model_requests':0,'followup_requests_used':128,'followup_request_cap':128,'historical_attempts_including_initial':228,
      'runtime_before':prior['experiment_seconds'],'runtime_after':ledger['experiment_seconds'],'new_runtime_seconds':ledger['experiment_seconds']-prior['experiment_seconds'],'remaining_runtime_seconds':1800-ledger['experiment_seconds'],
      'new_download_bytes':0,'total_download_bytes':downloads['accounted_bytes'],'model_bytes':downloads['model_bytes'],'external_spend_usd':ledger['external_spend_usd']}
    write('artifacts/study_v17/final_accounting.json',accounting);write('artifacts/study_v17/final_accounting_ledger.json',ledger)
    print(json.dumps(accounting,indent=2))

if __name__=='__main__':main()
