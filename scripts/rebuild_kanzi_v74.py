"""Offline rebuild into a NEW directory; no benchmark execution. Requires saved sources."""
import argparse,hashlib,json,os,subprocess,time,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',required=True);args=parser.parse_args()
    out=Path(args.output_dir).resolve();assert out.is_relative_to(ROOT)
    for name,digest in json.loads((ROOT/'artifacts/study_v74/source_verification.json').read_text())['sha256'].items():
        assert sha(ROOT/name)==digest,name
    lock=json.loads((ROOT/'configs/runtime_v74.lock.json').read_text())
    for name,digest in lock['sha256'].items():assert sha(ROOT/name)==digest,name
    out.mkdir(exist_ok=False);classes=out/'classes';classes.mkdir()
    sources=sorted((ROOT/'.local-runtime/kanzi-v74/source/java/src/main/java').rglob('*.java'))
    argfile=out/'sources.args';argfile.write_text('\n'.join(str(p) for p in sources)+'\n')
    command=[str(ROOT/lock['java']),'-Xmx1024m','-jar',str(ROOT/'artifacts/sources/v74/ecj.jar'),'-11','-proc:none','-g','-d',str(classes),'@'+str(argfile)]
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    start=time.monotonic()
    with (out/'build.log').open('xb') as log:r=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,env=env,timeout=180)
    receipt={'command':command,'exit_code':r.returncode,'seconds':time.monotonic()-start}
    (out/'build.json').write_text(json.dumps(receipt,indent=2)+'\n');assert r.returncode==0
    jar=out/'kanzi-1.9.0.jar'
    entries=[('META-INF/MANIFEST.MF',b'Manifest-Version: 1.0\r\nMain-Class: kanzi.app.Kanzi\r\nImplementation-Version: 1.9.0\r\n\r\n'),
             ('META-INF/LICENSE',(ROOT/'.local-runtime/kanzi-v74/source/LICENSE').read_bytes())]
    entries += [(str(p.relative_to(classes)),p.read_bytes()) for p in sorted(classes.rglob('*.class'))]
    with zipfile.ZipFile(jar,'x') as z:
        for name,body in entries:
            info=zipfile.ZipInfo(name,date_time=(2021,5,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,body)
    expected=lock['sha256'][lock['jar']];actual=sha(jar)
    (out/'comparison.json').write_text(json.dumps({'expected_sha256':expected,'actual_sha256':actual,'bitwise_match':actual==expected},indent=2)+'\n')
    assert actual==expected,'Rebuild differs: retain both artifacts and investigate'
    print(json.dumps({'bitwise_match':True,'seconds':receipt['seconds']}))

if __name__=='__main__':main()
