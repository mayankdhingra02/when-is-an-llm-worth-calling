"""Fixed post-hoc decomposition of ALL V16/V17 development cases; no new outcomes."""
import argparse,csv,hashlib,json,os,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib');os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.checkpoint_audit_v18 import decompose
from escalation.resources import Resources

def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    out=Path('results/v18_checkpoint_audit');baseline=read('artifacts/resource_ledger_v2.json')
    if baseline.get('active_since') or 1800-baseline['experiment_seconds']<5:raise RuntimeError('Need inactive ledger and five-second reserve')
    if not args.verify_only and (ROOT/out/'summary.json').exists():raise RuntimeError('Preserve completed audit')
    config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
    with Resources(config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for name,h in read('reports/protocol_v18_checkpoint.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
        records=[]
        for study,measurement in [(16,15),(17,17)]:
            with (ROOT/f'results/v{measurement}_measurements/configuration_summary.csv').open() as f:
                raw=list(csv.DictReader(f))
            assert all(r['successful_trials']=='3' for r in raw)
            table={(r['family'],r['config_id']):[float(r['median_compression_ms']),float(r['compressed_bytes'])] for r in raw}
            for dataset in read(f'data/live_manifest_v{measurement}.json')['datasets']:
                assert dataset['split']=='development';family=dataset['system_group']
                ys=[table[family,s['config_id']] for s in dataset['configurations']]
                for seed in [11,23,37,53,71]:
                    key=f'{family}_{seed}'
                    prefix=read(f'results/v{study}_classical/prefixes/{key}.json')
                    arm=read(f'results/v{study}_classical/joint_3nn/{key}.json')
                    records.append(dict(study=study,family=family,seed=seed,**decompose(ys,prefix,arm)))
        assert len(records)==30
        groups=[]
        for study in [16,17]:
            for family in ['zstd','lz4','zlib']:
                rs=[r for r in records if r['study']==study and r['family']==family];assert len(rs)==5
                means={k:statistics.mean(r[k] for r in rs) for k in ['reference_headroom','checkpoint_headroom','cheap_headroom','pre_checkpoint_saved_fraction_of_reference','continuation_saved_fraction_of_reference','remaining_fraction_of_reference']}
                groups.append(dict(study=study,family=family,cases=5,candidates=rs[0]['candidate_count'],feasible=rs[0]['feasible_count'],**means,
                    improved_by_continuation=sum(r['cheap_continuation_improved'] for r in rs),checkpoint_optimum_cases=sum(r['checkpoint_at_recorded_optimum'] for r in rs)))
        summary={'scope':'post-hoc descriptive development audit; full-table hindsight evaluator only; no model or optimizer run',
            'intended_cases':30,'completed_cases':len(records),'cases':records,'groups':groups,
            'new_physical_trials':0,'new_optimizer_acquisitions':0,'new_model_requests':0,
            'method':'All savings decomposition terms divided by reference runtime; each headroom column instead uses its named incumbent denominator.'}
        if args.verify_only:
            assert read(out/'summary.json')==summary
            print('Verified all30 cases against frozen source labels; decomposition identity and summary match.')
        else:
            write(out/'summary.json',summary)
            with (ROOT/out/'cases.csv').open('w',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
            resource.check()
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig,axes=plt.subplots(1,2,figsize=(9,4),sharey=True)
            for axis,study in zip(axes,[16,17]):
                rs=[g for g in groups if g['study']==study];bottom=[0.,0.,0.]
                for k,label in [('pre_checkpoint_saved_fraction_of_reference','Saved before checkpoint'),('continuation_saved_fraction_of_reference','Saved by cheap continuation'),('remaining_fraction_of_reference','Remaining hindsight opportunity')]:
                    values=[100*g[k] for g in rs];axis.bar(range(3),values,bottom=bottom,label=label)
                    bottom=[b+v for b,v in zip(bottom,values)]
                axis.set_xticks(range(3),['Zstandard','LZ4','zlib']);axis.set_title('32 settings' if study==16 else '96 / 96 / 90 settings');axis.grid(axis='y',alpha=.2)
            axes[0].set_ylabel('Fraction of reference runtime (%)')
            fig.suptitle('Where did the recorded optimization opportunity go?')
            handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=1,fontsize=8)
            fig.tight_layout(rect=[0,.22,1,.92]);fig.savefig(out/'decomposition.png',dpi=160);fig.savefig(out/'decomposition.svg');plt.close(fig)
            print(json.dumps({'groups':groups},indent=2))
        resource.checkpoint()
    after=read('artifacts/resource_ledger_v2.json');assert after['active_since'] is None and after['requests']==baseline['requests']==128
    name='replay' if args.verify_only else 'analysis'
    write(f'artifacts/study_v18/{name}_accounting.json',{'before':baseline['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-baseline['experiment_seconds'],'remaining_seconds':1800-after['experiment_seconds'],'new_requests':0})

if __name__=='__main__':main()
