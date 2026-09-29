"""Explicit owner source retrieval, five-megabyte finite allowance."""
import hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/sources/v150'
REQUESTS=[('memcached-downloads.html','https://www.memcached.org/downloads'),('libevent.html','https://libevent.org/'),('memcached-1.6.45.tar.gz','https://www.memcached.org/files/memcached-1.6.45.tar.gz'),('libevent-2.1.13-stable.tar.gz','https://github.com/libevent/libevent/releases/download/release-2.1.13-stable/libevent-2.1.13-stable.tar.gz')]
def main():
 assert not (A/'receipt.json').exists();start=time.monotonic();records=[];total=0;error=None
 try:
  for name,url in REQUESTS:
   if time.monotonic()-start>150:raise TimeoutError('Source audit clock')
   p=A/name;assert not p.exists();limit=min(3000000,5000000-total)
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bounded-research-source-audit/1.0'}),timeout=30) as r:b=r.read(limit+1)
   if len(b)>limit:raise ValueError('Oversized download not retained')
   p.write_bytes(b);total+=len(b);records.append({'path':str(p.relative_to(ROOT)),'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'sha1':hashlib.sha1(b).hexdigest()})
   if name=='memcached-1.6.45.tar.gz':assert records[-1]['sha1']=='45038980ea7045a548b9b5b5125ef7116312a768'
 except Exception as e:error=repr(e)
 finally:(A/'receipt.json').write_text(json.dumps({'files':records,'retained_bytes':total,'cap_bytes':5000000,'seconds':time.monotonic()-start,'error':error},indent=2)+'\n')
 if error:raise RuntimeError(error)
 print(json.dumps({'files':len(records),'retained_bytes':total}))
if __name__=='__main__':main()
