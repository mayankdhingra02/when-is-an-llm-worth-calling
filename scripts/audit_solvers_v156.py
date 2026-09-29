"""Source/runtime provenance and repository exposure audit; no objective collection."""
import json,hashlib,re,zipfile,datetime,platform,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v156'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=ROOT/'artifacts/sources/v156';receipt=json.loads((source/'receipt_continuation.json').read_text());assert receipt['error'] is None
 for r in receipt['files']:assert sha(ROOT/r['path'])==r['sha256']
 licenses={}
 for p in source.glob('*.whl'):
  with zipfile.ZipFile(p) as z:
   names=[n for n in z.namelist() if not n.endswith('/') and any(x in n.lower() for x in ['license','copying'])]
   for n in names:
    target=A/'licenses'/p.stem/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(n))
   licenses[p.name]=names
 patterns=re.compile(r'\bcvc[-_ ]?5\b|\b(?:google[-_ ]?)?or[-_ ]tools\b|\bcp[-_ ]sat\b',re.I)
 paths=set()
 for folder in ['reports','configs','data']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.yaml','.md'] and not any(x in p.parts for x in ['raw','registry_raw','registry_raw_v5']))
 for folder in ['artifacts','results']:
  paths.update(p for p in (ROOT/folder).rglob('*.json') if any(x in p.name for x in ['jobs','manifest','registry','admission','candidates','models','completion']) and 'sources' not in p.parts)
 paths={p for p in paths if not re.search(r'v15[6-9]',str(p.relative_to(ROOT)))}
 checked=[];matches=[]
 for p in sorted(paths):
  text=p.read_text(errors='replace');checked.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})
  for match in patterns.finditer(text):matches.append({'path':str(p.relative_to(ROOT)),'match':match.group(),'context':text[max(0,match.start()-120):match.end()+180]})
 env=ROOT/'.venv-solvers156/lib/python3.10/site-packages';binary={str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in env.rglob('*') if p.is_file() and p.suffix in ['.so','.dylib']}
 result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'architecture':platform.machine(),'python':sys.version,'retained_http_bytes':receipt['retained_http_bytes'],'discarded_content_bytes':20000001,'wheel_licenses':licenses,'binaries':binary,'exposure_scope':checked,'identity_matches':matches,'limits':'Lexical and manifest audit, not a proof that all unstructured historic data are absent; solver families share constraint-solving domain and standard N-queens benchmark.'}
 (A/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'files_checked':len(checked),'matches':matches,'binaries':len(binary),'retained_bytes':receipt['retained_http_bytes']},indent=2))
if __name__=='__main__':main()
