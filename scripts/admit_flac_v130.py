"""Bounded owner-source retrieval. No encoding or configuration outcomes."""
import hashlib, json, time, tarfile, urllib.request
from pathlib import Path
from collect_smollm_v47 import ROOT, write, now, sha

A=ROOT/'artifacts/study_v130'
D=ROOT/'artifacts/sources/v130'
FILES=[
 ('https://ftp.osuosl.org/pub/xiph/releases/flac/SHA256SUMS.txt','SHA256SUMS.txt',None,None),
 ('https://ftp.osuosl.org/pub/xiph/releases/flac/flac-1.5.0.tar.xz','flac-1.5.0.tar.xz','sha256','f2c1c76592a82ffff8413ba3c4a1299b6c7ab06c734dee03fd88630485c2b920'),
 ('https://www.openslr.org/12/','openslr12.html',None,None),
 ('https://www.openslr.org/resources/12/md5sum.txt','md5sum.txt',None,None),
 ('https://www.openslr.org/resources/12/test-clean.tar.gz','test-clean.tar.gz','md5','32fa31d27d2e1cad72775fee3f4849a9'),
]
def main():
 assert not D.exists() or not any(D.iterdir()), 'Create once: directory must be absent or empty'
 assert not (A/'downloads.json').exists(), 'No implicit repeat'
 D.mkdir(parents=True,exist_ok=True);start=time.monotonic();receipt={'at':now(),'bytes_received':0,'files':[],'complete':False}
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 try:
  for url,name,algorithm,expected in FILES:
   item={'url':url,'path':str((D/name).relative_to(ROOT)),'bytes':0};receipt['files'].append(item)
   with opener.open(url,timeout=30) as response,(D/name).open('xb') as target:
    item['final_url']=response.url
    if not response.url.startswith(('https://ftp.osuosl.org/','https://www.openslr.org/','https://openslr.trmal.net/')):raise ValueError('Unapproved redirect')
    while True:
     if time.monotonic()-start>600:raise TimeoutError('Download stage limit')
     block=response.read(min(1048576,400000000-receipt['bytes_received']+1))
     if not block:break
     target.write(block);item['bytes']+=len(block);receipt['bytes_received']+=len(block)
     if receipt['bytes_received']>400000000:raise ValueError('Download byte cap')
   item['sha256']=sha(D/name)
   if algorithm:
    h=hashlib.new(algorithm)
    with (D/name).open('rb') as f:
     for b in iter(lambda:f.read(1048576),b''):h.update(b)
    assert h.hexdigest()==expected, 'Owner checksum mismatch'
    item['owner_checksum']={algorithm:expected}
   write(A/'downloads.json',receipt)
  # Safe regular-file extraction only; no traversal or links, bounded size.
  with tarfile.open(D/'flac-1.5.0.tar.xz') as tf:
   members=tf.getmembers();total=0
   for m in members:
    p=Path(m.name)
    assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='flac-1.5.0'
    assert m.isfile() or m.isdir(), 'Unexpected archive entry'
    total+=m.size
   assert total<50000000
   tf.extractall(D,filter='data')
  # Corpus inventory/selection examines member names only, never objective values.
  with tarfile.open(D/'test-clean.tar.gz') as tf:
   members=[m for m in tf.getmembers() if m.isfile()]
   clips=[m for m in members if m.name.endswith('.flac') and m.name.startswith('LibriSpeech/test-clean/')]
   speakers=sorted({int(m.name.split('/')[2]) for m in clips})[:3]
   selected=[min((m for m in clips if int(m.name.split('/')[2])==s),key=lambda m:m.name) for s in speakers]
   notices=[m for m in members if Path(m.name).name in ('LICENSE.TXT','README.TXT','SPEAKERS.TXT')]
   assert sum(m.size for m in selected+notices)<50000000
   for m in selected+notices:
    p=Path(m.name);assert not p.is_absolute() and '..' not in p.parts
    dest=D/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tf.extractfile(m).read())
   write(A/'corpus_selection.json',{'rule':'First three numerically sorted speakers, lexicographically first utterance each','group':'flac','clips':[{'path':str((D/m.name).relative_to(ROOT)),'sha256':sha(D/m.name),'bytes':m.size} for m in selected],'notices':[m.name for m in notices]})
  receipt['complete']=True
 except Exception as e:
  receipt['error']=repr(e);raise
 finally:
  receipt['seconds']=time.monotonic()-start;receipt['finished_at']=now();write(A/'downloads.json',receipt)
if __name__=='__main__':main()
