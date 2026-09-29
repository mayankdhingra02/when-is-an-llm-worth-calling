"""Build already inspected official NGINX source, entirely project-local."""
import hashlib,json,platform,subprocess,time,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'artifacts/study_v105';SRC=ROOT/'.local-runtime/nginx-v105/nginx-1.28.3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    marker=ART/'build_manifest.json';assert not marker.exists()
    start=time.monotonic();commands=[['./configure',f'--prefix={ROOT}/.local-runtime/nginx-v105/runtime','--without-http_rewrite_module','--without-http_gzip_module'],['make','-j2']]
    attempts=[]
    for i,cmd in enumerate(commands):
        with (ART/f'build_{i}.log').open('x') as log:
            t=time.monotonic();p=subprocess.run(cmd,cwd=SRC,stdout=log,stderr=subprocess.STDOUT,timeout=max(1,600-(t-start)))
        attempts.append({'argv':cmd,'returncode':p.returncode,'seconds':time.monotonic()-t})
        if p.returncode:break
    binary=SRC/'objs/nginx';success=len(attempts)==2 and all(x['returncode']==0 for x in attempts)
    result={'success':success,'commands':attempts,'seconds':time.monotonic()-start,'platform':platform.platform(),'machine':platform.machine(),
            'source_sha256':sha(ROOT/'artifacts/sources/v105/nginx-1.28.3.tar.gz'),'binary_sha256':sha(binary) if success else None,
            'build_settings':subprocess.run([str(binary),'-V'],capture_output=True,text=True).stderr if success else None}
    shutil.copyfile(SRC/'LICENSE',ART/'NGINX_LICENSE.txt')
    marker.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    if not success:raise SystemExit(1)
