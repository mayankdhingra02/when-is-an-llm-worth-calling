"""Post-collection table/figure and independent prompt-intervention audit; no inference."""
import csv,hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib');os.environ['XDG_CACHE_HOME']=str(ROOT/'.cache')
from escalation.resources import Resources

def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(x) for x in (ROOT/p).read_text().splitlines()]
def write(p,v):(ROOT/p).write_text(json.dumps(v,indent=2)+'\n')
def main():
    before=read('artifacts/resource_ledger_v2.json')
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Need inactive five-second reserve')
    out=ROOT/'results/v19_order_probe'
    if (out/'response_table.csv').exists():raise RuntimeError('Preserve completed presentation audit')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':137}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        jobs=read('data/order_probe_v19.json')['jobs'];responses=lines('results/v19_order_probe/requests.jsonl');starts=lines('results/v19_order_probe/request_starts.jsonl')
        original_responses=lines('results/v8/requests.jsonl');progress=read('results/v19_order_probe/progress.json');summary=read('results/v19_order_probe/summary.json');began=read('results/v19_order_probe/started.json')
        assert len(jobs)==len(responses)==len(starts)==progress['completed']==summary['completed']==9
        assert progress['request_attempts']==9 and progress['stop_reason'] is None
        assert before['requests']-began['baseline_ledger']['requests']==9
        assert [r['request_id'] for r in responses]==[r['request_id'] for r in starts]==list(range(129,138))
        approval=began['authorization'];assert approval['granted'] and approval['request_cap']==137
        assert approval['recorded_at']<began['at']<min(r['started'] for r in responses)
        rows=[];matrix=[];labels=[]
        for dataset in dict.fromkeys(j['dataset'] for j in jobs):
            old=next(r for r in original_responses if r['dataset']==dataset and r['seed']==11)
            originals=json.loads(old['messages'][-1]['content'].split('\n',1)[1]);candidates=originals['candidates']
            original_mapping=next(j['original_pool']['mapping'] for j in jobs if j['dataset']==dataset)
            for mode in ['original','reverse_display','reverse_ids']:
                job=next(j for j in jobs if j['dataset']==dataset and j['condition']==mode)
                response=next(r for r in responses if r['job_id']==job['job_id']);body=json.loads(response['messages'][-1]['content'].split('\n',1)[1])
                assert response['messages']==job['messages']
                assert response['messages'][0]==old['messages'][0]
                assert {k:v for k,v in body.items() if k!='candidates'}=={k:v for k,v in originals.items() if k!='candidates'}
                if mode=='original':assert response['messages']==old['messages'] and body['candidates']==candidates
                elif mode=='reverse_display':assert body['candidates']==list(reversed(candidates)) and job['mapping']==original_mapping
                else:
                    assert [r['x'] for r in body['candidates']]==[r['x'] for r in candidates]
                    assert [r['id'] for r in body['candidates']]==[r['id'] for r in reversed(candidates)]
                    assert all(job['mapping'][new['id']]==original_mapping[old_row['id']] for old_row,new in zip(candidates,body['candidates']))
                assert response['status']=='response' and response['retry']==0 and response['parameters']['do_sample'] is False
                selected=response['raw_output'].strip().splitlines();assert len(selected)==len(set(selected))==10
                chosen=[job['mapping'][i] for i in selected]
                display=[r['id'] for r in body['candidates']];positions=[display.index(i)+1 for i in selected]
                record={'dataset':dataset,'seed':11,'condition':mode,'request_id':response['request_id'],'output_ids':' '.join(selected),'selected_display_positions':' '.join(map(str,positions)),
                    'exact_first_displayed_ten':selected==display[:10],'matches_archived_output':response['raw_output']==old['raw_output'],
                    'input_tokens':response['input_tokens'],'output_tokens':response['output_tokens'],'request_wall_seconds':response['wall_seconds']}
                rows.append(record);matrix.append([int(original_mapping[i] in chosen) for i in original_mapping]);labels.append(f'{dataset}: {mode}')
        with (out/'response_table.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
        fig,axis=plt.subplots(figsize=(10,4.8));axis.imshow(matrix,cmap=ListedColormap(['#eef0f3','#176b93']),vmin=0,vmax=1,aspect='auto')
        axis.set_yticks(range(9),labels);axis.set_xticks(range(20),range(1,21));axis.set_xlabel('Configuration position in the ORIGINAL candidate list')
        axis.set_title('Nine real responses: selected configurations track display order')
        for y in [2.5,5.5]:axis.axhline(y,color='white',linewidth=3)
        axis.axvline(9.5,color='white',linewidth=1)
        fig.text(.5,.02,'Blue = selected. Qwen2.5-0.5B-Instruct; three exposed cases; no quality or generalization claim.',ha='center',fontsize=9)
        fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(out/'selection_order.png',dpi=170);fig.savefig(out/'selection_order.svg');plt.close(fig)
        checks={'verified':True,'independent_prompt_intervention_checks':9,'request_start_response_ids_verified':True,'explicit_approval_precedes_inference':True,
            'fresh_original_matches_archived_outputs':sum(r['condition']=='original' and r['matches_archived_output'] for r in rows),
            'exact_first_ten_displayed_sequences':sum(r['exact_first_displayed_ten'] for r in rows),'intended':9,'completed':9,
            'new_model_calls_in_this_audit':0,'new_objective_acquisitions':0,'token_provenance_verified_by':'scripts/analyze_order_v19.py'}
        write('artifacts/study_v19/execution_verification.json',checks);resource.checkpoint()
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==137 and after['active_since'] is None
    write('artifacts/study_v19/presentation_accounting.json',{'before':before['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-before['experiment_seconds']})
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
