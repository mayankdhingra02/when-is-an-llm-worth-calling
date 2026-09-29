"""Owner-only source retrieval; create-once receipt; no objective execution."""
import hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/sources/v160'
def main():
 assert not (A/'receipt.json').exists();start=time.monotonic();rows=[];total=received=0;error=None
 def fetch(name,url,cap=40000000):
  nonlocal total,received
  if time.monotonic()-start>600:raise TimeoutError('600secondsourcecap')
  if not url.startswith(('https://www.python.org/','https://archive.ics.uci.edu/','https://codeload.github.com/nmslib/hnswlib/','https://api.github.com/repos/BurntSushi/ripgrep/','https://github.com/BurntSushi/ripgrep/releases/')):raise ValueError('Source not allowlisted')
  if total>=100000000:raise ValueError('Source byte cap')
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bounded-local-research/1.0'}),timeout=60) as r:
   if r.headers.get('Content-Length') and int(r.headers['Content-Length'])>min(cap,100000000-total):raise ValueError('Declared byte cap')
   body=r.read(min(cap,100000000-total)+1);received+=len(body)
  if len(body)>min(cap,100000000-total):raise ValueError('Observed byte cap')
  (A/name).write_bytes(body);total+=len(body);rows.append({'path':str((A/name).relative_to(ROOT)),'url':url,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()});print(name,len(body),flush=True);return body
 try:
  fetch('Python-3.10.13.tar.xz','https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz')
  fetch('optdigits.zip','https://archive.ics.uci.edu/static/public/80/optical%2Brecognition%2Bof%2Bhandwritten%2Bdigits.zip')
  fetch('hnswlib-v0.8.0.tar.gz','https://codeload.github.com/nmslib/hnswlib/tar.gz/refs/tags/v0.8.0')
  meta=json.loads(fetch('ripgrep_release.json','https://api.github.com/repos/BurntSushi/ripgrep/releases/tags/15.2.0',2000000))
  for suffix in ['.tar.gz','.tar.gz.sha256']:
   name='ripgrep-15.2.0-aarch64-apple-darwin'+suffix;asset=next(x for x in meta['assets'] if x['name']==name);fetch(name,asset['browser_download_url'],40000000 if suffix=='.tar.gz' else 10000)
  name='ripgrep-15.2.0-aarch64-apple-darwin.tar.gz';expected=(A/(name+'.sha256')).read_text().split()[0];assert hashlib.sha256((A/name).read_bytes()).hexdigest()==expected
 except Exception as e:error=repr(e)
 finally:(A/'receipt.json').write_text(json.dumps({'files':rows,'retained_http_bytes':total,'response_content_bytes_received':received,'seconds':time.monotonic()-start,'error':error,'stage_retained_byte_cap':100000000},indent=2)+'\n')
 if error:raise RuntimeError(error)
if __name__=='__main__':main()
