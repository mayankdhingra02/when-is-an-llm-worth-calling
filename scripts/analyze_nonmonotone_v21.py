"""Verify actual responses and score fixed rule matches; no objectives acquired."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.resources import Resources
from escalation.rule_audit_v20 import compare
from escalation.order_probe_v19 import inspect_response

def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2)+'\n')
def main():
    out=Path('results/v21_nonmonotone')
    if not (ROOT/out/'progress.json').exists():raise RuntimeError('No real probe; no synthetic substitution')
    if (ROOT/out/'summary.json').exists():raise RuntimeError('Preserve existing analysis')
    before=read('artifacts/resource_ledger_v2.json')
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Five-second reserve required')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':140}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for p,h in read('reports/protocol_v21_nonmonotone.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
        from transformers import AutoTokenizer
        from escalation.grammar_v8 import CandidateIDGrammar
        tok=AutoTokenizer.from_pretrained(ROOT/'models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False);grammar=CandidateIDGrammar(tok)
        jobs=read('data/nonmonotone_probe_v21.json')['jobs'];requests=lines(out/'requests.jsonl');starts=lines(out/'request_starts.jsonl');progress=read(out/'progress.json');began=read(out/'started.json')
        assert len(requests)==len(starts)<=3 and len(progress['cases'])==3
        assert before['requests']-began['baseline_ledger']['requests']==len(starts)
        assert began['authorization']['granted'] and began['authorization']['request_cap']==140
        rows=[]
        for job in jobs:
            matching=[r for r in requests if r['job_id']==job['job_id']]
            if not matching:rows.append({'dataset':job['dataset'],'status':'unattempted'});continue
            assert len(matching)==1;r=matching[0]
            assert r['messages']==job['messages'] and r['revision']=='7ae557604adf67be50417f59c2c2f167def9a775' and r['device']=='cpu' and r['dtype']=='torch.float32' and r['retry']==0
            if r['status']!='response':rows.append({'dataset':job['dataset'],'status':r['status'],'request_id':r['request_id']});continue
            assert grammar.replay(r['generated_token_ids'])==r['selection_trace']
            assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['raw_output']
            text=tok.apply_chat_template(r['messages'],tokenize=False,add_generation_prompt=True)
            assert hashlib.sha256(text.encode()).hexdigest()==r['rendered_prompt_sha256']
            assert len(tok(text)['input_ids'])==r['input_tokens'] and len(r['generated_token_ids'])==r['output_tokens']==20
            observation=inspect_response(r['raw_output'],job)
            rows.append({'dataset':job['dataset'],'status':'completed','request_id':r['request_id'],**observation,'rules':compare(job['display_ids'],observation['selected_ids'])})
        summary={'scope':'three fixed nonmonotone-ID conditions; no quality/generalization claim','intended':3,'actual_requests':len(starts),'completed':sum(r['status']=='completed' for r in rows),'cases':rows,'input_tokens_observed':sum(r['input_tokens'] for r in requests if r['input_tokens'] is not None),'output_tokens_observed':sum(r['output_tokens'] for r in requests if r['output_tokens'] is not None),'requests_missing_usage':sum(r['input_tokens'] is None or r['output_tokens'] is None for r in requests),'request_wall_seconds':sum(r['wall_seconds'] for r in requests),'new_objective_acquisitions':0,'external_spend_usd':0}
        write(out/'summary.json',summary);resource.checkpoint();print(json.dumps(summary,indent=2))
    after=read('artifacts/resource_ledger_v2.json');assert after['active_since'] is None
    write('artifacts/study_v21/analysis_accounting.json',{'before':before['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-before['experiment_seconds']})

if __name__=='__main__':main()
