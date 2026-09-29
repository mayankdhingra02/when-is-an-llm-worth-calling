"""Bounded create-once retrieval of explicit public owner artifacts; no execution."""
import argparse,hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('plan',type=Path);args=ap.parse_args();plan=json.loads(args.plan.read_text());base=ROOT/'artifacts/sources/v143';base.mkdir(parents=True,exist_ok=True);dest=base/(plan['stage']+'_receipt.json');assert not dest.exists();start=time.monotonic();records=[];error=None
 total=sum(json.loads(p.read_text())['saved_bytes'] for p in base.glob('*_receipt.json'))
 try:
  for req in plan['requests']:
   assert time.monotonic()-start<150;url=req['url'];assert url.startswith(('https://zenodo.org/','https://tfjmp.org/publications/','https://api.github.com/repos/mgarralda/spark-self-tuning-framework/','https://raw.githubusercontent.com/mgarralda/spark-self-tuning-framework/','https://re.public.polimi.it/','https://api.github.com/repos/ayat-khairy/tuneful-data/','https://raw.githubusercontent.com/ayat-khairy/tuneful-data/','https://api.github.com/repos/ayat-khairy/tuneful-code/','https://raw.githubusercontent.com/ayat-khairy/tuneful-code/','https://api.github.com/repos/xdbdilab/PTSSBench/','https://raw.githubusercontent.com/xdbdilab/PTSSBench/'))
   p=base/req['name'];assert not p.exists() and base in p.resolve().parents
   limit=min(req.get('max_bytes',2000000),20000000-total);assert limit>0
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bounded-research-audit/1.0'}),timeout=25) as r:b=r.read(limit+1)
   if len(b)>limit:raise RuntimeError('Download cap exceeded; oversized body not retained')
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);total+=len(b);rec={**req,'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};records.append(rec)
   if 'md5' in req:assert hashlib.md5(b).hexdigest()==req['md5']
   if 'git_sha' in req:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==req['git_sha']
 except Exception as e:error=repr(e)
 finally:dest.write_text(json.dumps({'plan':str(args.plan),'plan_sha256':hashlib.sha256(args.plan.read_bytes()).hexdigest(),'files':records,'saved_bytes':sum(r['bytes'] for r in records),'cumulative_stage_saved_bytes':total,'seconds':time.monotonic()-start,'error':error},indent=2)+'\n')
 if error:raise RuntimeError(error)
 print('Saved',len(records),'files;',total,'cumulative V143 bytes')
if __name__=='__main__':main()
