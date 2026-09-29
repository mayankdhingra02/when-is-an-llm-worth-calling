"""Corrupt isolated compact copies; never mutate measured evidence."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 records=[]
 for kind in ['aggregate_gain','undercharged_budget','late_selection','wrong_anchor']:
  with tempfile.TemporaryDirectory(prefix='v138-corruption-') as tmp:
   dest=Path(tmp)/'replay';shutil.copytree(ROOT/'output/v138_replay',dest)
   if kind=='aggregate_gain':
    rel='results/v138_incumbent/comparison.json';d=json.loads((dest/rel).read_text());d['groups']['llvm']['adaptive_incumbent_neighbor_vs_historical_model']['mean']+=1
   elif kind=='undercharged_budget':
    rel='results/v138_incumbent/summary.json';d=json.loads((dest/rel).read_text());d['new_acquisitions']-=1
   else:
    p=sorted((dest/'results/v138_incumbent/selections').glob('*.json'))[0];rel=str(p.relative_to(dest));d=json.loads(p.read_text())
    if kind=='late_selection':d['at_unix']+=100000
    else:d['selected']['anchor_id']+=1
   p=dest/rel;p.write_text(json.dumps(d));manifest=json.loads((dest/'manifest.json').read_text());manifest['files'][rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(dest/'manifest.json').write_text(json.dumps(manifest))
   run=subprocess.run([str(ROOT/'.venv/bin/python'),'-I','-S',str(dest/'replay.py')],text=True,capture_output=True,timeout=30)
   assert run.returncode!=0 and 'AssertionError' in run.stderr;records.append({'mutation':kind,'rejected':True,'transport_hash_refreshed':True,'exit_code':run.returncode})
 (ROOT/'artifacts/study_v138/mutation_checks.json').write_text(json.dumps({'synthetic_only':True,'measured_files_unchanged':True,'checks':records},indent=2)+'\n');print('Rejected four semantic corruptions after refreshing transport hashes')
if __name__=='__main__':main()
