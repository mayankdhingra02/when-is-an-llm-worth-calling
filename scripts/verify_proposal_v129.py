"""Replay requests, independently reconstruct projection/ranking, verify acquired cells."""
import csv,json,math,random,statistics
from decimal import Decimal
from collect_smollm_v47 import ROOT,read,write,sha
from analyze_proposal_v129 import frozen,choose,OUT,references
from prepare_proposal_v128 import candidates
from proposal_v128 import messages,payload,capacity
from audit_output_capacity_v127 import vocab

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
 frozen();verify_cache();model=read(ROOT/'artifacts/study_v91/model_manifest.json');assert sha(ROOT/model['path'])==model['sha256'];tokens=vocab(ROOT/model['path']);jobs=read(ROOT/'artifacts/study_v128/jobs.json');jm={j['key']:j for j in jobs};raw=[json.loads(x) for x in (ROOT/'results/v129_merged/responses.jsonl').read_text().splitlines()];starts=[json.loads(x) for x in (ROOT/'results/v129_merged/generation_starts.jsonl').read_text().splitlines()];ledger=read(ROOT/'results/v129_merged/ledger.json');rm={r['key']:r for r in raw}
 assert len(starts)==ledger['generation_requests']<=13 and len(raw)<=len(starts) and len(rm)==len(raw);assert ledger['allocated_output_tokens']==len(starts)*1024<=13288 and ledger['retries']==1 and ledger['automatic_retries']==ledger['external_spend_usd']==0 and ledger['stage_seconds']<=2100 and ledger['peak_server_rss_bytes']<=8589934592;assert ledger['server_exit_code'] is not None and ledger['original_server_exit_code']==-9
 assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:2]]+[j['key'] for j in read(ROOT/'artifacts/study_v129/jobs.json')[:len(starts)-2]]
 for n,h in read(ROOT/'results/v129_merged/preflight_seal.json')['sha256'].items():assert sha(ROOT/n)==h,n
 for s in starts:
  j=jm[s['identity']];spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix']);pre=read(ROOT/f"results/v129_merged/preflight/{j['key']}.json");assert pre['messages']==read(ROOT/j['messages_path'])==messages(c.names,c.x,p['state'],spec['meaning'],spec['direction'],j['condition']);assert s['payload']==payload(pre['rendered']['prompt'],j['sampling_seed'],j['domains']);assert len(pre['prompt_tokens'])+1024<=4096;assert pre['output_capacity']==capacity(j['domains'],tokens,len(pre['prompt_tokens']))
  if j['key'] in rm:
   r=rm[j['key']]['response'];assert r['prompt']==s['payload']['prompt'];gs=r['generation_settings']
   for k in ['seed','n_predict','temperature','repeat_penalty','top_p','top_k','min_p','grammar']:
    assert math.isclose(gs[k],s['payload'][k],abs_tol=1e-6,rel_tol=0) if type(s['payload'][k]) is float else gs[k]==s['payload'][k],(j['key'],k)
 choices,d=choose();assert d==read(OUT/'diagnostics.json')
 for n,h in read(OUT/'selection_seal.json')['sha256'].items():assert sha(ROOT/n)==h,n
 old_events=[json.loads(x) for x in (ROOT/'results/v128_analysis/acquisitions.jsonl').read_text().splitlines()];new_events=[json.loads(x) for x in (OUT/'acquisitions.jsonl').read_text().splitlines()];assert len(old_events)==300 and len(new_events)<=90;events=[e for e in old_events if not e['key'].endswith('_model') or e['key']=='mongodb_twins_11_model']+new_events;assert len(events)==300;summary=read(OUT/'summary.json');assert summary['complete'] and summary['actual_new_acquisitions']==90 and summary['combined_new_experimental_acquisitions']==390 and summary['reused_arms']==21 and len(summary['arms'])==30;controls=0
 for ch in choices:
  assert ch==read(OUT/'choices'/f"{ch['key']}.json");p=read(ROOT/ch['prefix'])['state'];spec,c=candidates(ch['dataset']);batch=independent_batch(c.x,p,spec['direction'])
  if ch['mode']=='full_batch_3nn' or ch['fallback']:selected=batch
  else:
   if ch['mode']=='random_projection':
    rng=random.Random(ch['random_proposal_seed']);proposals=[tuple(rng.choice(d) for d in ch['domains']) for _ in range(10)]
   else:
    rr=rm[ch['request_key']]['response'];encoded=json.loads(rr['content']);assert len(encoded)==10;alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';proposals=[tuple(dom[alphabet.index(symbol)] for dom,symbol in zip(ch['domains'],x)) for x in encoded]
   selected=independent_project(c.x,p['order'],p['ids'],proposals)
  assert ch['selected_rows']==selected;es=[e for e in events if e['key']==ch['key']];assert [e['row_id'] for e in es]==selected
  lines=(ROOT/spec['path']).read_text().splitlines();header=next(csv.reader([lines[0]],delimiter=spec['delimiter']));ys=[]
  for e in es:
   assert e['source_line']==c.source_ids[e['row_id']];row=dict(zip(header,next(csv.reader([lines[e['source_line']-1]],delimiter=spec['delimiter']))));assert row[spec['primary_objective']]==e['raw_target'];assert tuple(float(row[n]) for n in c.names)==c.x[e['row_id']];ys.append([float(e['raw_target'])])
  a=read(OUT/'arms'/f"{ch['key']}.json");s=a['state'];assert s['order']==p['order'] and s['ids']==p['ids']+selected and s['labels']==p['labels']+ys and len(set(s['ids']))==20;opt=min if spec['direction']=='-' else max;assert a['target']==opt(y[0] for y in s['labels']);assert a['references']==references(ch,read(ROOT/ch['prefix']),spec['direction'])
 result=read(OUT/'comparison.json');assert len(result['cases'])==10;am={a['key']:a for a in summary['arms']}
 for r in result['cases']:
  a=am[r['key']+'_model'];assert r['target']==a['target'] and r['fallback']==a['fallback'];refs={**a['references'],**{m:am[r['key']+'_'+m]['target'] for m in ['random_projection','full_batch_3nn']}};assert r['references']==refs
  for m,v in refs.items():assert math.isclose(r['gains'][m],(v-r['target'])/v*(1 if a['direction']=='-' else -1),rel_tol=0,abs_tol=1e-15)
 for m,v in result['contrasts'].items():
  rs=[r for r in result['cases'] if m in r['gains']];assert v['cases']==len(rs);groups={r['system_group'] for r in rs};assert v['equal_family_mean']==statistics.mean(statistics.mean(r['gains'][m] for r in rs if r['system_group']==g) for g in sorted(groups));assert v['wins']+v['ties']+v['losses']==len(rs)
 receipt={'verified':True,'real_requests_replayed':len(starts),'returned_responses':len(raw),'source_events_replayed':300,'total_two_stage_acquisitions':390,'paired_arms':30,'exposed_families':2,'cases':10,'new_acquisitions':0,'new_inference':0};write(ROOT/'artifacts/study_v129/verification.json',receipt);print(receipt)
if __name__=='__main__':main()
