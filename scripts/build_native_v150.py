"""Time-bounded owner source builds exclusively beneath this project."""
import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v150';B=ROOT/'.native-v150'
def main():
 assert not (A/'build.json').exists();start=time.monotonic();records=[];error=None;prefix=B/'prefix'
 cmds=[(B/'libevent-2.1.13-stable',['./configure','--prefix='+str(prefix),'--disable-shared','--enable-static','--disable-openssl','--disable-samples','--disable-libevent-regress']), (B/'libevent-2.1.13-stable',['make','-j2']), (B/'libevent-2.1.13-stable',['make','install']), (B/'memcached-1.6.45',['./configure','--prefix='+str(prefix),'--with-libevent='+str(prefix),'--disable-docs']), (B/'memcached-1.6.45',['make','-j2'])]
 try:
  for i,(cwd,cmd) in enumerate(cmds):
   remaining=600-(time.monotonic()-start)
   if remaining<=0:raise TimeoutError('Build cap')
   log=A/f'build_{i}.log';before=time.monotonic()
   with log.open('wb') as f:r=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=remaining)
   records.append({'cwd':str(cwd.relative_to(ROOT)),'command':cmd,'exit':r.returncode,'seconds':time.monotonic()-before,'log':str(log.relative_to(ROOT))})
   r.check_returncode()
 except Exception as e:error=repr(e)
 finally:
  binaries=[B/'memcached-1.6.45/memcached',prefix/'lib/libevent.a']
  (A/'build.json').write_text(json.dumps({'commands':records,'seconds':time.monotonic()-start,'cap_seconds':600,'error':error,'outputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in binaries if p.exists()}},indent=2)+'\n')
 if error:raise RuntimeError(error)
 print('Built Memcached and static libevent in project only')
if __name__=='__main__':main()
