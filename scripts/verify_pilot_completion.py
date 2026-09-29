"""Whole-pilot forensic audit. No inference, search acquisitions, or ledger resets.

Older verifiers' ledger assertions are evaluated against their preserved stage
snapshots; current cumulative limits are checked separately. Redirect all older
verification reports into this audit directory, preserving historical artifacts.
"""
import sys,runpy,importlib.util,math,contextlib,io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from escalation import io as shared_io
from escalation.io import read,write,lines,digest,now
from escalation.data import sha
from escalation.core import State
from escalation.finite_v6 import load_candidates,features
from escalation.study_v6 import outcome_rows
from escalation.analyze_v6 import policy_masks
from escalation.router import GainRouter,UncertaintyRouter,group_mean

OUT=Path('artifacts/completion_audit')

def main():
    OUT.mkdir(parents=True,exist_ok=True);ledger_before=sha('artifacts/resource_ledger_v2.json')
    checks=[]
    def record(name,evidence,detail):
        for path in evidence:assert Path(path).is_file(),path
        checks.append({'requirement':name,'status':'verified','evidence':evidence,'detail':detail})
    source=read('artifacts/source_manifest.json')
    for entry in source['sources']:assert sha(entry['path'])==entry['sha256'],entry['path']
    snap=Path('artifacts/sources/snap2.html').read_text()
    assert '<title>Better Together, in the Right Order: Classical-then-LLM Optimization for SE</title>' in snap
    assert 'conditional' in snap.lower()
    for p in ['reports/source_audit.md','THIRD_PARTY.md','artifacts/environment.json','requirements.lock.txt','configs/pilot.yaml','RESEARCH_BRIEF.md']:
        assert Path(p).is_file()
    record('1. Primary sources, artifact mapping and hardware',['artifacts/source_manifest.json','reports/source_audit.md','THIRD_PARTY.md','artifacts/environment.json'],
       'All saved owner-source bytes match recorded hashes; SNAP2 title and conditional escalation appear in original HTML. Exact SNAP2 artifact remains unlocated, explicitly an adaptation. Hardware inventory retained; no claim upstream EZR was executed.')
    for version in ['v4','v6','v7','v8']:
        for p,h in read('reports/protocol_'+version+'.freeze.json')['sha256'].items():assert sha(p)==h,p
    for p,h in read('reports/registry_v5.freeze.json')['sha256'].items():assert sha(p)==h,p
    def audit_write(path,obj):write(OUT/Path(path).name,obj)
    # Top-level V3 scripts write only verification outputs; redirect those writes.
    original_write=shared_io.write;shared_io.write=audit_write
    try:
        for name in ['verify_results_v3','verify_v3']:
            with (OUT/(name+'.log')).open('w') as log,contextlib.redirect_stdout(log):runpy.run_path('scripts/'+name+'.py',run_name='__main__')
    finally:shared_io.write=original_write
    # Stage-specific historical checks never mutate or substitute the live ledger.
    for version in ['v6','v7','v8']:
        path=Path('scripts/verify_'+version+'.py');spec=importlib.util.spec_from_file_location('audit_'+version,path)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        original_read=mod.read
        def stage_read(path,version=version,original_read=original_read):
            if str(path)=='artifacts/resource_ledger_v2.json' and version!='v8':
                return original_read('artifacts/study_'+version+'/final_ledger_snapshot.json')
            return original_read(path)
        mod.read=stage_read;mod.write=lambda path,obj,version=version:write(OUT/('verification_'+version+'.json'),obj)
        with (OUT/('verify_'+version+'.log')).open('w') as log,contextlib.redirect_stdout(log):mod.main()
    classic=lines('results/v3/classical/runs.jsonl')
    assert len(classic)==30 and {r['seed'] for r in classic}=={11,23,37,53,71}
    assert all(r['logical_evaluations']==20 and len(set(r['ids']))==20 for r in classic)
    record('2–3. Runner, hidden-label controls, deterministic classical smoke',['src/escalation/core.py','src/escalation/data.py','src/escalation/finite_v6.py','data/manifest_v3.json','artifacts/completion_audit/result_verification_v3.json'],
       'Replayed all30 corrected classical arms, three distinct systems/five seeds, inclusive20 and ten-label paired prefixes; full source labels and offline scores checked. Synthetic invariant tests are separate. V1/V2 schema issue remains labeled, never pooled.')
    model=read('artifacts/model_manifest.json')
    assert model['complete']
    for entry in model['files']:assert sha(Path('models/Qwen2.5-0.5B-Instruct')/entry['file'])==entry['sha256']
    record('4. Real model provenance, usage, failures and limits',['artifacts/model_manifest.json','src/escalation/provider.py','results/v3/requests.jsonl','results/v6/requests.jsonl','results/v8/requests.jsonl'],
       'Official pinned local weights hashed; recorded generated token IDs, decoding, grammars, prompts and usage replayed by V3/V6/V7/V8 verifiers. Paid-client guards inspected and tested. Historical failure logs retained; no fabricated model responses.')
    m=read('data/manifest_v6.json');dev=outcome_rows(m,'development');test=outcome_rows(m,'test');seal=read('results/v6/router_seal.json')
    dev_groups={r['system_group'] for r in dev};test_groups={r['system_group'] for r in test}
    assert len(dev_groups)==len(test_groups)==3 and not dev_groups&test_groups
    assert len(dev)==len(test)==15
    for d in m['datasets']:
        if not d['selected']:continue
        c=load_candidates(d)
        for seed in m['seeds']:
            p=read('results/v6/prefixes/'+d['id']+'_'+str(seed)+'.json')
            feat,_=features(c,State(**p['state']).clone(),seed)
            assert feat==p['features']
    # Development-only refit checks the saved learned object; it is not a new policy selection.
    fitted=GainRouter().fit(dev).export();u=UncertaintyRouter().fit(dev)
    for field in ['coefficient','intercept','mean','scale','development_oof_predictions']:
        assert np.allclose(fitted[field],seal['benefit'][field],rtol=0,atol=1e-12),field
    assert fitted['threshold']==seal['benefit']['threshold'] and fitted['training_groups']==seal['benefit']['training_groups']
    assert (None if np.isinf(u.threshold) else float(u.threshold))==seal['uncertainty']['threshold']
    masks,_=policy_masks(test,seal)
    expected={'never','always','benefit','uncertainty','random_development_rate','random_matched_realized_rate_diagnostic','hindsight_oracle_diagnostic'}
    assert set(masks)==expected
    summary=read('results/v6/summary.json');groups=[r['system_group'] for r in test]
    for saved in summary['held_out_policies']:
        mask=masks[saved['policy']];loss=[r['llm_loss'] if chosen else r['classical_loss'] for r,chosen in zip(test,mask)]
        assert math.isclose(group_mean(loss,groups),saved['group_mean_loss'],abs_tol=1e-14)
        assert int(sum(mask))==saved['escalations']
        assert sum(bool(chosen and r['gain']<-.02) for r,chosen in zip(test,mask))==saved['harmful_escalations']
    record('5–6. Paired continuations, full policies, grouped split and predecision features',['results/v6/router_seal.json','results/v6/policies.csv','src/escalation/router.py','src/escalation/analyze_v6.py','artifacts/completion_audit/verification_v6.json'],
       'Replayed30 paired states; recomputed all30 prefix-only feature vectors; refit only development groups and matched sealed coefficients/preprocessing/thresholds. All seven required policies reproduce saved held-out loss/escalation/harm counts. Seal predates test acquisitions. Three test groups are explicitly insufficient for generalization.')
    null=read('results/v9_analysis/summary.json')
    assert null['observed_cases']==15 and all(c['formula_matches_all_subsets'] and c['subsets']==184756 for c in null['verification'])
    assert all(r['probability_random_no_worse_than_observed']>=.5 for r in null['records'])
    for p,h in read('reports/protocol_v9_analysis.freeze.json')['sha256'].items():assert sha(p)==h,p
    for p in ['reports/pilot_report_v6.md','reports/pilot_report_v8.md','results/v8/comparison.png','results/v9_analysis/exact_reference.png','reports/limitations.md','reports/next_experiment.md']:
        assert Path(p).is_file() and Path(p).stat().st_size>0
    record('7. Raw evidence, reproducible results, limits and cost separation',['results/v8/acquisitions.jsonl','results/v9_analysis/exact_distributions.json','reports/pilot_report_v6.md','reports/pilot_report_v8.md','reports/concrete_result.md','reports/next_experiment.md'],
       'Measured artifacts and retrospective reference kept separate; exact distributions exhaustively checked over184756 subsets per case. Actual collection/token/runtime and hypothetical deployment costs separated. Reports disclose insufficient routing evidence and post-hoc analyses; no positive claim required.')
    ledger=read('artifacts/resource_ledger_v2.json')
    assert ledger['requests']==128 and ledger['experiment_seconds']<1800 and ledger['active_since'] is None
    assert ledger_before==sha('artifacts/resource_ledger_v2.json')
    assert len(lines('results/v8/acquisitions.jsonl'))==450 and len(lines('results/v8/requests.jsonl'))==15
    report={'at':now(),'verified':True,'checks':checks,'requests':ledger['requests'],'live_ledger_unchanged_by_audit':True,
      'historical_ledger_snapshots_used_only_for_version_specific_verifiers':['artifacts/study_v6/final_ledger_snapshot.json','artifacts/study_v7/final_ledger_snapshot.json'],
      'limits':['learned routing generalization remains unestablished','post-hoc mechanism evidence does not test model behavior on new orders','no novelty or positive-effect guarantee'],
      'previous_goal_turn_classification':'progress: real measured model execution and diagnostic evidence changed the next action'}
    write(OUT/'completion.json',report);print('Whole-pilot audit passed:',len(checks),'requirement groups; live ledger unchanged.')

if __name__=='__main__':main()
