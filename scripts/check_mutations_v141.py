"""Isolated semantic corruption tests; never change measured evidence."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 rows=[]
 for kind in ['aggregate_gain','request_undercount','wrong_target','late_selection']:
  with tempfile.TemporaryDirectory(prefix='v141-synthetic-') as tmp:
   d=Path(tmp)/'replay';shutil.copytree(ROOT/'output/v141_replay',d)
   if kind=='aggregate_gain':
    rel='results/v141_analysis/comparison.json';v=json.loads((d/rel).read_text());v['totals']['smollm3_3b']['sequential_3nn']['mean_fraction']='1'
   elif kind=='request_undercount':
    rel='results/v141_models/qwen3_8b/ledger.json';v=json.loads((d/rel).read_text());v['generation_requests']-=1
   elif kind=='wrong_target':
    p=next((d/'results/v141_analysis/arms').glob('*.json'));rel=str(p.relative_to(d));v=json.loads(p.read_text());v['state']['labels'][-1][0]+=1
   else:
    rel='results/v141_analysis/selection_seal.json';v=json.loads((d/rel).read_text());v['at_unix']+=100000
   p=d/rel;p.write_text(json.dumps(v));m=json.loads((d/'manifest.json').read_text());m['files'][rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(d/'manifest.json').write_text(json.dumps(m))
   r=subprocess.run([str(ROOT/'.venv/bin/python'),'-I','-S',str(d/'replay.py')],capture_output=True,text=True,timeout=30)
   assert r.returncode and 'AssertionError' in r.stderr;rows.append({'mutation':kind,'rejected':True,'transport_hash_refreshed':True,'exit_code':r.returncode})
 (ROOT/'artifacts/study_v141/mutation_checks.json').write_text(json.dumps({'synthetic_only':True,'measured_files_unchanged':True,'checks':rows},indent=2)+'\n');print('Four semantic corruptions rejected')
if __name__=='__main__':main()
