"""Replay classical decisions and validate all native outputs before aggregation."""
import hashlib,json,math,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v83 import expected,validate
from escalation.h2_v84 import CONFIGS,PRIOR,SEEDS,ARMS,choose,prefix_choice,incumbent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def analyze():
    raw=ROOT/'results/v84_h2_classical';summary=read(raw/'summary.json');rows=read(raw/'acquisitions.json');cases=read(raw/'cases.json');truth=expected();lock=read(ROOT/'configs/runtime_v83.lock.json')
    for n,d in read(ROOT/'reports/protocol_v84.freeze.json')['sha256'].items():assert sha(ROOT/n)==d,n
    assert summary['complete'] and summary['intended_trials']==summary['charged_trials']==summary['valid_trials']==len(rows)==165
    assert summary['unattempted']==0 and summary['completed_seeds']==5 and summary['new_model_requests']==0 and summary['seconds']<1800
    for i,r in enumerate(rows):
        p=raw/f'trial_{i:03d}';c=CONFIGS[r['config_id']];assert r['trial']==i and r['config']==c and r['status']=='valid' and r['path']==str(p.relative_to(ROOT))
        cmd=[str(ROOT/lock['java']),'-Xmx512m','-XX:ActiveProcessorCount=4','-cp',str(ROOT/lock['jar'])+':'+str(ROOT/lock['classes']),'H2Probe',str(c['mask']),str(c['recompile']).lower(),str(c['analyze_sample']),str(p)]
        assert r['command']==cmd
        charge=read(p/'charge.json');assert charge['status']=='charged'
        for k in charge:
            if k!='status':assert charge[k]==r[k],(i,k)
        receipt=read(p/'process_receipt.json');assert receipt==r['process'] and receipt['exit_code']==0 and receipt['termination_reason'] is None and receipt['wall_seconds']<60
        assert receipt['sampled_maxima']['rss_bytes']<2*1024**3 and receipt['sampled_maxima']['scratch_bytes']<128*1024**2
        assert validate(p,c,truth)==r['metrics'];assert sha(p/'answers.csv')==r['answers_sha256'];assert read(p/'result.json')==r
        assert math.isfinite(r['metrics']['query_seconds']) and r['metrics']['query_seconds']>0
    cursor=0;results=[]
    def consume(seed,arm,purpose,cid,obs):
        nonlocal cursor
        r=rows[cursor];assert (r['seed'],r['arm'],r['purpose'],r['config_id'],r['logical_evaluation'])==(seed,arm,purpose,cid,len(obs)+1)
        obs.append({'config_id':cid,'query_seconds':r['metrics']['query_seconds'],'physical_trial':cursor});cursor+=1
    for si,seed in enumerate(SEEDS):
        case=cases[si];assert case['seed']==seed and case['complete'];prefix=[]
        for j in range(10):consume(seed,'prefix','search',prefix_choice(prefix,seed),prefix)
        pp=raw/f'prefix_{seed}.json';assert read(pp)=={'seed':seed,'system_group':'h2','observations':prefix,'budget_used':10,'remaining_including_confirmations':10}
        assert sha(pp)==case['prefix_sha256'] and prefix==case['prefix']
        branches={arm:[dict(o) for o in prefix] for arm in ['rf_lcb','random']};branches['prior']=[]
        for j in range(7):
            for arm in (['rf_lcb','random'] if (si+j)%2==0 else ['random','rf_lcb']):consume(seed,arm,'search',choose(branches[arm],arm,seed),branches[arm])
        selected={arm:incumbent(branches[arm]) for arm in ['rf_lcb','random']};selected['prior']=PRIOR
        assert case['selected']==selected and read(raw/f'locked_{seed}.json')=={'selected':selected,'physical_trials_at_lock':cursor,'prefix_sha256':sha(pp)}
        for rep in range(3):
            offset=(si+rep)%3
            for arm in ARMS[offset:]+ARMS[:offset]:consume(seed,arm,'fixed_prior' if arm=='prior' else 'confirmation',selected[arm],branches[arm])
        assert branches==case['branches'] and [len(branches[a]) for a in ARMS]==[20,20,3]
        arm_results={}
        for arm in ARMS:
            rr=[rows[o['physical_trial']] for o in branches[arm][-3:]];t=[r['metrics']['query_seconds'] for r in rr];median=statistics.median(t);index=statistics.median(r['metrics']['index_and_analyze_seconds'] for r in rr)
            arm_results[arm]={'selected_config_id':selected[arm],'config':CONFIGS[selected[arm]],'confirmation_seconds':t,'median_seconds':median,'range_over_median':(max(t)-min(t))/median,'precision_pass':median>=.1 and (max(t)-min(t))/median<=.2,'median_index_analyze_seconds':index,'modeled_index_plus_query_seconds':{str(k):index+k*median for k in [1,10,100]},'logical_evaluations':len(branches[arm]),'realized_branch_collection_seconds_including_shared_prefix':sum(rows[o['physical_trial']]['process']['wall_seconds']+rows[o['physical_trial']]['decision_seconds'] for o in branches[arm])}
        prior=arm_results['prior']
        for arm in ['rf_lcb','random']:
            a=arm_results[arm];a['gain_vs_prior']=1-a['median_seconds']/prior['median_seconds'];a['material_gain_flag']=a['gain_vs_prior']>=.1;a['comparison_precision_pass']=a['precision_pass'] and prior['precision_pass']
        results.append({'seed':seed,'arms':arm_results,'rf_gain_vs_random':1-arm_results['rf_lcb']['median_seconds']/arm_results['random']['median_seconds']})
    assert cursor==165
    return {'complete':True,'system_group':'h2','independent_system_groups':1,'cases':results,'physical_trials':165,'logical_rf_random_trials':200,'logical_prior_trials':15,'checked_scored_answers':165*6144,'actual_native_wall_seconds':sum(r['process']['wall_seconds'] for r in rows),'actual_decision_seconds':sum(r['decision_seconds'] for r in rows),'runner_wall_seconds':summary['seconds'],'model_calls':0,'scope':'exposed development classical pilot; no LLM or generalization claim'}

def main():
    out=ROOT/'results/v84_h2_analysis';assert not out.exists();data=analyze();out.mkdir()
    (out/'summary.json').write_text(json.dumps(data,indent=2)+'\n')
    import csv
    with (out/'per_seed.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['seed','arm','candidate','median_seconds','range_over_median','precision_pass','gain_vs_prior','logical_evaluations'])
        for case in data['cases']:
            for arm,a in case['arms'].items():w.writerow([case['seed'],arm,a['selected_config_id'],a['median_seconds'],a['range_over_median'],a['precision_pass'],a.get('gain_vs_prior',''),a['logical_evaluations']])
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4))
    for i,arm in enumerate(ARMS):
        vals=[c['arms'][arm]['median_seconds'] for c in data['cases']];ax.plot(SEEDS,vals,marker='o',label=arm)
    ax.set_xlabel('Repeated seed (one H2 system)');ax.set_ylabel('Confirmation median query-suite seconds');ax.legend();fig.tight_layout();fig.savefig(out/'confirmation.png',dpi=160);plt.close(fig)
    print(json.dumps({k:v for k,v in data.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
