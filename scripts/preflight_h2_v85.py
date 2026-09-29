"""Six prompt/token checks, no completions or H2 measurements."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v85 import messages,check_cfg,CONFIGS,SEEDS
from escalation.receipts_v70 import atomic_json
from runtime_h2_v85 import Runtime

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    cfg=json.loads((ROOT/'configs/study_v85.json').read_text());check_cfg(cfg)
    pins=json.loads((ROOT/'reports/protocol_v78.freeze.json').read_text())['sha256']
    for n,d in pins.items():
        if n.startswith(('models/SmolLM3','.local-runtime/llama-')) or n=='artifacts/study_v78/runtime_plan.json':assert sha(ROOT/n)==d,n
    out=ROOT/'artifacts/study_v85/prompt_preflight';out.mkdir(exist_ok=False);rt=Runtime(ROOT,out,cfg);records=[];error=None
    try:
        rt.start()
        for seed in SEEDS+[None]:
            if seed is None:
                label='synthetic_structure_stress';obs=[{'config_id':i,'query_seconds':59.99999999999999} for i in range(320,336)]
            else:label='prefix_'+str(seed);obs=json.loads((ROOT/f'results/v84_h2_classical/prefix_{seed}.json').read_text())['observations']
            msgs=messages(obs);rendered=rt.api('/apply-template',{'messages':msgs,'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
            tokens=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens'];assert len(tokens)+64<=4096
            row={'name':label,'synthetic':seed is None,'messages':msgs,'rendered':rendered,'tokens':tokens,'input_tokens':len(tokens),'prompt_sha256':hashlib.sha256(rendered['prompt'].encode()).hexdigest()};records.append(row)
            atomic_json(out/(label+'.json'),row)
        assert rt.ledger['generation_requests']==0
    except Exception as e:error=repr(e);raise
    finally:
        rt.close();atomic_json(out/'summary.json',{'complete':error is None and len(records)==6,'error':error,'new_model_generations':rt.ledger['generation_requests'],'new_objective_evaluations':0,'prompt_input_tokens':{r['name']:r['input_tokens'] for r in records},'stress_fixture_is_not_measured_outcome':True,'not_a_bound_on_every_future_prompt':True})
if __name__=='__main__':main()
