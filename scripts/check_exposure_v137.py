"""Recheck name-based exposure with explicit tested regexes; no target parsing."""
import json,re,subprocess,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={'gcc':r'\bgcc\b','imagemagick':r'\bimagemagick\b','lingeling':r'\blingeling\b','nodejs':r'\bnode[ ._-]?js\b','poppler':r'\bpoppler\b','xz':r'\bxz\b|\blzma\b','spear':r'\bspear\b','deeparch':r'\bdeeparch\b'}
def main():
 old=json.loads((ROOT/'artifacts/study_v137/exposure_scan.json').read_text());paths=list(old['scanned']);start=time.monotonic();candidates=set()
 for alias,example in [('gcc','GCC'),('imagemagick','ImageMagick'),('nodejs','Node.js'),('xz','liblzma not a word; xz')]:assert re.search(PATTERNS[alias],example,re.I)
 assert re.search(PATTERNS['gcc'],'libgcc_s') is None
 combined='|'.join(PATTERNS.values())
 for offset in range(0,len(paths),500):
  remaining=180-(time.monotonic()-start)
  if remaining<=0:raise TimeoutError('Exposure check limit')
  r=subprocess.run(['rg','-l','-i','-e',combined,'--']+paths[offset:offset+500],cwd=ROOT,text=True,capture_output=True,timeout=remaining)
  assert r.returncode in (0,1),r.stderr;candidates.update(r.stdout.splitlines())
 hits={k:[] for k in PATTERNS}
 for name in sorted(candidates):
  b=(ROOT/name).read_bytes();assert hashlib.sha256(b).hexdigest()==old['scanned'][name]['sha256'];text=b.decode()
  for k,pat in PATTERNS.items():
   match=re.search(pat,text,re.I)
   if match:hits[k].append({'path':name,'sha256':old['scanned'][name]['sha256'],'context':text[max(0,match.start()-90):match.end()+100]})
 result={'scope':old['scope'],'patterns':PATTERNS,'original_scanned_manifest_sha256':hashlib.sha256((ROOT/'artifacts/study_v137/exposure_scan.json').read_bytes()).hexdigest(),'scanned_files':len(paths),'hits':hits,'seconds':time.monotonic()-start,'objective_values_parsed':0,'note':'Authoritative explicit-regex recheck of the original frozen file list; only matching files rehashed, no newly created V138 outcomes included.'}
 (ROOT/'artifacts/study_v137/exposure_recheck.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'scanned_files':len(paths),'hits':{k:len(v) for k,v in hits.items()},'seconds':result['seconds']}))
if __name__=='__main__':main()
