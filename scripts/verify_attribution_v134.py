"""Independent saved-input reconstruction of the retrospective attribution audit."""
import argparse,hashlib,json
from pathlib import Path
from decimal import Decimal
from fractions import Fraction

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--comparison',type=Path);args=ap.parse_args();root=args.root
 def read(n):return json.loads((root/n).read_text())
 mapping=read('results/v134_attribution/inputs.json')
 for n,h in mapping['sha256'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==h,n
 data=json.loads(args.comparison.read_text()) if args.comparison else read('results/v134_attribution/comparison.json');rows=data['rows'];assert len(rows)==60 and len({(r['group'],r['seed']) for r in rows})==60 and len(data['groups'])==12
 def gain(a,b,d):
  a,b=Fraction(Decimal(str(a))),Fraction(Decimal(str(b)));return ((b-a) if d=='maximize' else (a-b))/a
 for r in rows:
  v=r['stage'];source=read(r['source']);seed=r['seed'];group=r['group'];direction='minimize';fallback=False
  if v in [127,129]:
   case=next(c for c in source['cases'] if c['system_group']==group and c['seed']==seed);jobs=read(f'artifacts/study_v{127 if v==127 else 128}/jobs.json');job=next(j for j in jobs if j['base_key']==case['key'] and j['condition']=='normal');body=json.loads(read(job['messages_path'])[1]['content']);direction=body['direction'];p=read(job['prefix']);y=[x[0] for x in p['state']['labels']];prefix=(min if direction=='minimize' else max)(y);llm=case['target'];seq=case['references']['full_sequential_3nn'];fallback=case['fallback']
  else:
   case=next(c for c in source['rows'] if c['seed']==seed and (v!=131 or c['task']==group))
   if v==130:prefix,llm,seq=case['prefix_best_bytes'],case['llm_bytes'],case['sequential_3nn_bytes']
   else:prefix,llm,seq=case['prefix_best'],case['llm'],case['sequential_3nn']
   fallback=case['fallback']
  assert (r['prefix'],r['llm_policy'],r['sequential'],r['direction'],r['fallback'])==(prefix,llm,seq,direction,fallback)
  assert r['valid_model']==(not fallback) and r['gain_from_prefix_fraction']==str(gain(prefix,llm,direction)) and r['selection_paired_gain_fraction']==str(gain(seq,llm,direction))
  primary=gain(case['fresh_medians_ns']['sequential_3nn'],case['fresh_medians_ns']['llm'],'minimize') if group=='fftw' else gain(seq,llm,direction);assert r['primary_paired_gain_fraction']==str(primary)
  assert r['timing_caution']==(group=='fftw') and r['role']==('historical_exposed_development_or_failure' if v in [127,129,130] else 'prospective_frozen_router_test')
 for group,s in data['groups'].items():
  rs=[r for r in rows if r['group']==group];assert len(rs)==s['intended']==5 and s['fallbacks']==sum(r['fallback'] for r in rs)
  assert s['improved_prefix']==sum(Fraction(r['gain_from_prefix_fraction'])>0 for r in rs);assert s['beats_sequential']==sum(Fraction(r['primary_paired_gain_fraction'])>0 for r in rs);assert s['beats_sequential_over_1pct']==sum(Fraction(r['primary_paired_gain_fraction'])>Fraction(1,100) for r in rs);assert s['mean_paired_gain_fraction']==str(sum(Fraction(r['primary_paired_gain_fraction']) for r in rs)/5)
 for kind,c in data['counts'].items():
  rs=rows if kind=='all_intended' else [r for r in rows if r['valid_model']];assert c=={'cases':len(rs),'improved_prefix':sum(Fraction(r['gain_from_prefix_fraction'])>0 for r in rs),'beats_sequential':sum(Fraction(r['primary_paired_gain_fraction'])>0 for r in rs),'beats_sequential_over_1pct':sum(Fraction(r['primary_paired_gain_fraction'])>Fraction(1,100) for r in rs)}
 assert data['new_model_requests']==data['new_objective_acquisitions']==0 and set(data['prospective_router_test_groups'])=={'wavpack','fftw','libjpeg'}
 assert sum(r['fallback'] for r in rows)==5 and {r['group'] for r in rows if r['fallback']}=={'sac'}
 print(json.dumps({'verified':True,'intended_cases':60,'groups':12,'fallbacks_preserved':5,'valid_cases':55,'new_collection':0,'scope':'Retrospective arithmetic/source/denominator audit, not new empirical replication'}))
if __name__=='__main__':main()
