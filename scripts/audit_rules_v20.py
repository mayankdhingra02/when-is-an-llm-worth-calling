"""Compare fixed behavioral alternatives with saved actual responses, not mock inference."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.rule_audit_v20 import predictions,compare,nonmonotone_assignment,RULES
from escalation.resources import Resources

def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    before=read('artifacts/resource_ledger_v2.json');out=Path('results/v20_rule_audit')
    if before['active_since'] is not None or 1800-before['experiment_seconds']<5:raise RuntimeError('Five-second inactive reserve required')
    if not args.verify_only and (ROOT/out/'summary.json').exists():raise RuntimeError('Completed audit retained')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':137}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        for p,h in read('reports/protocol_v20_rules.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
        rows=[];orders={};counts={8:15,19:9}
        prepared={j['job_id']:j for j in read('data/order_probe_v19.json')['jobs']}
        for study,count in counts.items():
            path='results/v8/requests.jsonl' if study==8 else 'results/v19_order_probe/requests.jsonl';requests=lines(path);assert len(requests)==count
            for request in requests:
                assert request['status']=='response' and request['retry']==0
                if study==19:assert request['messages']==prepared[request['job_id']]['messages']
                body=json.loads(request['messages'][-1]['content'].split('\n',1)[1]);display=[c['id'] for c in body['candidates']]
                output=request['raw_output'].strip().splitlines();orders.setdefault(study,set()).add(tuple(display))
                for rule,match in compare(display,output).items():rows.append(dict(study=study,dataset=request['dataset'],seed=request['seed'],request_id=request['request_id'],condition=request.get('condition','original'),rule=rule,**match))
        groups=[]
        for study,count in counts.items():
            for rule in RULES:
                rs=[r for r in rows if r['study']==study and r['rule']==rule];assert len(rs)==count
                groups.append({'study':study,'rule':rule,'intended_responses':count,'defined_predictions':sum(r['defined'] for r in rs),'sequence_matches':sum(r['sequence_match'] for r in rs),'set_matches':sum(r['set_match'] for r in rs)})
        summary={'scope':'post-hoc rule equivalence audit of24 already observed responses; no inference/quality evaluation','groups':groups,'distinct_display_id_orders':{str(k):len(v) for k,v in orders.items()},'rows':rows,'new_model_calls':0,'new_objective_acquisitions':0}
        if args.verify_only:
            assert read(out/'summary.json')==summary;print('All24 measured responses/four rule comparisons reproduce exactly.')
        else:
            write(out/'summary.json',summary)
            with (ROOT/out/'rule_matches.csv').open('w',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=list(groups[0]));writer.writeheader();writer.writerows(groups)
            designs=[]
            for job in prepared.values():
                if job['condition']!='original':continue
                messages=json.loads(json.dumps(job['messages']));intro,raw=messages[-1]['content'].split('\n',1);body=json.loads(raw);assignment=nonmonotone_assignment();mapping={}
                for candidate,new_id in zip(body['candidates'],assignment):
                    mapping[new_id]=job['mapping'][candidate['id']];candidate['id']=new_id
                messages[-1]['content']=intro+'\n'+json.dumps(body,separators=(',',':'))
                designs.append({'dataset':job['dataset'],'seed':job['seed'],'messages':messages,'mapping':mapping,'rule_predictions_not_model_outputs':predictions(assignment),'actual_model_response':None,'tokenizer_checked':False})
            write('artifacts/study_v20/unexecuted_designs.json',{'namespace':'unexecuted_design_only_no_measured_outputs','authorized_for_inference':False,'designs':designs})
            print(json.dumps({'groups':groups,'distinct_display_id_orders':summary['distinct_display_id_orders']},indent=2))
        resource.checkpoint()
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==before['requests']==137 and after['active_since'] is None
    write('artifacts/study_v20/'+('replay' if args.verify_only else 'analysis')+'_accounting.json',{'before':before['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'remaining_seconds':1800-after['experiment_seconds'],'new_model_calls':0})

if __name__=='__main__':main()
