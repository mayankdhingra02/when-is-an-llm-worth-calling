"""Validate real response provenance and compare IDs/display positions/configurations."""
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines,digest
from escalation.order_probe_v19 import inspect_response
from escalation.resources import Resources
OUT=ROOT/'results/v19_order_probe'

def main():
    if not (OUT/'progress.json').exists():raise RuntimeError('No executed probe; no synthetic result substitution')
    if (OUT/'summary.json').exists():raise RuntimeError('Preserve completed analysis')
    before=read(ROOT/'artifacts/resource_ledger_v2.json')
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Five-second inactive reserve required')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':137}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for p,h in read(ROOT/'reports/protocol_v19_order.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
        jobs=read(ROOT/'data/order_probe_v19.json')['jobs'];req=lines(OUT/'requests.jsonl');starts=lines(OUT/'request_starts.jsonl')
        assert len(starts)==len(req)<=9
        from transformers import AutoTokenizer
        from escalation.grammar_v8 import CandidateIDGrammar
        tok=AutoTokenizer.from_pretrained(ROOT/'models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False);grammar=CandidateIDGrammar(tok)
        outcomes=[];comparisons=[]
        for job in jobs:
            path=OUT/'outcomes'/f"{job['job_id']:02d}.json"
            if not path.exists():outcomes.append({'job_id':job['job_id'],'dataset':job['dataset'],'condition':job['condition'],'status':'unattempted'});continue
            outcome=read(path);response=next(r for r in req if r['request_id']==outcome['request_id'])
            assert response['messages']==job['messages'] and response['revision']=='7ae557604adf67be50417f59c2c2f167def9a775'
            assert response['device']=='cpu' and response['dtype']=='torch.float32' and response['retry']==0
            assert response['condition']==job['condition'] and response['job_id']==job['job_id']
            if outcome['status']=='completed':
                assert grammar.replay(response['generated_token_ids'])==response['selection_trace']
                assert tok.decode(response['generated_token_ids'],skip_special_tokens=True)==response['raw_output']
                assert response['output_tokens']==len(response['generated_token_ids'])==20
                rendered=tok.apply_chat_template(response['messages'],tokenize=False,add_generation_prompt=True)
                assert response['rendered_prompt_sha256']==hashlib.sha256(rendered.encode()).hexdigest()
                assert response['input_tokens']==len(tok(rendered)['input_ids'])
                assert all(outcome[k]==v for k,v in inspect_response(response['raw_output'],job).items())
            outcomes.append(outcome)
        for dataset in dict.fromkeys(j['dataset'] for j in jobs):
            selected={o['condition']:o for o in outcomes if o['dataset']==dataset and o['status']=='completed'}
            for mode in ['reverse_display','reverse_ids']:
                if 'original' in selected and mode in selected:
                    original=set(selected['original']['selected_rows']);changed=set(selected[mode]['selected_rows'])
                    comparisons.append({'dataset':dataset,'condition':mode,'same_selected_row_set':original==changed,'overlap_out_of_ten':len(original&changed)})
        summary={'scope':'exploratory three-case mechanism probe; not optimization benefit or generalization','intended':9,'completed':sum(o['status']=='completed' for o in outcomes),'outcomes':outcomes,'comparisons':comparisons,'actual_requests':len(starts),'input_tokens_observed':sum(r['input_tokens'] for r in req if r['input_tokens'] is not None),'output_tokens_observed':sum(r['output_tokens'] for r in req if r['output_tokens'] is not None),'requests_missing_usage':sum(r['input_tokens'] is None or r['output_tokens'] is None for r in req),'request_wall_seconds':sum(r['wall_seconds'] for r in req),'new_objective_acquisitions':0,'external_spend_usd':0}
        write(OUT/'summary.json',summary);print(__import__('json').dumps(summary,indent=2));resource.checkpoint()
    after=read(ROOT/'artifacts/resource_ledger_v2.json');assert after['active_since'] is None
    write(ROOT/'artifacts/study_v19/analysis_accounting.json',{'before':before['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-before['experiment_seconds']})

if __name__=='__main__':main()
