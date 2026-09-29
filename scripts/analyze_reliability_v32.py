"""Fresh timing summaries; preserve historical selected configurations."""
import argparse,csv,hashlib,json,os,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
from escalation.io import read,write,lines
from escalation.reliability_v32 import compare,schedule
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require
OUT=Path('results/v32_reliability')

def calculate():
    freeze=read('reports/protocol_v32_reliability.freeze.json')
    for p,h in freeze['sha256'].items():require(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'Changed input: '+p)
    m=read('data/reliability_v32.json');p=read(OUT/'progress.json');trials=lines(OUT/'trials.jsonl');events=lines(OUT/'acquisitions.jsonl')
    expected=schedule([s['setting'] for s in m['selected']]);require(expected==read('artifacts/study_v32/schedule.json'),'Frozen schedule')
    require(p['complete'] and len(trials)==len(events)==len(expected)==m['intended_trials'],'Complete physical denominator')
    settings=[];times={}
    for a,t,e in zip(events,trials,expected):
        require(all(a[k]==t[k]==e[k] for k in ('trial_id','repetition','setting')),'Trial identity')
        require(a['charged_physical_vector']==1 and a['started_at']>freeze['created_at'],'Charged and frozen before launch')
        require(t['status']=='ok' and t['roundtrip_equal'],'Successful physical trial')
        require(hashlib.sha256(Path(t['compressed_path']).read_bytes()).hexdigest()==t['compressed_sha256'],'Payload retained')
    for s in m['selected']:
        config_id=s['setting']['config_id'];rows=sorted([t for t in trials if t['setting']['config_id']==config_id],key=lambda t:t['repetition'])
        require([t['repetition'] for t in rows]==list(range(20)),'Twenty fresh rounds')
        require(all(t['compressed_bytes']==s['expected_compressed_bytes'] and t['compressed_sha256']==s['expected_compressed_sha256'] for t in rows),'Stable output bytes')
        values=[t['compression_ns'] for t in rows];times[config_id]=values
        settings.append({'config_id':config_id,'family':s['setting']['family'],'historical_median_ms':s['historical_median_ms'],
            'fresh_median_ms':statistics.median(values)/1e6,'fresh_cv':statistics.pstdev(values)/statistics.mean(values),
            'min_ms':min(values)/1e6,'max_ms':max(values)/1e6,'compressed_bytes':s['expected_compressed_bytes']})
    cases=[]
    for c in m['cases']:
        roles=c['roles'];cheap=times[roles['joint_3nn']];random=times[roles['random']];oracle=times[roles['historical_hindsight']]
        for config_id in roles.values():require(next(s for s in settings if s['config_id']==config_id)['compressed_bytes']<=c['size_cap_bytes'],'Fixed size cap')
        comparison=compare(cheap,random)
        # compare takes candidate first, reference denominator second.
        hindsight=compare(oracle,cheap)
        cases.append({'family':c['family'],'seed':c['seed'],'size_cap_bytes':c['size_cap_bytes'],
            'cheap_config_id':roles['joint_3nn'],'random_config_id':roles['random'],'historical_hindsight_config_id':roles['historical_hindsight'],
            'same_cheap_random_setting':roles['joint_3nn']==roles['random'],
            'old_cheap_gain_over_random':c['cheap_gain_over_random'],
            'old_hindsight_headroom':c['hindsight_headroom_over_cheap'],
            'fresh_cheap_median_ms':statistics.median(cheap)/1e6,'fresh_random_median_ms':statistics.median(random)/1e6,
            'fresh_historical_hindsight_median_ms':statistics.median(oracle)/1e6,
            **comparison,**{'historical_reference_'+k:v for k,v in hindsight.items()}})
    groups=[]
    for family in ('zstd','lz4','zlib'):
        rows=[c for c in cases if c['family']==family]
        groups.append({'family':family,'cases':len(rows),'old_mean_cheap_gain':statistics.mean(c['old_cheap_gain_over_random'] for c in rows),
            'fresh_mean_cheap_gain':statistics.mean(c['relative_gain_of_medians'] for c in rows),
            'old_mean_hindsight_headroom':statistics.mean(c['old_hindsight_headroom'] for c in rows),
            'fresh_mean_historical_reference_gain':statistics.mean(c['historical_reference_relative_gain_of_medians'] for c in rows),
            'same_setting_cases':sum(c['same_cheap_random_setting'] for c in rows),
            'fresh_wins':sum(c['relative_gain_of_medians']>0 for c in rows),
            'fresh_ties':sum(c['relative_gain_of_medians']==0 for c in rows),'fresh_losses':sum(c['relative_gain_of_medians']<0 for c in rows)})
    return {'scope':'Exploratory remeasurement of fixed historical selections; not new optimizer arms or fresh full-grid headroom',
        'complete':True,'cases':cases,'groups':groups,'settings':settings,'physical_trials':len(trials),
        'unique_settings':len(settings),'rounds':20,'new_optimizer_acquisitions':0,'new_model_calls':0,
        'equal_family_old_gain':statistics.mean(g['old_mean_cheap_gain'] for g in groups),
        'equal_family_fresh_gain':statistics.mean(g['fresh_mean_cheap_gain'] for g in groups)}

def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,old,new,title in [(axes[0],'old_mean_cheap_gain','fresh_mean_cheap_gain','Cheap versus random selections'),
        (axes[1],'old_mean_hindsight_headroom','fresh_mean_historical_reference_gain','Fixed historical hindsight versus cheap')]:
        groups=result['groups'];x=list(range(len(groups)))
        ax.bar([v-.18 for v in x],[100*g[old] for g in groups],width=.36,label='Original three-repeat medians',color='#a0afb8')
        ax.bar([v+.18 for v in x],[100*g[new] for g in groups],width=.36,label='Fresh twenty-repeat medians',color='#176b93')
        ax.set_xticks(x,[g['family'] for g in groups]);ax.axhline(0,color='black',linewidth=.7)
        ax.set_title(title,fontsize=10);ax.set_ylabel('Mean relative target gain (%)');ax.legend(fontsize=7)
    fig.suptitle('V32: fresh timing check of fixed configuration choices')
    fig.text(.5,.015,'Same workload and size caps; shared settings reuse observations. No new optimizer or LLM runs. Separate panel scales.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.055,1,.95])
    for ext in ('png','svg'):fig.savefig(OUT/f'comparison.{ext}',dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        require(calculate()==read(OUT/'summary.json'),'Saved analysis differs');print('Physical schedule, hashes, caps, medians and all15 cases replayed.');return
    require(not (OUT/'summary.json').exists(),'Preserve completed analysis')
    before=read('artifacts/resource_ledger_v2.json');cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        resource.check();r=calculate();write(OUT/'summary.json',r)
        for name,rows in [('cases',r['cases']),('settings',r['settings'])]:
            with (OUT/f'{name}.csv').open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(r);resource.check()
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v32/analysis_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_physical_trials':0,'new_optimizer_acquisitions':0,'new_model_calls':0,'active_since':after['active_since']})
    print(json.dumps({'groups':r['groups'],'equal_family_old_gain':r['equal_family_old_gain'],'equal_family_fresh_gain':r['equal_family_fresh_gain']},indent=2))

if __name__=='__main__':main()
