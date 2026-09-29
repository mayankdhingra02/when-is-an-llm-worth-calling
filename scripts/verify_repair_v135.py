"""Independent stdlib replay of capacity repair, projection and acquired rows."""
import argparse,csv,hashlib,json,random
from pathlib import Path
from decimal import Decimal
from fractions import Fraction
ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--compact',action='store_true');args=ap.parse_args();root=args.root
 def read(n):return json.loads((root/n).read_text())
 def sha(n):return hashlib.sha256((root/n).read_bytes()).hexdigest()
 def lines(n):return [json.loads(l) for l in (root/n).read_text().splitlines()]
 if not args.compact:
  for n,h in read('reports/protocol_v135.freeze.json')['sha256'].items():assert sha(n)==h,n
 for n,h in read('artifacts/study_v135/inputs.freeze.json')['sha256'].items():assert sha(n)==h,n
 jobs=read('artifacts/study_v135/jobs.json');cand=read('artifacts/study_v135/candidates.json');xs=cand['x'];spec=cand['source_spec'];ds=[sorted({x[i] for x in xs}) for i in range(59)];assert len(xs)==1024 and len(ds)==59
 raw=lines('results/v135_proposals/responses.jsonl');gens=lines('results/v135_proposals/generation_starts.jsonl');ledger=read('results/v135_proposals/ledger.json');journal=lines('results/v135_analysis/acquisitions.jsonl');summary=read('results/v135_analysis/summary.json');seal=read('results/v135_analysis/selection_seal.json');result=read('results/v135_analysis/comparison.json')
 assert len(jobs)==len(raw)==len(gens)==ledger['generation_requests']==5 and ledger['allocated_output_tokens']==5120 and ledger['retries']==0 and ledger['server_exit_code']==0 and ledger['stage_seconds']<=600 and ledger['peak_server_rss_bytes']<=8589934592
 assert len(journal)==summary['new_recorded_acquisitions']==50 and summary['complete'] and summary['evaluation_seconds']<=180
 for n,h in seal['sha256'].items():assert sha(n)==h,n
 assert all(r['at']>seal['at'] for r in journal)
 extract=read('artifacts/study_v135/acquired_source_rows.json');assert extract['source_sha256']==spec['sha256'] and extract['source_path']==spec['path']
 if not args.compact:
  assert sha(spec['path'])==spec['sha256'];source=(root/spec['path']).read_text().splitlines();assert extract['header']==source[0]
  for line,value in extract['rows'].items():assert source[int(line)-1]==value
 header=next(csv.reader([extract['header']],delimiter=spec['delimiter']));arms=summary['arms'];assert len(arms)==5
 for j in jobs:
  p=read(j['prefix'])['state'];assert sha(j['prefix'])==j['prefix_sha256'];assert read(j['messages_path'])==read(j['old_messages_path']) and j['domains']==ds;key=j['key'];response=next(r for r in raw if r['key']==key)['response'];pf=read(f'results/v135_proposals/preflight/{key}.json');payload=next(g for g in gens if g['identity']==key)['payload'];assert payload['seed']==127000+j['seed'] and payload['n_predict']==1024 and payload['prompt']==pf['rendered']['prompt']
  proof=pf['output_capacity'];assert proof['constructive_token_upper_bound_including_eos']==622 and len(pf['prompt_tokens'])+1024<=4096 and pf['messages']==read(j['messages_path'])
  assert response['stop_type']=='eos' and response['truncated'] is False and 0<response['tokens_predicted']<=1024;coded=json.loads(response['content']);assert len(coded)==10 and response['content']==json.dumps(coded,separators=(',',':'));assert all(len(c)==59 and all(ch in ALPHABET[:len(d)] for ch,d in zip(c,ds)) for c in coded)
  props=[tuple(d[ALPHABET.index(ch)] for ch,d in zip(c,ds)) for c in coded];seen=set(p['ids']);selected=[]
  for prop in props:
   row=min([r for r in p['order'] if r not in seen],key=lambda r:sum(a!=b for a,b in zip(prop,xs[r])));selected.append(row);seen.add(row)
  choice=read(f'results/v135_analysis/choices/{key}.json');assert choice['selected_rows']==selected and not choice['fallback'];arm=next(a for a in arms if a['key']==key);assert arm==read(f'results/v135_analysis/arms/{key}.json');records=[r for r in journal if r['key']==key];assert len(records)==10 and [r['row_id'] for r in records]==selected
  ys=[]
  for row,event in zip(selected,records):
   source_line=cand['source_ids'][row];assert event['source_line']==source_line;cells=dict(zip(header,next(csv.reader([extract['rows'][str(source_line)]],delimiter=spec['delimiter']))));assert [float(cells[k]) for k in cand['names']]==xs[row] and cells[spec['primary_objective']]==event['raw_target'];ys.append([float(event['raw_target'])])
  state=arm['state'];assert state['order']==p['order'] and state['ids']==p['ids']+selected and state['labels']==p['labels']+ys and len(set(state['ids']))==20;assert arm['direction']=='-' and arm['target']==min(y[0] for y in state['labels']) and arm['prefix_best']==min(y[0] for y in p['labels'])
  for mode in ['batch_3nn','full_sequential_3nn','random_full']:
   old=read(f'results/v41_transfer/arms/{j["base_key"]}_{mode}.json')['state'];assert old['ids'][:10]==p['ids'] and old['labels'][:10]==p['labels'] and arm['references'][mode]==min(y[0] for y in old['labels'])
  optional={'presentation_first10':f'results/v41_models/0.5/arms/{j["base_key"]}.json','single_portfolio':f'results/v115_portfolio/arms/{j["base_key"]}.json'}
  for mode,path in optional.items():
   if mode in arm['references']:
    prior=read(path)['state'];assert prior['ids'][:10]==p['ids'] and prior['labels'][:10]==p['labels'] and len(prior['ids'])==20 and arm['references'][mode]==min(y[0] for y in prior['labels'])
  old=read(f'results/v127_analysis/arms/{j["base_key"]}_model.json');assert old['fallback'] and old['target']==arm['old_failed_contract_target'] and old['state']['ids'][:10]==p['ids'];assert not arm['fallback'] and arm['model_status']=='valid'
  r=next(r for r in result['rows'] if r['seed']==j['seed']);assert r['new_target']==arm['target'] and r['old_fallback_target']==old['target'] and r['sequential_target']==arm['references']['full_sequential_3nn'] and r['prefix_best']==arm['prefix_best']
 assert result['valid']==5 and result['fallbacks']==0 and result['improved_prefix']==sum(a['target']<a['prefix_best'] for a in arms)
 for mode,c in result['comparisons'].items():
  gs=[(Fraction(str(a['references'][mode]))-Fraction(str(a['target'])))/Fraction(str(a['references'][mode])) for a in arms if mode in a['references']];assert c['cases']==len(gs) and c['mean_fraction']==str(sum(gs)/len(gs)) and c['wins']==sum(g>0 for g in gs) and c['ties']==sum(g==0 for g in gs) and c['losses']==sum(g<0 for g in gs)
 assert result['usage']['generated_observed']==sum(r['response']['tokens_predicted'] for r in raw) and result['usage']['prefill_observed']==sum(r['response']['tokens_evaluated'] for r in raw) and result['usage']['missing_usage']==0
 print(json.dumps({'verified':True,'compact':args.compact,'same_prompt_prefix_cases':5,'valid_real_responses':5,'new_charged_recorded_accesses':50,'constructive_capacity_tokens':622,'B20_arms':5,'new_collection':0}))
if __name__=='__main__':main()
