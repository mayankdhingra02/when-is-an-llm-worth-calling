"""Read-only independent audit of raw physical and optimizer event denominators."""
import csv,hashlib,json,math,random,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def main():
 for version,name in ((50,'utility'),(51,'interface')):
  for p,h in read(f'reports/protocol_v{version}_{name}.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 trials=lines('results/v51_interfaces/trials.jsonl');events=lines('results/v51_interfaces/acquisitions.jsonl');ledger=read('results/v51_interfaces/ledger.json');summary=read('results/v51_analysis/summary.json')
 assert len(trials)==len(events)==ledger['physical_attempts']==ledger['ok']==960 and ledger['failed']==0
 work=read('artifacts/study_v15/workload_manifest.json')
 for t,e in zip(trials,events):
  assert t['trial_id']==e['trial_id'] and t['setting']==e['setting'] and t['mode']==e['mode'] and e['charged_physical_vector']==1
  b=(ROOT/t['compressed_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==t['compressed_sha256'] and len(b)==t['compressed_bytes']
  assert t['roundtrip_equal'] and t['decoded_sha256']==work['workload_sha256']
  assert b[4]&4 # content-checksum flags share bit2
  if t['setting']['family']=='lz4':assert b[4]&32
 for s in summary['settings']:
  rr=[t for t in trials if t['setting']['config_id']==s['config_id']];modes={m:sorted([t for t in rr if t['mode']==m],key=lambda r:r['repetition']) for m in ('api','cli')}
  assert len(modes['api'])==len(modes['cli'])==5
  ratios=[c['compression_ns']/a['compression_ns'] for a,c in zip(modes['api'],modes['cli'])]
  assert math.isclose(s['median_cli_over_api_time_ratio'],statistics.median(ratios))
  assert s['byte_equal_pairs']==sum(a['compressed_sha256']==c['compressed_sha256'] for a,c in zip(modes['api'],modes['cli']))
  assert s['size_equal_pairs']==sum(a['compressed_bytes']==c['compressed_bytes'] for a,c in zip(modes['api'],modes['cli']))
 for g in summary['families']:
  ss=[s for s in summary['settings'] if s['family']==g['family']]
  assert len(ss)==48 and math.isclose(g['median_setting_cli_over_api_ratio'],statistics.median(s['median_cli_over_api_time_ratio'] for s in ss))
  assert g['byte_equal_pairs']==sum(s['byte_equal_pairs'] for s in ss)
 journal=lines('results/v51_classical/acquisitions.jsonl');assert len(journal)==600
 datasets=read('results/v50_utility/feature_manifest.json')['datasets'];cases=read('results/v51_classical/cases.json');assert len(cases)==20
 for case in cases:
  f=case['family'];mode=case['mode'];seed=case['seed'];key=f'{mode}_{f}_{seed}'
  d=next(d for d in datasets if d['system_group']==f);configs=d['configurations'];table={r['config_id']:r for r in csv.DictReader((ROOT/f'results/v51_analysis/{mode}/configuration_summary.csv').open())}
  prefix=read(f'results/v51_classical/prefixes/{key}.json');order=list(range(len(configs)));random.Random(seed).shuffle(order);assert prefix['order']==order
  ref=prefix['reference_row'];assert prefix['ids'][:4]==[ref]+[i for i in order if i!=ref][:3]
  for arm in ('prefix','joint_3nn','random'):
   record=prefix if arm=='prefix' else read(f'results/v51_classical/{arm}/{key}.json');rows=record['ids'];yy=record['labels']
   if arm!='prefix':assert rows[:10]==prefix['ids'] and yy[:10]==prefix['labels'] and len(set(rows))==20
   for i,y in zip(rows,yy):
    r=table[configs[i]['config_id']];assert y==[float(r['median_compression_ms']),float(r['compressed_bytes'])]
   events=[e for e in journal if (e['mode'],e['family'],e['seed'],e['arm'])==(mode,f,seed,arm)]
   expected=rows if arm=='prefix' else rows[10:]
   assert [e['row_id'] for e in events]==expected
   assert all(e['config_id']==configs[e['row_id']]['config_id'] and e['charged_recorded_vector']==1 for e in events)
   if arm!='prefix':assert record['best_feasible_ms']==min(y[0] for y in yy if y[1]<=prefix['size_cap'])
  full=[float(table[c['config_id']]['median_compression_ms']) for c in configs if float(table[c['config_id']]['compressed_bytes'])<=prefix['size_cap']]
  assert case['hindsight_ms']==min(full)
  assert math.isclose(case['hindsight_headroom'],(case['classical_ms']-min(full))/case['classical_ms'],abs_tol=1e-12)
  assert math.isclose(case['classical_gain_over_random'],(case['random_ms']-case['classical_ms'])/case['random_ms'],abs_tol=1e-12)
 print(json.dumps({'verified':True,'physical_attempts':960,'output_hashes':960,'native_cli_pairs':480,'recorded_vector_events':600,'classical_cases':20,'classical_arms':40,'new_compressions_in_verifier':0,'note':'Read-only replay; physical roundtrips executed in original workers, not rerun here. Frozen replay separately reconstructed acquired-only choices.'},indent=2))
if __name__=='__main__':main()
