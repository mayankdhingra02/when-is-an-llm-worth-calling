"""Resolve installed clang/SDK mismatch only for this project build process."""
import json,os,subprocess,time
from pathlib import Path
from build_nginx_v105 import ROOT,ART,SRC,sha
if __name__=='__main__':
    marker=ART/'build_repair_manifest.json';assert not marker.exists()
    original=json.loads((ART/'build_manifest.json').read_text());assert not original['success']
    env=os.environ.copy();env['PATH']='/Library/Developer/CommandLineTools/usr/bin:'+env['PATH']
    env['SDKROOT']='/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk'
    commands=[['./configure',f'--prefix={ROOT}/.local-runtime/nginx-v105/runtime','--without-http_rewrite_module','--without-http_gzip_module','--with-cc=/Library/Developer/CommandLineTools/usr/bin/clang'],['make','-j2']]
    start=time.monotonic();attempts=[]
    for i,cmd in enumerate(commands):
        with (ART/f'build_repair_{i}.log').open('x') as log:
            t=time.monotonic();p=subprocess.run(cmd,cwd=SRC,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=max(1,600-original['seconds']-(t-start)))
        attempts.append({'argv':cmd,'returncode':p.returncode,'seconds':time.monotonic()-t})
        if p.returncode:break
    b=SRC/'objs/nginx';success=len(attempts)==2 and all(x['returncode']==0 for x in attempts)
    result={'success':success,'commands':attempts,'seconds':time.monotonic()-start,'process_local_toolchain':'/Library/Developer/CommandLineTools/usr/bin','process_local_SDKROOT':env['SDKROOT'],'system_settings_changed':False,
       'source_sha256':original['source_sha256'],'binary_sha256':sha(b) if success else None,'build_settings':subprocess.run([str(b),'-V'],capture_output=True,text=True).stderr if success else None}
    marker.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    if not success:raise SystemExit(1)
