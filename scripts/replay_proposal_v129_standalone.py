"""Replay requests, independently reconstruct projection/ranking, verify acquired cells."""
import csv,json,math,random,statistics
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from functools import lru_cache
import hashlib,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from proposal_v128 import messages,payload,parse,project
OUT=ROOT/'results/v129_analysis'
def read(p):return json.loads(Path(p if Path(p).is_absolute() else ROOT/p).read_text())
def sha(p):return hashlib.sha256(Path(p if Path(p).is_absolute() else ROOT/p).read_bytes()).hexdigest()
def write(p,v):pass  # Portable replay does not mutate evidence.
def frozen():
 m=read(ROOT/'manifest.json')
 for n,v in m['files'].items():assert sha(ROOT/n)==v['sha256'] and (ROOT/n).stat().st_size==v['bytes'],n
 for n,h in read(ROOT/'reports/protocol_v129.freeze.json')['sha256'].items():
  if (ROOT/n).is_file():assert sha(ROOT/n)==h,n
@lru_cache(maxsize=2)
def candidates(dataset):
 version={'wc_5d_c5':119,'mongodb_twins':121}[dataset]
 spec=read(ROOT/f'data/manifest_v{version}.json')['datasets'][0]
 assert sha(ROOT/spec['path'])==spec['sha256']
 with (ROOT/spec['path']).open(newline='') as f:
  xs=[];source_ids=[];seen=set()
  for line,row in enumerate(csv.DictReader(f,delimiter=spec['delimiter']),2):
   if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
   x=tuple(float(row[n]) for n in spec['feature_names'])
   if x in seen:continue
   seen.add(x);xs.append(x);source_ids.append(line)
 assert len(xs)==spec['rows']
 eligible=[i for i,x in enumerate(xs) if all(x[spec['feature_names'].index(k)]==v for k,v in spec['fixed_features'].items())]
 if len(eligible)>1024:
  def key(i):return hashlib.sha256(json.dumps({'salt':'v41','x':xs[i]},sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest(),i
  eligible=sorted(eligible,key=key)[:1024]
 eligible.sort()
 return spec,SimpleNamespace(x=tuple(xs[i] for i in eligible),names=spec['feature_names'],source_ids=[source_ids[i] for i in eligible])

def references(j,p,direction):
 refs={};opt=min if direction=='-' else max
 version=j['classical_version']
 paths={m:f"results/v{version}_classical/arms/{j['base_key']}_{m}.json" for m in ['batch_3nn','full_sequential_3nn','random_full','single_portfolio']}
 paths['presentation_first10']=(f"results/v120_analysis/arms/{j['base_key']}.json" if version==119 else f"results/v121_classical/arms/{j['base_key']}_presentation_first10.json")
 for m,n in paths.items():
  s=read(ROOT/n)['state'];assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels'] and len(s['ids'])==len(set(s['ids']))==20
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

def verify_cache():
 links=read(ROOT/'results/v129_merged/cache_links.json')['links']
 assert len({r['key'] for r in links})==len(links)
 view={r['key']:r for r in [json.loads(x) for x in (ROOT/'results/v129_merged/responses.jsonl').read_text().splitlines()]}
 for r in links:
  assert sha(ROOT/r['source'])==r['source_sha256']
  source={x['key']:x for x in [json.loads(line) for line in (ROOT/r['source']).read_text().splitlines()]}
  assert view[r['key']]==source[r['key']]
 new=read(ROOT/'results/v129_proposals/ledger.json')
 assert new['generation_requests']<=11 and new['allocated_output_tokens']<=11264 and new['stage_seconds']<=1200 and new['peak_server_rss_bytes']<=8589934592 and new['retries']==0

def main():
 frozen();verify_cache();jobs=read(ROOT/'artifacts/study_v128/jobs.json');jm={j['key']:j for j in jobs};raw=[json.loads(x) for x in (ROOT/'results/v129_merged/responses.jsonl').read_text().splitlines()];starts=[json.loads(x) for x in (ROOT/'results/v129_merged/generation_starts.jsonl').read_text().splitlines()];ledger=read(ROOT/'results/v129_merged/ledger.json');rm={r['key']:r for r in raw}
 assert len(starts)==ledger['generation_requests']<=13 and len(raw)<=len(starts) and len(rm)==len(raw);assert ledger['allocated_output_tokens']==len(starts)*1024<=13312 and ledger['retries']==1 and ledger['automatic_retries']==ledger['external_spend_usd']==0 and ledger['stage_seconds']<=2100 and ledger['peak_server_rss_bytes']<=8589934592;assert ledger['server_exit_code']==0 and ledger['original_server_exit_code']==-9
 assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:2]]+[j['key'] for j in read(ROOT/'artifacts/study_v129/jobs.json')[:len(starts)-2]]
 for n,h in read(ROOT/'results/v129_merged/preflight_seal.json')['sha256'].items():assert sha(ROOT/n)==h,n
 for s in starts:
  j=jm[s['identity']];spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix']);pre=read(ROOT/f"results/v129_merged/preflight/{j['key']}.json");assert pre['messages']==read(ROOT/j['messages_path'])==messages(c.names,c.x,p['state'],spec['meaning'],spec['direction'],j['condition']);assert s['payload']==payload(pre['rendered']['prompt'],j['sampling_seed'],j['domains']);assert len(pre['prompt_tokens'])+1024<=4096
  if j['key'] in rm:
   r=rm[j['key']]['response'];assert r['prompt']==s['payload']['prompt'];gs=r['generation_settings']
   for k in ['seed','n_predict','temperature','repeat_penalty','top_p','top_k','min_p','grammar']:
    assert math.isclose(gs[k],s['payload'][k],abs_tol=1e-6,rel_tol=0) if type(s['payload'][k]) is float else gs[k]==s['payload'][k],(j['key'],k)
 choices=[read(p) for p in sorted((OUT/'choices').glob('*.json'))];d=read(OUT/'diagnostics.json');assert len(choices)==30
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
 old_events=[json.loads(x) for x in (ROOT/'results/v128_analysis/acquisitions.jsonl').read_text().splitlines()];new_events=[json.loads(x) for x in (OUT/'acquisitions.jsonl').read_text().splitlines()];assert len(old_events)==300 and len(new_events)==90;events=[e for e in old_events if not e['key'].endswith('_model') or e['key']=='mongodb_twins_11_model']+new_events;assert len(events)==300;summary=read(OUT/'summary.json');assert summary['complete'] and summary['actual_new_acquisitions']==90 and summary['combined_new_experimental_acquisitions']==390 and summary['reused_arms']==21 and len(summary['arms'])==30;controls=0
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
 result=read(OUT/'comparison.json');assert len(result['cases'])==10;am={a['key']:a for a in summary['arms']}
 for r in result['cases']:
  a=am[r['key']+'_model'];assert r['target']==a['target'] and r['fallback']==a['fallback'];refs={**a['references'],**{m:am[r['key']+'_'+m]['target'] for m in ['random_projection','full_batch_3nn']}};assert r['references']==refs
  for m,v in refs.items():assert math.isclose(r['gains'][m],(v-r['target'])/v*(1 if a['direction']=='-' else -1),rel_tol=0,abs_tol=1e-15)
 for m,v in result['contrasts'].items():
  rs=[r for r in result['cases'] if m in r['gains']];assert v['cases']==len(rs);groups={r['system_group'] for r in rs};assert v['equal_family_mean']==statistics.mean(statistics.mean(r['gains'][m] for r in rs if r['system_group']==g) for g in sorted(groups));assert v['wins']==sum(r['gains'][m]>1e-12 for r in rs);assert v['ties']==sum(abs(r['gains'][m])<=1e-12 for r in rs);assert v['losses']==sum(r['gains'][m]<-1e-12 for r in rs)
 assert result['normal_valid']==sum(r['condition']=='normal' and r['status']=='valid' for r in d['requests'])
 from fractions import Fraction
 env=read(OUT/'policy_envelope.json');rs=result['cases'];groups={r['system_group'] for r in rs}
 assert env['source_sha256']==sha(OUT/'comparison.json') and env['case_order']==[r['key'] for r in rs]
 gains=[(Fraction(str(r['references']['full_sequential_3nn']))-Fraction(str(r['target'])))/Fraction(str(r['references']['full_sequential_3nn'])) for r in rs]
 weights=[Fraction(1,len(groups)*sum(x['system_group']==r['system_group'] for x in rs)) for r in rs]
 assert len(env['masks'])==1<<len(rs)
 for mask,row in enumerate(env['masks']):
  gain=sum((w*g for i,(w,g) in enumerate(zip(weights,gains)) if mask>>i&1),Fraction(0))
  assert row['mask']==format(mask,f'0{len(rs)}b') and row['calls']==mask.bit_count()
  assert row['gain_numerator']==gain.numerator and row['gain_denominator']==gain.denominator and row['mean_relative_gain']==float(gain)
 assert env['positive_gain_policies']==sum(m['gain_numerator']>0 for m in env['masks'])
 assert env['zero_gain_policies']==sum(m['gain_numerator']==0 for m in env['masks'])
 assert env['never_dominates_all_nonempty_policies_in_quality_and_calls']==all(g<=0 for g in gains)
 assert env['observed_hindsight_gain']==float(sum((w*max(g,Fraction(0)) for w,g in zip(weights,gains)),Fraction(0)))

 receipt={'verified':True,'real_requests_replayed':len(starts),'returned_responses':len(raw),'source_events_replayed':300,'total_two_stage_acquisitions':390,'paired_arms':30,'exposed_families':2,'cases':10,'new_acquisitions':0,'new_inference':0};write(ROOT/'artifacts/study_v128/verification.json',receipt);print(receipt)
if __name__=='__main__':
 import runpy
 main()
 runpy.run_path(str(ROOT/'replay_original.py'),run_name='__main__')
