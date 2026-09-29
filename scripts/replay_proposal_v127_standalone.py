"""Replay requests, independently reconstruct projection/ranking, verify acquired cells."""
import csv,json,math,random,statistics
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from functools import lru_cache
import hashlib,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from proposal_v127 import messages,payload,parse,project
OUT=ROOT/'results/v127_analysis'
def read(p):return json.loads(Path(p if Path(p).is_absolute() else ROOT/p).read_text())
def sha(p):return hashlib.sha256(Path(p if Path(p).is_absolute() else ROOT/p).read_bytes()).hexdigest()
def write(p,v):pass  # Portable replay does not mutate evidence.
def frozen():
 m=read(ROOT/'manifest.json')
 for n,v in m['files'].items():assert sha(ROOT/n)==v['sha256'] and (ROOT/n).stat().st_size==v['bytes'],n
 for n,h in read(ROOT/'reports/protocol_v127.freeze.json')['sha256'].items():
  if (ROOT/n).is_file():assert sha(ROOT/n)==h,n
@lru_cache(maxsize=6)
def candidates(dataset):
 spec=next(s for s in read(ROOT/'data/manifest_v41.json')['datasets'] if s['id']==dataset)
 lines=(ROOT/spec['path']).read_text().splitlines();header=next(csv.reader([lines[0]],delimiter=spec['delimiter']));xs=[]
 for line in spec['subset']['source_lines']:
  row=dict(zip(header,next(csv.reader([lines[line-1]],delimiter=spec['delimiter']))));xs.append(tuple(float(row[n]) for n in spec['feature_names']))
 return spec,SimpleNamespace(x=tuple(xs),names=spec['feature_names'],source_ids=spec['subset']['source_lines'])
def references(j,p,direction):
 refs={};opt=min if direction=='-' else max
 paths={**{m:f"results/v41_transfer/arms/{j['base_key']}_{m}.json" for m in ['batch_3nn','full_sequential_3nn','random_full']},'presentation_first10':f"results/v41_models/0.5/arms/{j['base_key']}.json",'single_portfolio':f"results/v115_portfolio/arms/{j['base_key']}.json"}
 for m,n in paths.items():
  if not (ROOT/n).exists():assert m=='single_portfolio';continue
  s=read(ROOT/n)['state'];assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels'] and len(set(s['ids']))==20
  if m=='presentation_first10':assert s['ids'][10:]==[p['pool']['mapping'][i] for i in '0123456789']
  refs[m]=opt(y[0] for y in s['labels'])
 return refs

def independent_project(xs,order,seen,proposals):
 seen=set(seen);rows=[]
 for x in proposals:
  scores=[(sum(a!=b for a,b in zip(xs[i],x)),k,i) for k,i in enumerate(order) if i not in seen]
  i=min(scores)[2];rows.append(i);seen.add(i)
 return rows

def independent_batch(xs,p,direction):
 scores=[]
 for i in p['order']:
  if i in p['ids']:continue
  near=sorted(range(10),key=lambda k:sum(a!=b for a,b in zip(xs[p['ids'][k]],xs[i])))[:3]
  value=sum(Decimal(str(p['labels'][k][0])) for k in near)/3;scores.append((value if direction=='-' else -value,i))
 return [i for _,i in sorted(scores,key=lambda item:item[0])[:10]]

