"""Standard-library-only reconstruction of V80 outcomes, not a native/model rerun.
Run from an isolated bundle with python -I -S scripts/replay_kanzi_v80_portable.py.
The full scikit-learn decision replay remains scripts/analyze_kanzi_v80.py.
"""
import hashlib,json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=read(ROOT/'portable_manifest.json')
    for n,m in manifest['files'].items():
        p=ROOT/n;assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'],n
    out=ROOT/'results/v80_kanzi_paired';summary=read(out/'summary.json');ledger=read(out/'ledger.json')
    assert summary['complete'] and summary['charged_evaluations']==summary['successful_evaluations']==450 and summary['unattempted']==0
    events=read(out/'acquisitions.json');assert len(events)==450
    bypath={r['path']:r for r in events};assert len(bypath)==450
    workloads=read(ROOT/'artifacts/study_v79/workloads.json')['files'];means={};used=[];requests=[];observed_usage=[];wins={}
    charges=[json.loads(s) for s in (out/'charges.jsonl').read_text().splitlines()];assert len(charges)==450
    for e,charge in zip(events,charges):
        assert all(e[k]==v for k,v in charge.items() if k!='status') and e['status']=='valid'
        r=read(ROOT/e['path']/'result.json');assert r['compressed_bytes']==e['compressed_bytes'] and r['status']=='valid' and r['exact_byte_equality']
        w=next(w for w in workloads if w['name']==e['workload']);assert r['input_sha256']==r['decoded_sha256']==w['sha256'] and r['decoded_bytes']==w['bytes']
        for phase in ['compression','decompression']:assert r[phase]['exit_code']==0 and r[phase]['termination_reason'] is None
    methods=['rf_lcb','preset','llm'];reconstructed=[]
    for w in workloads:
        cases=[]
        for seed in [11,23,37,53,71]:
            case=read(out/f"case_{w['name']}_{seed}.json");prefixpath=ROOT/f"results/v79_kanzi_classical/prefix_{w['name']}_{seed}.json";prefix=read(prefixpath)
            assert len(prefix)==10 and case['prefix_sha256']==sha(prefixpath)
            failed=False;fallback=[];actual_medians={}
            for m in methods:
                obs=case['arms'][m];conf=case['confirmation'][m];assert obs[:10]==prefix and len(obs)==17 and len(conf)==3
                assert len({o['config_id'] for o in obs})==17
                chosen=min(obs,key=lambda o:(o['compressed_bytes'],o['config_id']))['config_id'];assert chosen==case['selected_config_ids'][m]
                assert all(o['config_id']==chosen for o in conf)
                for i,o in enumerate(obs[10:]+conf,11):
                    e=bypath[o['physical_receipt']];assert e['workload']==w['name'] and e['seed']==seed and e['arm']==m and e['ordinal']==i and e['config_id']==o['config_id'] and e['compressed_bytes']==o['compressed_bytes']
                    assert e['purpose']==('search' if i<18 else 'confirmation');used.append(e['path'])
                actual_medians[m]=statistics.median(o['compressed_bytes'] for o in conf)
            for step in range(1,8):
                name=f"v80_{w['name']}_seed{seed}_step{step}"
                if not failed:
                    p=out/name;req=read(p/'request.json');resp=read(p/'response.json');dec=read(p/'decision.json');requests.append(name)
                    assert req['request_id']==name and hashlib.sha256(req['payload']['prompt'].encode()).hexdigest()==req['prompt_sha256']
                    assert req['payload']['seed']==seed and req['payload']['n_predict']==64 and req['payload']['temperature']==0
                    assert dec['usage']=={k:resp.get(k) for k in ['tokens_predicted','tokens_evaluated']};observed_usage.append(dec['usage'])
                    failed=not dec['valid']
                    if not failed:assert dec['selected_id']==case['arms']['llm'][step+9]['config_id']
                if failed:fallback.append(step)
            assert case['fallback_steps']==fallback
            cases.append(actual_medians);reconstructed.append({'workload':w['name'],'seed':seed,'medians':actual_medians})
        means[w['name']]={m:statistics.mean(c[m] for c in cases) for m in methods}
        wins[w['name']]={m:{'wins':sum(c['llm']<c[m] for c in cases),'ties':sum(c['llm']==c[m] for c in cases),'losses':sum(c['llm']>c[m] for c in cases)} for m in methods[:2]}
    assert sorted(used)==sorted(bypath) and len(used)==450
    starts=[json.loads(s)['request_id'] for s in (out/'request_starts.jsonl').read_text().splitlines()];assert starts==requests
    assert len(requests)==ledger['generation_requests']<=105 and ledger['unattempted_generation_requests']==105-len(requests)
    published=read(ROOT/'results/v80_kanzi_analysis/summary.json');assert means==published['mean_seed_median_bytes_by_workload']
    for c in reconstructed:
        pub=next(p for p in published['cases'] if p['workload']==c['workload'] and p['seed']==c['seed'])
        assert c['medians']=={m:pub['arms'][m]['median_bytes'] for m in methods}
    descriptive=read(ROOT/'results/v80_kanzi_analysis/descriptive_summary.json')
    for w,comparisons in wins.items():
        for control,v in comparisons.items():
            assert all(descriptive['comparisons'][w][control][k]==n for k,n in v.items())
            ratio=100*(means[w][control]-means[w]['llm'])/means[w][control]
            assert abs(ratio-descriptive['comparisons'][w][control]['ratio_of_means_saved_pct'])<1e-12
    for k in ['tokens_predicted','tokens_evaluated']:
        assert sum(u[k] for u in observed_usage if u[k] is not None)==published['usage'][k]['observed_sum']
        assert sum(u[k] is None for u in observed_usage)==published['usage'][k]['unknown_requests']
    print(json.dumps({'verified':True,'files':len(manifest['files']),'physical_trials':450,'logical_arm_charges':900,'real_requests_replayed':len(requests),'python':sys.version.split()[0],'means':means,'wins_ties_losses':wins,'limitations':'Standard-library receipt/outcome reconstruction, not full RF decision replay, independent fresh compression, inference, or clean-machine measurement'},indent=2))
if __name__=='__main__':main()
