"""Receipt/decision replay and descriptive analysis; launches no application."""
import csv,hashlib,json,os,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid,features,choose,SEEDS,METHODS
from escalation.kanzi_v74 import parse_header,verify_settings
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def verify():
    for n,d in read(ROOT/'reports/protocol_v77.freeze.json')['sha256'].items():assert sha(ROOT/n)==d,n
    out=ROOT/'results/v77_kanzi_classical';summary=read(out/'summary.json');events=read(out/'acquisitions.json')
    charges=[json.loads(s) for s in (out/'charges.jsonl').read_text().splitlines()]
    assert summary['complete'] and summary['charged_evaluations']==summary['successful_evaluations']==len(events)==len(charges)==200
    assert summary['seconds']<=1800 and summary['new_model_requests']==0
    configs=grid();x=features(configs);data=ROOT/'data/generated_v74/workload.bin';digest=sha(data)
    for i,row in enumerate(events):
        assert row['event_id']==i and all(row[k]==v for k,v in charges[i].items() if k!='status')
        folder=ROOT/row['path'];assert row==read(folder/'result.json')
        assert row['config']==configs[row['config_id']] and row['status']=='valid'
        assert row['exact_byte_equality'] and row['decoded_sha256']==row['input_sha256']==digest and row['decoded_bytes']==data.stat().st_size
        header=parse_header(bytes.fromhex(row['header_hex']));assert header==row['stream_header'];verify_settings(header,row['config'],(folder/'compression.log').read_text())
        for phase in ['compression','decompression']:
            receipt=row[phase];assert receipt['exit_code']==0 and receipt['termination_reason'] is None and receipt['wall_seconds']<=40
            assert receipt['sampled_maxima']['rss_bytes']<=2*1024**3 and receipt['sampled_maxima']['scratch_bytes']<=128*1024**2
        assert read(folder/'retention.json')['removed_after_validation']==['output.knz','decoded.bin']
        assert not (folder/'output.knz').exists() and not (folder/'decoded.bin').exists()
    def check_observation(o,seed,arm,ordinal,purpose):
        r=events[o['event_id']]
        assert r['seed']==seed and r['arm']==arm and r['ordinal']==ordinal and r['purpose']==purpose
        assert r['config_id']==o['config_id'] and r['compressed_bytes']==o['compressed_bytes']
    cases=[];used=[]
    for seed in SEEDS:
        case=read(out/f'case_{seed}.json');assert case==next(c for c in summary['cases'] if c['seed']==seed)
        prefix=read(out/f'prefix_{seed}.json');assert len(prefix)==10 and sha(out/f'prefix_{seed}.json')==case['prefix_sha256']
        initial=random.Random(seed).sample(range(448),4)
        for j,o in enumerate(prefix):
            cid=initial[j] if j<4 else choose(x,prefix[:j],'nn',seed)
            assert o['config_id']==cid;check_observation(o,seed,'prefix',j+1,'search');used.append(o['event_id'])
        best=min(o['compressed_bytes'] for o in prefix);arm_results={}
        for method in METHODS:
            obs=case['arms'][method];assert len(obs)==17 and obs[:10]==prefix
            assert len({o['config_id'] for o in obs})==17
            rng=random.Random(seed+1000)
            for j in range(10,17):
                assert obs[j]['config_id']==choose(x,obs[:j],method,seed,rng)
                decision=next(d for d in case['decisions'] if d['method']==method and d['step']==j-10)
                assert decision['config_id']==obs[j]['config_id'] and decision['observed_events']==[o['event_id'] for o in obs[:j]]
                check_observation(obs[j],seed,method,j+1,'search');used.append(obs[j]['event_id'])
            selected=min(obs,key=lambda o:(o['compressed_bytes'],o['config_id']))['config_id'];assert case['selected_config_ids'][method]==selected
            confirmation=case['confirmation'][method];assert len(confirmation)==3 and len(obs)+len(confirmation)==20
            for j,o in enumerate(confirmation):
                assert o['config_id']==selected;check_observation(o,seed,method,j+18,'confirmation');used.append(o['event_id'])
            values=[o['compressed_bytes'] for o in confirmation];median=statistics.median(values)
            arm_results[method]={'config_id':selected,'confirmation_bytes':values,'confirmed_median_bytes':median,
                'prefix_best_bytes':best,'size_reduction_vs_prefix_pct':100*(best-median)/best,
                'confirmation_bytes_all_equal':len(set(values))==1,
                'decision_seconds':sum(d['seconds'] for d in case['decisions'] if d['method']==method)}
        # Verify the frozen randomized round order through the actual event IDs.
        order_rng=random.Random(seed+75000);expected=[]
        for step in range(7):
            order=list(METHODS);order_rng.shuffle(order)
            expected.extend(case['arms'][m][step+10]['event_id'] for m in order)
        for rep in range(3):
            order=list(METHODS);order_rng.shuffle(order)
            expected.extend(case['confirmation'][m][rep]['event_id'] for m in order)
        assert expected==sorted(expected)
        cases.append({'seed':seed,'arms':arm_results})
    assert sorted(used)==list(range(200))
    result={'complete':True,'physical_evaluations':200,'logical_arm_charges':300,'families':1,'cases':cases,
        'mean_of_seed_medians_bytes':{m:statistics.mean(c['arms'][m]['confirmed_median_bytes'] for c in cases) for m in METHODS},
        'wins_ties_losses_vs_random':{m:{label:sum((c['arms'][m]['confirmed_median_bytes']<c['arms']['random']['confirmed_median_bytes'] if label=='wins' else c['arms'][m]['confirmed_median_bytes']==c['arms']['random']['confirmed_median_bytes'] if label=='ties' else c['arms'][m]['confirmed_median_bytes']>c['arms']['random']['confirmed_median_bytes']) for c in cases) for label in ['wins','ties','losses']} for m in ['nn','rf_lcb']},
        'unique_sampled_configurations':len({r['config_id'] for r in events}),
        'unique_observed_byte_counts':len({r['compressed_bytes'] for r in events}),
        'unique_observed_compressed_hashes':len({r['compressed_sha256'] for r in events}),
        'stage_seconds':summary['seconds'],'application_process_seconds':sum(r[p]['wall_seconds'] for r in events for p in ['compression','decompression']),
        'peak_sampled_rss_bytes':max(r[p]['sampled_maxima']['rss_bytes'] for r in events for p in ['compression','decompression']),
        'limitations':'Development, generated input, one family, 448 canonical candidates not certified effective behaviors; deleted products verified only by retained receipts; no model calls'}
    return result
def main():
    result=verify();out=ROOT/'results/v77_kanzi_analysis';out.mkdir(exist_ok=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    rows=[{'seed':c['seed'],'method':m,**{k:v for k,v in a.items() if k!='confirmation_bytes'}} for c in result['cases'] for m,a in c['arms'].items()]
    with (out/'cases.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    cache=ROOT/'.cache/kanzi-v77-plot';cache.mkdir(parents=True,exist_ok=True);os.environ.setdefault('MPLCONFIGDIR',str(cache));os.environ.setdefault('XDG_CACHE_HOME',str(cache))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
    for m,marker in zip(METHODS,['o','s','^']):ax.plot(SEEDS,[c['arms'][m]['confirmed_median_bytes']/1024**2 for c in result['cases']],marker=marker,label=m)
    ax.set_xticks(SEEDS);ax.set_xlabel('Seed (one software family)');ax.set_ylabel('Confirmed compressed MiB — lower is better');ax.legend();ax.spines[['top','right']].set_visible(False)
    ax.set_title('Kanzi buffer-fix adaptation: 20 evaluations per arm, shared prefix of 10\nGenerated 16 MiB input; classical policies only')
    fig.savefig(out/'classical.png',dpi=160);fig.savefig(out/'classical.svg');plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