def main():
 frozen();jobs=read(ROOT/'artifacts/study_v127/jobs.json');jm={j['key']:j for j in jobs};raw=[json.loads(x) for x in (ROOT/'results/v127_proposals/responses.jsonl').read_text().splitlines()];starts=[json.loads(x) for x in (ROOT/'results/v127_proposals/generation_starts.jsonl').read_text().splitlines()];ledger=read(ROOT/'results/v127_proposals/ledger.json');rm={r['key']:r for r in raw}
 assert len(starts)==ledger['generation_requests']<=36 and len(raw)<=len(starts) and len(rm)==len(raw);assert ledger['allocated_output_tokens']==len(starts)*512<=18432 and ledger['retries']==ledger['external_spend_usd']==0 and ledger['stage_seconds']<=1800 and ledger['peak_server_rss_bytes']<=8589934592;assert ledger['server_exit_code']==0
 assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:len(starts)]]
 for n,h in read(ROOT/'results/v127_proposals/preflight_seal.json')['sha256'].items():assert sha(ROOT/n)==h,n
 for s in starts:
  j=jm[s['identity']];spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix']);pre=read(ROOT/f"results/v127_proposals/preflight/{j['key']}.json");assert pre['messages']==read(ROOT/j['messages_path'])==messages(c.names,c.x,p['state'],spec['meaning'],spec['direction'],j['condition']);assert s['payload']==payload(pre['rendered']['prompt'],j['sampling_seed'],j['domains']);assert len(pre['prompt_tokens'])+512<=4096
  if j['key'] in rm:
   r=rm[j['key']]['response'];assert r['prompt']==s['payload']['prompt'];gs=r['generation_settings']
   for k in ['seed','n_predict','temperature','repeat_penalty','top_p','top_k','min_p','grammar']:
    assert math.isclose(gs[k],s['payload'][k],abs_tol=1e-6,rel_tol=0) if type(s['payload'][k]) is float else gs[k]==s['payload'][k],(j['key'],k)
 choices=[read(p) for p in sorted((OUT/'choices').glob('*.json'))];d=read(OUT/'diagnostics.json');assert len(choices)==90
 dm={r['key']:r for r in d['requests']};assert set(dm)==set(jm)
 for j in jobs:
  dd=dm[j['key']];r=rm.get(j['key']);spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix'])['state']
  try:
   if r is None:raise ValueError('No returned response')
   props=parse(r['response'],j['domains']);selected,detail=project(props,c.x,p)
  except ValueError:
   assert dd['status']==('missing' if r is None else 'invalid') and dd['selected_rows'] is None
  else:assert dd['status']=='valid' and dd['selected_rows']==independent_project(c.x,p['order'],p['ids'],props)==selected and dd['projection']==detail
 for r in d['label_rotation_probes']:
  a=dm[r['key']+'_normal']['selected_rows'];b=dm[r['key']+'_rotated_labels']['selected_rows'];valid=a is not None and b is not None;assert r['both_valid']==valid
  if valid:assert r['selection_set_overlap']==len(set(a)&set(b)) and r['same_order']==(a==b)
 for n,h in read(OUT/'selection_seal.json')['sha256'].items():assert sha(ROOT/n)==h,n
 events=[json.loads(x) for x in (OUT/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==900;summary=read(OUT/'summary.json');assert summary['complete'] and summary['actual_new_acquisitions']==900 and len(summary['arms'])==90;controls=0
 for ch in choices:
  assert ch==read(OUT/'choices'/f"{ch['key']}.json");p=read(ROOT/ch['prefix'])['state'];spec,c=candidates(ch['dataset']);batch=independent_batch(c.x,p,spec['direction'])
  if ch['mode']=='full_batch_3nn' or ch['fallback']:selected=batch
  else:
   if ch['mode']=='random_projection':
    rng=random.Random(ch['random_proposal_seed']);proposals=[tuple(rng.choice(d) for d in ch['domains']) for _ in range(10)]
   else:
    rr=rm[ch['request_key']]['response'];encoded=json.loads(rr['content']);assert len(encoded)==10;alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';proposals=[tuple(dom[alphabet.index(symbol)] for dom,symbol in zip(ch['domains'],x)) for x in encoded]
   selected=independent_project(c.x,p['order'],p['ids'],proposals)
  assert ch['fallback']==(ch['mode']=='model' and dm[ch['request_key']]['status']!='valid');assert ch['selected_rows']==selected;es=[e for e in events if e['key']==ch['key']];assert [e['row_id'] for e in es]==selected
  lines=(ROOT/spec['path']).read_text().splitlines();header=next(csv.reader([lines[0]],delimiter=spec['delimiter']));ys=[]
  for e in es:
   assert e['source_line']==c.source_ids[e['row_id']];row=dict(zip(header,next(csv.reader([lines[e['source_line']-1]],delimiter=spec['delimiter']))));assert row[spec['primary_objective']]==e['raw_target'];assert tuple(float(row[n]) for n in c.names)==c.x[e['row_id']];ys.append([float(e['raw_target'])])
  a=read(OUT/'arms'/f"{ch['key']}.json");s=a['state'];assert s['order']==p['order'] and s['ids']==p['ids']+selected and s['labels']==p['labels']+ys and len(set(s['ids']))==20;opt=min if spec['direction']=='-' else max;assert a['target']==opt(y[0] for y in s['labels']);assert a['references']==references(ch,read(ROOT/ch['prefix']),spec['direction'])
 result=read(OUT/'comparison.json');assert len(result['cases'])==30;am={a['key']:a for a in summary['arms']}
 for r in result['cases']:
  a=am[r['key']+'_model'];assert r['target']==a['target'] and r['fallback']==a['fallback'];refs={**a['references'],**{m:am[r['key']+'_'+m]['target'] for m in ['random_projection','full_batch_3nn']}};assert r['references']==refs
  for m,v in refs.items():assert math.isclose(r['gains'][m],(v-r['target'])/v*(1 if a['direction']=='-' else -1),rel_tol=0,abs_tol=1e-15)
 for m,v in result['contrasts'].items():
  rs=[r for r in result['cases'] if m in r['gains']];assert v['cases']==len(rs);groups={r['system_group'] for r in rs};assert v['equal_family_mean']==statistics.mean(statistics.mean(r['gains'][m] for r in rs if r['system_group']==g) for g in sorted(groups));assert v['wins']==sum(r['gains'][m]>1e-12 for r in rs);assert v['ties']==sum(abs(r['gains'][m])<=1e-12 for r in rs);assert v['losses']==sum(r['gains'][m]<-1e-12 for r in rs)
 primary=['full_sequential_3nn','random_projection','full_batch_3nn'];joint=sum(all(r['gains'][m]>=.05 for m in primary) for r in result['cases']);assert result['joint_5pct_cases']==joint;assert result['normal_valid']==sum(r['condition']=='normal' and r['status']=='valid' for r in d['requests'])
 receipt={'verified':True,'real_requests_replayed':len(starts),'returned_responses':len(raw),'source_events_replayed':900,'paired_arms':90,'exposed_families':6,'cases':30,'new_acquisitions':0,'new_inference':0};write(ROOT/'artifacts/study_v127/verification.json',receipt);print(receipt)
if __name__=='__main__':main()
