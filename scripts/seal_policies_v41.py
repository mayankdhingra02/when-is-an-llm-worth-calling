"""Commit controller decisions using saved predecision features, before new LLMs."""
import hashlib, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,digest,now
from escalation.policy_transfer_v41 import predecision_masks
from escalation.transfer_v41 import current_config
from escalation.resources import Resources
from run_transfer_v41 import verify_freeze

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    out=Path('results/v41_policy_precommit')
    if out.exists() or Path('results/v41_models').exists():raise ValueError('Commit once before any V41 model attempt')
    verify_freeze();seal=read('results/v6/router_seal.json')
    if sha('results/v6/router_seal.json')!=read('results/v6/router_seal.sha256.json')['sha256']:raise ValueError('Changed old controller')
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        resource.check();manifest=read('data/manifest_v41.json');source_hashes={};rows=[]
        frozen=read('results/v41_transfer/collection_seal.json')['sha256']
        for d in manifest['datasets']:
            for seed in manifest['seeds']:
                path=f"results/v41_transfer/prefixes/{d['id']}_{seed}.json"
                if sha(path)!=frozen[path]:raise ValueError('Changed prefix')
                source_hashes[path]=frozen[path];p=read(path)
                rows.append({k:p[k] for k in ('dataset','seed','system_group','features')})
        masks,scores=predecision_masks(rows,seal)
        training=read('results/v6/development_outcomes.json')
        if digest(training)!=seal['development_rows_sha256']:raise ValueError('Changed development data')
        ranges={k:[min(r['features'][k] for r in training),max(r['features'][k] for r in training)] for k in seal['benefit']['features']}
        shift=[{'dataset':row['dataset'],'seed':row['seed'],
                'outside_development_range':[k for k,(lo,hi) in ranges.items() if not lo <= row['features'][k] <= hi]}
               for row in rows]
        result={'at':now(),'namespace':'measured_predecision_only_v41','rows':rows,'masks':masks,'benefit_scores':scores,
            'source_hashes':source_hashes,'controller_sha256':sha('results/v6/router_seal.json'),
            'development_sha256':sha('results/v6/development_outcomes.json'),
            'calls_if_deployed_per_model':{k:sum(v) for k,v in masks.items()},
            'development_feature_ranges':ranges,'feature_shift':shift,
            'classical_outcomes_previously_inspected':True,'new_llm_outcomes_used':False,
            'qualification':'No threshold refit. Scores use the old normalized-loss target, not calibrated V41 relative gains. Shift descriptions do not alter masks. Not LLM performance evidence.'}
        write(out/'decisions.json',result)
        paths=['src/escalation/policy_transfer_v41.py','scripts/seal_policies_v41.py','scripts/analyze_models_v41.py',
               'tests/synthetic/test_policy_transfer_v41.py','reports/analysis_addendum_v41.md',str(out/'decisions.json')]
        write(out/'analysis_seal.json',{'at':now(),'phase':'after classical outcomes, before any new-model inference',
              'original_protocol_freeze_sha256':sha('reports/protocol_v41_transfer.freeze.json'),
              'sha256':{p:sha(p) for p in paths}})
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/policy_precommit_accounting.json',{'seconds':after['experiment_seconds']-before['experiment_seconds'],
          'new_requests':after['requests']-before['requests'],'new_objective_acquisitions':0})
    print(__import__('json').dumps({'calls_per_model':result['calls_if_deployed_per_model'],
          'cases_outside_training_range':sum(bool(r['outside_development_range']) for r in shift)},indent=2))

if __name__=='__main__':main()
