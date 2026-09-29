"""Replay every native correctness/count/timing record independently of collection."""
import copy,hashlib,json,math,random,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def verify(rows,summary,version):
 expected_ops=128000 if version==150 else 2048000;groups={};assert len(rows)==20
 for i,row in enumerate(rows):
  assert row['index']==i and row['charged'] and row['block']==i//4
  cfgs=[(t,r) for t in [1,4] for r in [1,20]];random.Random(version*1000+i//4).shuffle(cfgs);assert (row['threads'],row['requests_per_event'])==cfgs[i%4]
  assert row['status']=='correct' and row['server_reaped'] and row['server_exit']==0 and row['client_exit']==0;assert 0<row['lifecycle_seconds']<=15
  m=json.loads(row['client_stdout']);assert m==row['measurement'];assert m['checked_operations']==expected_ops and m['failed_clients']==0 and m['clients']==4 and m['pipeline']==32;assert m['batches_per_client']==expected_ops//128;assert 0<m['seconds']<=10
  s=row['stats'];expected={'cmd_get':expected_ops//2,'get_hits':expected_ops//2,'get_misses':0,'cmd_set':expected_ops//2+1024,'curr_items':1024,'evictions':0}
  for k,v in expected.items():assert int(s[k])==v
  assert s['version']=='1.6.45';argv=row['server_command'];assert argv[argv.index('-l')+1]=='127.0.0.1' and argv[argv.index('-U')+1]=='0' and argv[argv.index('-m')+1]=='64'
  groups.setdefault((row['threads'],row['requests_per_event']),[]).append(m['seconds'])
 meds=[];passes=[]
 for g in summary['groups']:
  vals=groups[(g['threads'],g['requests_per_event'])];assert len(vals)==5 and vals==g['times_seconds'];med=statistics.median(vals);mad=statistics.median([abs(x-med) for x in vals]);assert med==g['median_seconds'];assert math.isclose(mad/med,g['relative_mad'],abs_tol=1e-12);meds.append(med);passes.append(mad/med<=.01);assert g['noise_pass']==passes[-1]
 contrast=(max(meds)-min(meds))/max(meds);assert math.isclose(contrast,summary['median_contrast'],abs_tol=1e-12);assert summary['feasible']==(all(passes) and contrast>=.05)
 c=summary['completion'];assert c['charged_probes']==c['correct']==c['intended_probes']==20 and c['wall_seconds']<=300

def main():
 records=[]
 for v in [150,152]:
  freeze=read(ROOT/f'artifacts/study_v{v}/preprobe.freeze.json')
  for n,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
  out=ROOT/f'results/v{v}_native';rows=[read(p) for p in sorted(out.glob('probe_*.json'))];s=read(out/'summary.json');verify(rows,s,v)
  assert read(out/'ledger.json')['charged_probes']==20
  assert all(r['at_unix']>freeze['at_unix'] for r in rows)
  mutations=[]
  for name in ['counter','elapsed','gate']:
   rr=copy.deepcopy(rows);ss=copy.deepcopy(s)
   if name=='counter':rr[0]['stats']['get_hits']='0'
   elif name=='elapsed':rr[0]['measurement']['seconds']=0
   else:ss['feasible']=not ss['feasible']
   try:verify(rr,ss,v)
   except AssertionError:mutations.append({'name':name,'rejected':True})
   else:raise AssertionError('Accepted corrupt '+name)
  records.append({'version':v,'verified':True,'native_probes':20,'all_correct':True,'gate_pass':s['feasible'],'mutations':mutations})
 dest=ROOT/'artifacts/study_v152/replay.json';dest.write_text(json.dumps({'verified':True,'stages':records},indent=2)+'\n');print('Verified40nativeprobes,allcorrect,caps/reaping/randomization,6mutationrejections')
if __name__=='__main__':main()
