"""Synthetic isolated corruption checks; measured files remain untouched."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 records=[]
 for kind in ['aggregate_gain','budget_undercount','wrong_decoded_bytes','late_selection']:
  with tempfile.TemporaryDirectory(prefix='v140-corruption-') as tmp:
   dest=Path(tmp)/'replay';shutil.copytree(ROOT/'output/v140_replay',dest)
   if kind=='aggregate_gain':
    rel='results/v140_native/comparison.json';d=json.loads((dest/rel).read_text());d['summary']['sequential_3nn']['mean_fraction']='1'
   elif kind=='budget_undercount':
    rel='results/v140_native/classical/ledger.json';d=json.loads((dest/rel).read_text());d['configuration_attempts']-=1
   elif kind=='wrong_decoded_bytes':
    rel='results/v140_native/classical/11_prefix_00/result.json';d=json.loads((dest/rel).read_text());d['records'][0]['validation']['decoded_sha256']='0'*64
   else:
    rel='results/v140_native/selections/11_prefix_00.json';d=json.loads((dest/rel).read_text());d['at_unix']+=100000
   p=dest/rel;p.write_text(json.dumps(d));manifest=json.loads((dest/'manifest.json').read_text());manifest['files'][rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(dest/'manifest.json').write_text(json.dumps(manifest))
   r=subprocess.run([str(ROOT/'.venv/bin/python'),'-I','-S',str(dest/'replay.py')],text=True,capture_output=True,timeout=30)
   assert r.returncode!=0 and 'AssertionError' in r.stderr;records.append({'mutation':kind,'rejected':True,'transport_hash_refreshed':True,'exit_code':r.returncode})
 (ROOT/'artifacts/study_v140/mutation_checks.json').write_text(json.dumps({'synthetic_only':True,'measured_files_unchanged':True,'checks':records},indent=2)+'\n');print('Four semantic mutations rejected')
if __name__=='__main__':main()
