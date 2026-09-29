"""Build isolated Apache-2.0 owner-source buffer repair; original files untouched."""
import difflib,hashlib,json,os,shutil,subprocess,time,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    art=ROOT/'artifacts/study_v76';art.mkdir(exist_ok=False)
    src=ROOT/'.local-runtime/kanzi-v74/source'
    for n,d in json.loads((ROOT/'artifacts/study_v74/source_verification.json').read_text())['sha256'].items():assert sha(ROOT/n)==d
    lock=json.loads((ROOT/'configs/runtime_v74.lock.json').read_text())
    for n,d in lock['sha256'].items():assert sha(ROOT/n)==d
    target=ROOT/'.local-runtime/kanzi-v76';target.mkdir(exist_ok=False);shutil.copytree(src,target/'source')
    name='java/src/main/java/kanzi/io/CompressedOutputStream.java';p=target/'source'/name;before=p.read_text()
    old='this.obs.writeBits(this.data.array, n, chkSize);';assert before.count(old)==1
    after=before.replace(old,'this.obs.writeBits(baos.getBuffer(), n, chkSize);')
    needle='      public CustomByteArrayOutputStream(byte[] buffer, int size)';assert after.count(needle)==1
    after=after.replace(needle,'      public byte[] getBuffer() { return this.buf; }\n\n'+needle);p.write_text(after)
    (art/'buffer_fix.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='owner/'+name,tofile='adaptation/'+name)))
    files=sorted((target/'source/java/src/main/java').rglob('*.java'));classes=target/'classes';classes.mkdir()
    args=art/'sources.args';args.write_text('\n'.join(str(f) for f in files)+'\n')
    command=[str(ROOT/lock['java']),'-Xmx1024m','-jar',str(ROOT/'artifacts/sources/v74/ecj.jar'),'-11','-proc:none','-g','-d',str(classes),'@'+str(args)]
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    start=time.monotonic()
    with (art/'build.log').open('xb') as f:r=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=180)
    (art/'build.json').write_text(json.dumps({'command':command,'exit_code':r.returncode,'seconds':time.monotonic()-start},indent=2)+'\n');assert r.returncode==0
    jar=target/'kanzi-1.9-v76-buffer-fix.jar'
    entries=[('META-INF/MANIFEST.MF',b'Manifest-Version: 1.0\r\nMain-Class: kanzi.app.Kanzi\r\nImplementation-Version: 1.9-v76-buffer-fix\r\n\r\n'),('META-INF/LICENSE',(src/'LICENSE').read_bytes())]
    entries += [(str(f.relative_to(classes)),f.read_bytes()) for f in sorted(classes.rglob('*.class'))]
    with zipfile.ZipFile(jar,'x') as z:
        for name,body in entries:
            info=zipfile.ZipInfo(name,date_time=(2021,5,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,body)
    pins={str(f.relative_to(ROOT)):sha(f) for f in files};pins[str(jar.relative_to(ROOT))]=sha(jar)
    (ROOT/'configs/runtime_v76.lock.json').write_text(json.dumps({'java':lock['java'],'jar':str(jar.relative_to(ROOT)),'original_jar':lock['jar'],'sha256':pins,'adaptation':'Only current ByteArrayOutputStream backing buffer is emitted, retaining original owner runtime separately','original_commit':lock['source_commit']},indent=2)+'\n')
    print(json.dumps({'patched_jar':str(jar.relative_to(ROOT)),'sha256':sha(jar)}))
if __name__=='__main__':main()
