"""Independent source/decision replay and evaluator-only restricted-table bounds."""
import csv,hashlib,json,math,random,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'results/v50_utility';OUT=ROOT/'results/v50_analysis'
FEATURES={'zstd':('level','window_log','checksum'),'lz4':('level','block_id','dependent'),'zlib':('level','memory_level','filtered')}
def read(p):return json.loads(Path(p).read_text())
def lines(p):return [json.loads(s) for s in Path(p).read_text().splitlines()]
def choose(xs,order,ids,ys,cap,method):
 available=[i for i in order if i not in ids]
 if method=='random':return available[0]
 predictions=[]
 for i in available:
  neighbors=sorted(range(len(ids)),key=lambda j:sum(a!=b for a,b in zip(xs[i],xs[ids[j]])))[:3]
  predictions.append([sum(ys[j][col] for j in neighbors)/3 for col in (0,1)])
 feasible=[p for p,v in enumerate(predictions) if v[1]<=cap]
 pos=min(feasible,key=lambda p:(predictions[p][0],p)) if feasible else min(range(len(available)),key=lambda p:(predictions[p][1],predictions[p][0],p))
 return available[pos]
def main():
 assert not OUT.exists(),'Preserve original analysis'
 ledger=read(SRC/'ledger.json');assert ledger['decode_verifications']==ledger['decode_passes']==846 and ledger['recorded_vector_acquisitions']==450 and ledger['completed_cases']==15
 assert ledger['stage_seconds']<=180 and 'failure' not in ledger
 for p,h in read(ROOT/'reports/protocol_v50_utility.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 decodes=lines(SRC/'decode_results.jsonl');starts=lines(SRC/'decode_starts.jsonl');trials=lines(ROOT/'results/v17_measurements/trials.jsonl')
 assert len(decodes)==len(starts)==846
 for d,t,start in zip(decodes,trials,starts):
  assert d['trial_id']==t['trial_id']==start['trial_id'] and d['sha256']==t['compressed_sha256'] and d['decoded_sha256']==t['decoded_sha256'] and d['exact_bytes_equal']
  blob=(ROOT/t['compressed_path']).read_bytes();assert hashlib.sha256(blob).hexdigest()==d['sha256']
  if d['family']=='zstd':assert d['frame']['content_checksum']==bool(blob[4]&4)==t['setting']['checksum']
  if d['family']=='lz4':assert d['frame']['independent_blocks']==bool(blob[4]&32) and d['frame']['content_checksum']==bool(blob[4]&4)
 data=list(csv.DictReader((ROOT/'results/v17_measurements/configuration_summary.csv').open()));labels={(r['family'],r['config_id']):[float(r['median_compression_ms']),float(r['compressed_bytes'])] for r in data}
 cv={(r['family'],r['config_id']):float(r['compression_cv']) for r in data};events=lines(SRC/'acquisitions.jsonl');assert len(events)==450
 all_cases=[];datasets=read(SRC/'feature_manifest.json')['datasets']
 old=read(ROOT/'data/live_manifest_v17.json')['datasets']
 for ds in datasets:
  f=ds['system_group'];rows=ds['configurations'];prior=next(d for d in old if d['system_group']==f)['configurations']
  expected=[r for r in prior if (f=='zstd' and r['checksum']) or (f=='lz4' and not r['dependent']) or f=='zlib']
  assert rows==expected and len(rows)=={'zstd':48,'lz4':48,'zlib':90}[f]
  xs=[[r[n] for n in FEATURES[f]] for r in rows];yy=[labels[f,r['config_id']] for r in rows]
  for seed in (11,23,37,53,71):
   key=f'{f}_{seed}';prefix=read(SRC/'prefixes'/f'{key}.json');seal=read(SRC/'prefix_seals'/f'{key}.json')
   assert hashlib.sha256((SRC/'prefixes'/f'{key}.json').read_bytes()).hexdigest()==seal['sha256']
   order=list(range(len(rows)));random.Random(seed).shuffle(order);assert prefix['order']==order
   reference=prefix['reference_row'];ids=[reference]+[i for i in order if i!=reference][:3];ys=[yy[i] for i in ids];cap=ys[0][1]
   ref={'zstd':{'level':3,'window_log':19,'checksum':True},'lz4':{'level':1,'block_id':7,'dependent':False},'zlib':{'level':6,'memory_level':8,'filtered':False}}[f]
   assert all(rows[reference][k]==v for k,v in ref.items())
   while len(ids)<10:
    i=choose(xs,order,ids,ys,cap,'joint_3nn');ids.append(i);ys.append(yy[i])
   assert ids==prefix['ids'] and ys==prefix['labels'] and cap==prefix['size_cap']
   groups={'prefix':ids};arms={}
   for method in ('joint_3nn','random'):
    branch=read(SRC/method/f'{key}.json');ii=ids.copy();ys2=[y.copy() for y in ys]
    while len(ii)<20:
     i=choose(xs,order,ii,ys2,cap,method);ii.append(i);ys2.append(yy[i])
    assert len(ii)==len(set(ii))==20 and ii==branch['ids'] and ys2==branch['labels']
    best=min((yy[i][0],i) for i in ii if yy[i][1]<=cap)
    assert best==(branch['best_feasible_ms'],branch['best_row'])
    groups[method]=ii[10:];arms[method]=branch
   for method,expected_ids in groups.items():
    journal=[e for e in events if (e['family'],e['seed'],e['arm'])==(f,seed,method)]
    assert [e['row_id'] for e in journal]==expected_ids
    assert all(e['config_id']==rows[e['row_id']]['config_id'] and e['charged_recorded_vector']==1 for e in journal)
    if method!='prefix':assert seal['at']<=journal[0]['at']
   cheap=arms['joint_3nn']['best_feasible_ms'];rand=arms['random']['best_feasible_ms'];best,i=min((y[0],i) for i,y in enumerate(yy) if y[1]<=cap)
   all_cases.append({'family':f,'seed':seed,'size_cap_bytes':cap,'classical_ms':cheap,'random_ms':rand,'classical_gain_over_random':(rand-cheap)/rand,
    'hindsight_best_ms':best,'hindsight_config_id':rows[i]['config_id'],'hindsight_headroom':(cheap-best)/cheap,
    'classical_config_id':rows[arms['joint_3nn']['best_row']]['config_id'],'classical_cv':cv[f,rows[arms['joint_3nn']['best_row']]['config_id']],
    'hindsight_cv':cv[f,rows[i]['config_id']],'classical_infeasible_continuations':arms['joint_3nn']['infeasible_continuation_acquisitions']})
 family=[]
 for f in FEATURES:
  rr=[r for r in all_cases if r['family']==f]
  family.append({'family':f,'cases':5,'mean_gain_over_random':statistics.mean(r['classical_gain_over_random'] for r in rr),'wins':sum(r['classical_gain_over_random']>0 for r in rr),'ties':sum(r['classical_gain_over_random']==0 for r in rr),'harms':sum(r['classical_gain_over_random']<0 for r in rr),'mean_hindsight_headroom':statistics.mean(r['hindsight_headroom'] for r in rr),'headroom_at_least_5pct':sum(r['hindsight_headroom']>=.05 for r in rr)})
 inventory=[]
 for name in ('data/manifest_v8.json','data/manifest_v41.json'):
  for d in read(ROOT/name)['datasets']:
   inventory.append({'id':d['id'],'family':d['system_group'],'manifest':name,'features':d['feature_names'],'objectives':d['objective_columns'],
    'correctness_status':'not_certified_by_recorded_schema','qualification':'No row-level output/equivalent-utility certificate in these admitted manifests; feature semantics require original workload evidence.'})
 flags=[]
 for f in FEATURES:
  rr=[r for r in decodes if r['family']==f]
  flags.append({'family':f,'decoded':len(rr),'eligible_decodes':sum(r['eligible'] for r in rr),'checksum_false':sum(r['frame'].get('content_checksum') is False for r in rr),
   'dependent_frames':sum(r['frame'].get('independent_blocks') is False for r in rr)})
 summary={'scope':'Exploratory restricted-contract development study, no LLM or new compression runtime measurements','cases':all_cases,'families':family,'flags':flags,
  'headroom_screen_pass':sum(g['headroom_at_least_5pct']>=2 for g in family)>=2,'external_inventory':inventory,
  'cost':{**ledger,'cumulative_recorded_accesses':14708+450,'cumulative_physical_compression_trials':1274,'cumulative_model_requests_including_initial100':1976},
  'verification':{'source_events':450,'decisions_replayed':15*26,'decode_records':846,'arms':30}}
 OUT.mkdir();(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 with (OUT/'cases.csv').open('w',newline='') as stream:
  w=csv.DictWriter(stream,fieldnames=list(all_cases[0]));w.writeheader();w.writerows(all_cases)
 print(json.dumps({'families':family,'headroom_screen_pass':summary['headroom_screen_pass'],'flags':flags,'verification':summary['verification']},indent=2))
if __name__=='__main__':main()
