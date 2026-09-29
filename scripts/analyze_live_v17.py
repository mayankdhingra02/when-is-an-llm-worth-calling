"""Describe saved measurement completeness/noise; never choose a best configuration."""
import csv,hashlib,json,statistics,sys,os
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.live_compression_v17 import schedule,settings
from escalation.resources import Resources


def read(path):return json.loads((ROOT/path).read_text())
def lines(path):return [json.loads(line) for line in (ROOT/path).read_text().splitlines() if line.strip()]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    config=read('configs/live_measurement_v17.json');out=ROOT/'results/v17_measurements'
    if (out/'summary.json').exists():raise RuntimeError('Analysis already saved; preserve it instead of overwriting')
    before=read('artifacts/resource_ledger_v2.json')
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Analysis requires inactive ledger with5seconds reserve')
    resource_config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
    with Resources(resource_config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for name,expected in read('reports/protocol_v17_expansion.freeze.json')['sha256'].items():assert sha(ROOT/name)==expected,name
        workload=read('artifacts/study_v15/workload_manifest.json')
        planned=schedule();saved=read('results/v17_measurements/schedule.json');assert saved==planned
        acquired=lines('results/v17_measurements/acquisitions.jsonl');trials=lines('results/v17_measurements/trials.jsonl')
        assert len(acquired)==len(trials)
        assert [r['trial_id'] for r in trials]==list(range(len(trials)))
        observed=defaultdict(list)
        for entry,row in zip(acquired,trials):
            expected=planned[row['trial_id']]
            for key in ('trial_id','repetition','setting'):assert entry[key]==row[key]==expected[key]
            assert entry['charged_physical_vector']==1
            if row['status']=='ok':
                assert row['roundtrip_equal'] is True and row['decoded_sha256']==workload['workload_sha256']
                payload=ROOT/row['compressed_path'];assert payload.stat().st_size==row['compressed_bytes'] and sha(payload)==row['compressed_sha256']
                observed[row['setting']['config_id']].append(row)
        records=[]
        for setting in settings():
            values=observed[setting['config_id']];times=[r['compression_ns']/1e6 for r in values]
            record={'config_id':setting['config_id'],'family':setting['family'],'setting':setting,
                    'successful_trials':len(values),'complete_three_trials':len(values)==3,
                    'median_compression_ms':statistics.median(times) if times else None,
                    'compression_cv':statistics.stdev(times)/statistics.mean(times) if len(times)>1 else None,
                    'distinct_output_digests':len({r['compressed_sha256'] for r in values}),
                    'compressed_bytes':values[0]['compressed_bytes'] if values else None}
            records.append(record)
        groups=[]
        for family in config['families']:
            rows=[r for r in records if r['family']==family];complete=[r for r in rows if r['complete_three_trials']]
            physical=[r for r in trials if r['setting']['family']==family]
            groups.append({'family':family,'intended_configurations':len(rows),'complete_configurations':len(complete),
                           'attempted_trials':len(physical),'successful_trials':sum(r['status']=='ok' for r in physical),
                           'median_cv':statistics.median(r['compression_cv'] for r in complete) if complete else None,
                           'cv_above_point_one':sum(r['compression_cv']>.1 for r in complete),
                           'unstable_output_configurations':sum(r['distinct_output_digests']>1 for r in rows),
                           'distinct_successful_outputs':len({r['compressed_sha256'] for r in physical if r['status']=='ok'})})
        summary={'scope':'live development measurement feasibility only; no optimizer or LLM gain comparison',
                 'intended_trials':846,'charged_physical_vector_attempts':len(acquired),
                 'status_counts':dict(Counter(r['status'] for r in trials)),
                 'unattempted_trials':846-len(trials),'settings':records,'groups':groups,
                 'new_model_requests':0,'workload_bytes':workload['workload_bytes'],
                 'collection_wall_seconds_sum':sum(r['collection_wall_seconds'] for r in trials),
                 'roundtrip_verification_scope':'worker checked exact actual decoded bytes; this offline replay checks saved payload hashes, logs and counts without rerunning codecs'}
        with (out/'configuration_summary.csv').open('w',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=[k for k in records[0] if k!='setting']);writer.writeheader()
            writer.writerows({k:v for k,v in row.items() if k!='setting'} for row in records)
        resource.check()
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        figure,axis=plt.subplots(figsize=(7,4))
        for i,family in enumerate(config['families']):
            rows=[r for r in records if r['family']==family and r['complete_three_trials']]
            x=[i+(j-(len(rows)-1)/2)*.012 for j in range(len(rows))]
            axis.scatter(x,[100*r['compression_cv'] for r in rows],s=20,alpha=.75,label=family)
        axis.axhline(10,color='darkorange',linestyle='--',linewidth=1,label='10% diagnostic flag')
        axis.set_xticks(range(3),['Zstandard','LZ4','zlib']);axis.set_ylabel('Within-setting timing CV (%)')
        axis.set_title('Live measurement feasibility: three trials per setting')
        axis.grid(axis='y',alpha=.2);axis.legend(loc='best',fontsize=8)
        figure.text(.5,.015,'One CPython source archive; development only. Timing stacks differ; no LLM inference.',ha='center',fontsize=8)
        figure.tight_layout(rect=[0,.045,1,1]);figure.savefig(out/'timing_variability.png',dpi=160);figure.savefig(out/'timing_variability.svg');plt.close(figure)
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        verification={'verified':True,'schedule_replayed':True,'physical_charges':len(acquired),'payloads_hash_checked':sum(r['status']=='ok' for r in trials),'full_intended_denominator':846,'new_model_calls':0,'new_compression_trials_during_analysis':0}
        (ROOT/'artifacts/study_v17/physical_verification.json').write_text(json.dumps(verification,indent=2)+'\n')
        resource.checkpoint()
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==before['requests']==128 and after['active_since'] is None
    (ROOT/'artifacts/study_v17/physical_analysis_ledger_ledger.json').write_text(json.dumps(after,indent=2)+'\n')
    print(json.dumps({'groups':groups,'status_counts':summary['status_counts'],'charged_physical_vector_attempts':len(acquired),'remaining_runtime_seconds':1800-after['experiment_seconds']},indent=2))


if __name__=='__main__':main()
