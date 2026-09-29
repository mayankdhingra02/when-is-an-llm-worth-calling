"""Receipt/decision replay and descriptive analysis; launches no application."""
import csv,hashlib,json,os,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid,features,SEEDS
from escalation.kanzi_v79 import choose,METHODS
from escalation.kanzi_v74 import parse_header,verify_settings
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def verify():
    for n,d in read(ROOT/'reports/protocol_v79.freeze.json')['sha256'].items():assert sha(ROOT/n)==d,n
    out=ROOT/'results/v79_kanzi_classical';summary=read(out/'summary.json');events=read(out/'acquisitions.json')
    charges=[json.loads(s) for s in (out/'charges.jsonl').read_text().splitlines()]
    assert summary['complete'] and summary['charged_evaluations']==summary['successful_evaluations']==len(events)==len(charges)==450
    assert summary['seconds']<=1800 and summary['new_model_requests']==0
    configs=grid();x=features(configs);workloads=read(ROOT/'artifacts/study_v79/workloads.json')['files'];byname={w['name']:w for w in workloads}
    for i,row in enumerate(events):
        assert row['event_id']==i and all(row[k]==v for k,v in charges[i].items() if k!='status')
        data=ROOT/byname[row['workload']]['path'];digest=byname[row['workload']]['sha256']
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
        assert r['workload']==workload and r['seed']==seed and r['arm']==arm and r['ordinal']==ordinal and r['purpose']==purpose
        assert r['config_id']==o['config_id'] and r['compressed_bytes']==o['compressed_bytes']
    cases=[];used=[]
    for entry in workloads:
        workload=entry['name']
        for seed in SEEDS:
            case=read(out/f'case_{workload}_{seed}.json');assert case==next(c for c in summary['cases'] if c['seed']==seed and c['workload']==workload)
            prefix=read(out/f'prefix_{workload}_{seed}.json');assert len(prefix)==10 and sha(out/f'prefix_{workload}_{seed}.json')==case['prefix_sha256']
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
            order_rng=random.Random(seed+79000);expected=[]
            for step in range(7):
                order=list(METHODS);order_rng.shuffle(order)
                expected.extend(case['arms'][m][step+10]['event_id'] for m in order)
            for rep in range(3):
                order=list(METHODS);order_rng.shuffle(order)
                expected.extend(case['confirmation'][m][rep]['event_id'] for m in order)
            assert expected==sorted(expected)
            cases.append({'workload':workload,'seed':seed,'arms':arm_results})
    assert sorted(used)==list(range(450))
    groups={}
    for entry in workloads:
        subset=[c for c in cases if c['workload']==entry['name']]
        means={m:statistics.mean(c['arms'][m]['confirmed_median_bytes'] for c in subset) for m in METHODS}
        differences=[c['arms']['rf_lcb']['confirmed_median_bytes']-c['arms']['preset']['confirmed_median_bytes'] for c in subset]
        groups[entry['name']]={'mean_bytes':means,'preset_saved_pct_ratio_of_means':100*(means['rf_lcb']-means['preset'])/means['rf_lcb'],
            'preset_wins':sum(d>0 for d in differences),'ties':sum(d==0 for d in differences),'preset_losses':sum(d<0 for d in differences)}
    return {'verified':True,'physical_evaluations':450,'logical_arm_charges':600,'families':1,'workloads':groups,'cases':cases,
        'stage_seconds':summary['seconds'],'new_model_requests':0,
        'application_process_seconds':sum(r[p]['wall_seconds'] for r in events for p in ['compression','decompression']),
        'peak_sampled_rss_bytes':max(r[p]['sampled_maxima']['rss_bytes'] for r in events for p in ['compression','decompression']),
        'all_confirmation_bytes_equal':all(a['confirmation_bytes_all_equal'] for c in cases for a in c['arms'].values()),
        'limitations':'Prospective new-workload classical comparison; V78-informed preset; one exposed development family; no LLM counterfactual or learned router; receipt replay after validated payload removal'}

def main():
    result=verify();out=ROOT/'results/v79_kanzi_analysis';out.mkdir(exist_ok=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    rows=[{'workload':c['workload'],'seed':c['seed'],'method':m,**{k:v for k,v in a.items() if k!='confirmation_bytes'}} for c in result['cases'] for m,a in c['arms'].items()]
    with (out/'cases.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    cache=ROOT/'.cache/kanzi-v79-plot';cache.mkdir(parents=True,exist_ok=True);os.environ.setdefault('MPLCONFIGDIR',str(cache));os.environ.setdefault('XDG_CACHE_HOME',str(cache))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    for ax,(name,g) in zip(axes,result['workloads'].items()):
        subset=[c for c in result['cases'] if c['workload']==name]
        for m,marker in zip(METHODS,['o','s']):
            ax.plot(range(5),[c['arms'][m]['confirmed_median_bytes']/1024**2 for c in subset],marker=marker,label=m)
        ax.set_xticks(range(5),SEEDS);ax.set_xlabel('Search seed');ax.set_title(name);ax.spines[['top','right']].set_visible(False)
    axes[0].set_ylabel('Confirmed compressed MiB (lower is better)');axes[0].legend()
    fig.suptitle('Kanzi adaptation: preset strategy versus RF on three Silesia files\n20 evaluations per arm; all workloads belong to one development family')
    fig.savefig(out/'classical.png',dpi=160);fig.savefig(out/'classical.svg');plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
