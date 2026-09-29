"""Post-collection response mapping audit and plot; no inference/objective acquisition."""
import csv,hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib');os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.resources import Resources

def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2)+'\n')
def main():
    before=read('artifacts/resource_ledger_v2.json');out=ROOT/'results/v21_nonmonotone'
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Five-second inactive reserve required')
    if (out/'response_table.csv').exists():raise RuntimeError('Preserve completed audit')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':140}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        jobs=read('data/nonmonotone_probe_v21.json')['jobs'];requests=lines('results/v21_nonmonotone/requests.jsonl');starts=lines('results/v21_nonmonotone/request_starts.jsonl');summary=read('results/v21_nonmonotone/summary.json');began=read('results/v21_nonmonotone/started.json')
        assert len(jobs)==len(requests)==len(starts)==summary['completed']==3
        assert [r['request_id'] for r in requests]==[r['request_id'] for r in starts]==[138,139,140]
        assert before['requests']-began['baseline_ledger']['requests']==3
        assert began['authorization']['recorded_at']<began['at']<min(r['started'] for r in requests)
        originals=read('data/order_probe_v19.json')['jobs'];previous=read('results/v19_order_probe/summary.json')['outcomes'];rows=[];matrix=[]
        for job in jobs:
            original=next(j for j in originals if j['dataset']==job['dataset'] and j['condition']=='original')
            new_body=json.loads(job['messages'][-1]['content'].split('\n',1)[1]);old_body=json.loads(original['messages'][-1]['content'].split('\n',1)[1])
            assert job['messages'][0]==original['messages'][0]
            assert {k:v for k,v in new_body.items() if k!='candidates'}=={k:v for k,v in old_body.items() if k!='candidates'}
            assert [r['x'] for r in new_body['candidates']]==[r['x'] for r in old_body['candidates']]
            assert all(job['mapping'][new['id']]==original['mapping'][old['id']] for new,old in zip(new_body['candidates'],old_body['candidates']))
            request=next(r for r in requests if r['job_id']==job['job_id']);assert request['messages']==job['messages'] and request['status']=='response'
            outcome=next(r for r in summary['cases'] if r['request_id']==request['request_id']);selected=request['raw_output'].strip().splitlines()
            assert selected==outcome['selected_ids']
            assert [job['mapping'][i] for i in selected]==outcome['selected_rows']
            display=[r['id'] for r in new_body['candidates']];positions=[display.index(i)+1 for i in selected]
            prior=next(r for r in previous if r['dataset']==job['dataset'] and r['condition']=='original')
            rows.append({'dataset':job['dataset'],'request_id':request['request_id'],'output_ids':' '.join(selected),'selected_display_positions':' '.join(map(str,positions)),'display_prefix_match':outcome['rules']['display_prefix']['sequence_match'],'endpoint_sequence_match':outcome['rules']['endpoint_sequence']['sequence_match'],'lowest_ids_match':outcome['rules']['lowest_ids']['sequence_match'],'overlap_with_v19_original_out_of_ten':len(set(outcome['selected_rows'])&set(prior['selected_rows']))})
            matrix.append([int(i in selected) for i in display])
        with (out/'response_table.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
        fig,axis=plt.subplots(figsize=(9,3.4));axis.imshow(matrix,cmap=ListedColormap(['#edf0f2','#176b93']),vmin=0,vmax=1,aspect='auto')
        axis.set_yticks(range(3),[r['dataset'] for r in rows]);axis.set_xticks(range(20),jobs[0]['display_ids']);axis.set_xlabel('Candidate IDs in their actual displayed order')
        axis.set_title('Three real responses to an interleaved-ID assignment')
        axis.axvline(9.5,color='white',linewidth=2)
        fig.text(.5,.02,'Blue = selected. One response per exposed case; existing Qwen0.5B; no selection-quality claim.',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.08,1,1]);fig.savefig(out/'interleaved_selection.png',dpi=170);fig.savefig(out/'interleaved_selection.svg');plt.close(fig)
        checks={'verified':True,'independent_feature_preserving_relabeling_checks':3,'request_start_ids_verified':True,'approval_precedes_inference':True,'intended':3,'completed':3,'display_prefix_matches':sum(r['display_prefix_match'] for r in rows),'endpoint_sequence_matches':sum(r['endpoint_sequence_match'] for r in rows),'new_model_calls_in_audit':0,'new_objective_acquisitions':0}
        write('artifacts/study_v21/execution_verification.json',checks);resource.checkpoint();print(json.dumps(checks,indent=2))
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==140 and after['active_since'] is None
    write('artifacts/study_v21/presentation_accounting.json',{'before':before['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'remaining_seconds':1800-after['experiment_seconds']})

if __name__=='__main__':main()
