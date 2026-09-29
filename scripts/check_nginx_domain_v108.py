"""Check static syntax for every frozen candidate; no HTTP/objective work."""
import argparse,json,subprocess,time,hashlib
from pathlib import Path
from nginx_domain_v108 import ROOT,domain,config,PAYLOAD
from native_nginx_v105 import BINARY
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--attempt',choices=['syntax','syntax_permitted'],default='syntax');args=ap.parse_args()
 out=ROOT/'artifacts/study_v108'/args.attempt;out.mkdir(exist_ok=False);(out/'www').mkdir();(out/'logs').mkdir();(out/'www/payload.bin').write_bytes(PAYLOAD)
 rows=[];start=time.monotonic()
 for i,r in enumerate(domain()):
  p=out/'nginx.conf';p.write_text(config(r,out))
  run=subprocess.run([str(BINARY),'-p',str(out)+'/', '-c',str(p),'-t'],capture_output=True,text=True,timeout=5)
  rows.append({'id':i,'valid':run.returncode==0,'returncode':run.returncode,'config_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stdout':run.stdout,'stderr':run.stderr})
  if time.monotonic()-start>300:raise TimeoutError('Syntax stage ceiling')
 (out/'results.json').write_text(json.dumps({'rows':rows,'seconds':time.monotonic()-start,'objective_acquisitions':0,'http_requests':0,'syntax_checks':len(rows)},indent=2)+'\n')
 assert len(rows)==768 and all(r['valid'] for r in rows)
 print('768/768 syntax checks passed; no HTTP requests or objective acquisitions.')
