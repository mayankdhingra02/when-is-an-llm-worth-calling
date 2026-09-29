from pathlib import Path
import hashlib,json,platform,subprocess
root=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for p in sorted((root/'artifacts/sources').glob('*')):
 records.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)})
(root/'artifacts/source_manifest.json').write_text(json.dumps({'sources':records,'reading_report_sha256':sha(root/'reading/deep-research.md'),'read_once':True},indent=2))
env={'python':platform.python_version(),'platform':platform.platform(),'machine':platform.machine(),'chip':'Apple M3 Pro','cpu_cores':11,'gpu_cores':14,'ram_gib':18,'initial_disk_available_gib_approx':32,'note':'hardware identifiers deliberately not retained'}
(root/'artifacts/environment.json').write_text(json.dumps(env,indent=2))
# pip progress uses rounded sizes, so do not represent these as exact network bytes.
import re
pip_approx=0
for log in ['install.log','scipy_compat_install.log']:
 text=(root/'artifacts'/log).read_text()
 for n,unit in re.findall(r'Downloading .*?\(([\d.]+) (MB|kB)\)',text):pip_approx+=float(n)*(1e6 if unit=='MB' else 1e3)
model=json.loads((root/'artifacts/model_manifest.json').read_text())
raw_bytes=sum(p.stat().st_size for p in (root/'data/raw').glob('*'))
source_bytes=sum(x['bytes'] for x in records)
# Download overhead is not precisely observable from retained logs; a conservative reserve covers metadata/HTTP.
reserve=100*1024**2
total=model['download_bytes']+raw_bytes+source_bytes+pip_approx+reserve
assert total<5*1024**3
(root/'artifacts/download_accounting.json').write_text(json.dumps({'model_exact_bytes':model['download_bytes'],'raw_tables_exact_bytes':raw_bytes,'source_files_exact_bytes':source_bytes,'pip_payload_approx_bytes':pip_approx,'conservative_metadata_overhead_reserve_bytes':reserve,'accounted_upper_estimate_bytes':total,'max_total_bytes':5*1024**3,'note':'Pip progress amounts are rounded; no exact network-transfer or electricity-cost claim. No further downloads needed.'},indent=2))
print('Source/environment/download manifests written')
