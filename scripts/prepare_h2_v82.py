"""Compile own JDBC harness using already pinned project-local ECJ/JRE."""
import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=json.loads((ROOT/'configs/runtime_v74.lock.json').read_text())
    for n,d in old['sha256'].items():assert sha(ROOT/n)==d,n
    java=ROOT/old['java'];compiler=ROOT/'artifacts/sources/v74/ecj.jar';jar=ROOT/'artifacts/sources/v81/h2-2.3.232.jar';classes=ROOT/'.local-runtime/h2-v82/classes';classes.mkdir(exist_ok=False)
    command=[str(java),'-Xmx512m','-jar',str(compiler),'-11','-proc:none','-g','-cp',str(jar),'-d',str(classes),str(ROOT/'src/native_v82/H2Probe.java')]
    start=time.monotonic();r=subprocess.run(command,capture_output=True,text=True,timeout=60,cwd=ROOT)
    (ROOT/'artifacts/study_v82/build.json').write_text(json.dumps({'command':command,'exit_code':r.returncode,'seconds':time.monotonic()-start,'stdout':r.stdout,'stderr':r.stderr},indent=2)+'\n');assert r.returncode==0,r.stderr
    pins={n:d for n,d in old['sha256'].items() if 'java-v53' in n or n.endswith('ecj.jar')}
    for p in [jar,ROOT/'src/native_v82/H2Probe.java',*classes.glob('*.class')]:pins[str(p.relative_to(ROOT))]=sha(p)
    (ROOT/'configs/runtime_v82.lock.json').write_text(json.dumps({'java':old['java'],'jar':str(jar.relative_to(ROOT)),'classes':str(classes.relative_to(ROOT)),'h2_version':'2.3.232','unmodified_dependency':True,'compiler':'ECJ3.32.0 targetJava11','sha256':pins},indent=2)+'\n')
    print('Compiled own harness; no benchmark run.')
if __name__=='__main__':main()
