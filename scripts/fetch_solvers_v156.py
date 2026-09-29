"""Retrieve pinned owner-linked registry wheels; no solving and no hidden output."""
import json,hashlib,time,urllib.request,zipfile,email
from pathlib import Path
from packaging.tags import sys_tags
from packaging.utils import parse_wheel_filename
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/sources/v156'
PINS={'cvc5':'1.4.1','ortools':'9.14.6206','absl-py':'2.3.1','numpy':'2.2.6','pandas':'2.3.3','protobuf':'6.31.1','typing-extensions':'4.15.0','immutabledict':'4.2.2','python-dateutil':'2.9.0.post0','pytz':'2025.2','tzdata':'2025.2','six':'1.17.0'}
def main():
 assert not (A/'receipt.json').exists();start=time.monotonic();rows=[];total=0;error=None;tags=list(sys_tags());rank={t:i for i,t in enumerate(tags)};lock=[]
 def fetch(n,url,cap):
  nonlocal total
  if time.monotonic()-start>600:raise TimeoutError('Source600scap')
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bounded-local-research/1.0'}),timeout=60) as response:data=response.read(min(cap,150000000-total)+1)
  if len(data)>cap or total+len(data)>150000000:raise ValueError('Downloadcap')
  p=A/n;p.write_bytes(data);total+=len(data);rows.append({'path':str(p.relative_to(ROOT)),'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});return data
 try:
  for name,version in PINS.items():
   meta=json.loads(fetch(name+'.json',f'https://pypi.org/pypi/{name}/{version}/json',1000000));options=[]
   for f in meta['urls']:
    if f['packagetype']!='bdist_wheel':continue
    _,_,_,ts=parse_wheel_filename(f['filename']);rr=[rank[t] for t in ts if t in rank]
    if rr:options.append((min(rr),f['filename'],f))
   if not options:raise ValueError('No compatible wheel '+name)
   f=min(options)[2];assert f['url'].startswith('https://files.pythonhosted.org/');body=fetch(f['filename'],f['url'],40000000 if name in ['numpy','pandas'] else 20000000);assert hashlib.sha256(body).hexdigest()==f['digests']['sha256']
   with zipfile.ZipFile(A/f['filename']) as z:
    md=[n for n in z.namelist() if n.endswith('.dist-info/METADATA')];assert len(md)==1;text=z.read(md[0]).decode();(A/(name+'.METADATA')).write_text(text);message=email.message_from_string(text)
   lock.append(name+'=='+version+' --hash=sha256:'+f['digests']['sha256']);rows[-1].update(registry_hash_verified=True,requires_dist=message.get_all('Requires-Dist',[]),license=message.get('License'),project_urls=message.get_all('Project-URL',[]));print(name,version,f['filename'],len(body),flush=True)
 except Exception as e:error=repr(e)
 finally:(A/'receipt.json').write_text(json.dumps({'files':rows,'retained_http_bytes':total,'cap_bytes':150000000,'seconds':time.monotonic()-start,'error':error},indent=2)+'\n');(ROOT/'configs/solvers_v156.lock.txt').write_text('\n'.join(lock)+'\n')
 if error:raise RuntimeError(error)
if __name__=='__main__':main()
