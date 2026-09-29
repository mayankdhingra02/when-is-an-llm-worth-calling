"""Verify physical pairs, preserve all timing observations, build bound median tables."""
import csv,hashlib,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'results/v51_interfaces';OUT=ROOT/'results/v51_analysis'
def read(p):return json.loads(Path(p).read_text())
def main():
 assert not OUT.exists(),'Preserve analysis'
 trials=[json.loads(s) for s in (SRC/'trials.jsonl').read_text().splitlines()];charges=[json.loads(s) for s in (SRC/'acquisitions.jsonl').read_text().splitlines()];schedule=read(SRC/'schedule.json');ledger=read(SRC/'ledger.json')
 assert len(trials)==len(charges)==len(schedule)==ledger['ok']==ledger['physical_attempts']==960 and ledger['failed']==0
 assert ledger['stage_seconds']<=180 and ledger['unattempted']==0
 for p,h in read(ROOT/'reports/protocol_v51_interface.freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 for t,c,j in zip(trials,charges,schedule):
  assert t['trial_id']==c['trial_id']==j['trial_id'] and c['charged_physical_vector']==1 and t['status']=='ok'
  assert t['mode']==c['mode']==j['mode'] and t['setting']==c['setting']==j['setting']
  blob=(ROOT/t['compressed_path']).read_bytes();assert hashlib.sha256(blob).hexdigest()==t['compressed_sha256'] and len(blob)==t['compressed_bytes']
  assert t['roundtrip_equal'] and t['compression_ns']>0 and t['frame']['content_checksum']
  if t['setting']['family']=='lz4':assert t['frame']['independent_blocks']
 from collect_interface_v51 import schedule as regenerate
 assert schedule==regenerate(read(ROOT/'results/v50_utility/feature_manifest.json')['datasets'])
 ids=sorted({t['setting']['config_id'] for t in trials});settings=[];table={mode:[] for mode in ('api','cli')}
 for cid in ids:
  tt=[t for t in trials if t['setting']['config_id']==cid];f=tt[0]['setting']['family'];repeats={mode:sorted([t for t in tt if t['mode']==mode],key=lambda t:t['repetition']) for mode in ('api','cli')}
  assert all(len(rr)==5 and [r['repetition'] for r in rr]==list(range(5)) for rr in repeats.values())
  ratios=[];same_bytes=0;same_size=0
  for a,c in zip(repeats['api'],repeats['cli']):
   ratios.append(c['compression_ns']/a['compression_ns']);same_bytes+=a['compressed_sha256']==c['compressed_sha256'];same_size+=a['compressed_bytes']==c['compressed_bytes']
  setting={'config_id':cid,'family':f,'setting':tt[0]['setting'],'median_cli_over_api_time_ratio':statistics.median(ratios),'byte_equal_pairs':same_bytes,'size_equal_pairs':same_size,'pairs':5}
  for mode,rr in repeats.items():
   assert len({r['compressed_bytes'] for r in rr})==1,'Unstable output size blocks replay'
   times=[r['compression_ns']/1e6 for r in rr];median=statistics.median(times);cv=statistics.stdev(times)/statistics.mean(times)
   setting[mode+'_median_ms']=median;setting[mode+'_cv']=cv
   table[mode].append({'config_id':cid,'family':f,'successful_trials':5,'complete_five_trials':True,'median_compression_ms':median,'compression_cv':cv,'distinct_output_digests':len({r['compressed_sha256'] for r in rr}),'compressed_bytes':rr[0]['compressed_bytes']})
  settings.append(setting)
 family=[]
 for f in ('zstd','lz4'):
  ss=[s for s in settings if s['family']==f]
  family.append({'family':f,'settings':48,'paired_observations':240,'median_setting_cli_over_api_ratio':statistics.median(s['median_cli_over_api_time_ratio'] for s in ss),
   'byte_equal_pairs':sum(s['byte_equal_pairs'] for s in ss),'size_equal_pairs':sum(s['size_equal_pairs'] for s in ss),'api_median_cv':statistics.median(s['api_cv'] for s in ss),'cli_median_cv':statistics.median(s['cli_cv'] for s in ss)})
 OUT.mkdir()
 for mode,rows in table.items():
  dest=OUT/mode;dest.mkdir()
  with (dest/'configuration_summary.csv').open('w',newline='') as stream:
   w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary={'families':family,'settings':settings,'cost':ledger,'qualification':'Paired interface comparison on exposed small workload. Different outputs confound a pure-startup interpretation.'}
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (OUT/'table_seal.json').write_text(json.dumps({'sha256':{str((OUT/m/'configuration_summary.csv').relative_to(ROOT)):hashlib.sha256((OUT/m/'configuration_summary.csv').read_bytes()).hexdigest() for m in table}},indent=2)+'\n')
 print(json.dumps({'families':family,'cost':ledger},indent=2))
if __name__=='__main__':main()
