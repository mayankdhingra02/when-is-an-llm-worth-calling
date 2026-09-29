"""Bounded owner-source capture only. Never imports or executes fetched code."""
import urllib.request,time
from collect_smollm_v47 import ROOT,read,write,sha,now
REV='196fe237f60a3d3a2fa53cbf8f474ec20a01dd57'
def main():
 cfg=read(ROOT/'configs/study_v124.json');out=ROOT/'artifacts/sources/v124';out.mkdir(parents=True,exist_ok=False);used=0;start=time.monotonic();files=[]
 for name in ['llambo/discriminative_sm.py','llambo/discriminative_sm_utils.py','LICENSE']:
  assert len(files)<cfg['source_request_cap'] and time.monotonic()-start<cfg['source_time_cap_seconds'];url=f'https://raw.githubusercontent.com/tennisonliu/LLAMBO/{REV}/{name}';remaining=cfg['source_download_cap_bytes']-used
  req=urllib.request.Request(url,headers={'User-Agent':'bounded-research-source-audit','Accept-Encoding':'identity'})
  with urllib.request.urlopen(req,timeout=25) as r:
   assert r.geturl()==url;body=r.read(remaining);assert len(body)<remaining,'Source cap reached'
  used+=len(body);p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body);files.append({'path':str(p.relative_to(ROOT)),'url':url,'bytes':len(body),'sha256':sha(p)})
  write(out/'manifest.json',{'at':now(),'owner':'tennisonliu/LLAMBO','revision':REV,'files':files,'actual_source_bytes':used,'executed_upstream_code':False})
 print('Saved',len(files),'owner files;',used,'bytes')
if __name__=='__main__':main()
