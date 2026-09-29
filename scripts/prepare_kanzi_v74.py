"""Offline, one-shot provenance checks and workload generation; no application run."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v74 import generated_workload

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):
    with p.open('x') as f:json.dump(data,f,indent=2);f.write('\n')

def main():
    art=ROOT/'artifacts/study_v74';sources=ROOT/'artifacts/sources/v74'
    for e in json.loads((sources/'manifest.json').read_text())['entries']:
        p=sources/e['file'];assert sha(p)==e['sha256'] and p.stat().st_size==e['bytes']
    tree=json.loads((sources/'tree.json').read_text());assert not tree['truncated']
    assert tree['sha']=='9828b05815b754f1ae40acd83552605885ba515b'
    source=ROOT/'.local-runtime/kanzi-v74/source';verified={}
    for e in tree['tree']:
        if e['type']!='blob':continue
        p=source/e['path'];b=p.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha'],e['path']
        verified[str(p.relative_to(ROOT))]=sha(p)
    write(art/'source_verification.json',{'owner_commit':tree['sha'],'git_blobs_verified':len(verified),'sha256':verified})
    # Inspect identifier-bearing project manifests; no measured objective table is opened.
    manifests=sorted(p for p in (ROOT/'data').glob('*.json'))
    matches=[str(p.relative_to(ROOT)) for p in manifests if 'kanzi' in p.read_text().lower()]
    write(art/'family_exposure.json',{'searched_sha256':{str(p.relative_to(ROOT)):sha(p) for p in manifests},
        'kanzi_text_matches':matches,'scope':'top-level data manifests only; aliases/pretraining not exhaustively resolved',
        'assignment':'development','held_out_claim':False,'prior_feature_inspection':'V73 configuration metadata only'})
    target=ROOT/'data/generated_v74';target.mkdir(exist_ok=False)
    (target/'workload.bin').write_bytes(generated_workload())
    write(target/'manifest.json',{'kind':'generated feasibility input, not production workload or synthetic result',
        'bytes':(target/'workload.bin').stat().st_size,'sha256':sha(target/'workload.bin'),
        'generator':'src/escalation/kanzi_v74.py','generator_sha256':sha(ROOT/'src/escalation/kanzi_v74.py'),
        'family':'kanzi','split':'development'})
    java=ROOT/'.local-runtime/java-v53/jdk-17.0.20.1+1-jre/Contents/Home'
    jar=ROOT/'.local-runtime/kanzi-v74/kanzi-1.9.0.jar'
    assert sha(jar)=='b1585d7dd7fe118bcdf27844ce6bad37c808d28177a35eb7de98379f50aa397c'
    pins={str(p.relative_to(ROOT)):sha(p) for p in [jar,java/'bin/java',java/'release',java/'lib/modules',java/'lib/server/libjvm.dylib',sources/'ecj.jar']}
    write(ROOT/'configs/runtime_v74.lock.json',{'java':str((java/'bin/java').relative_to(ROOT)),'jar':str(jar.relative_to(ROOT)),
        'sha256':pins,'source_commit':tree['sha'],'compiler':'Eclipse ECJ 3.32.0, Java 11 target',
        'java_identity':'Eclipse Temurin 17.0.20.1+1, aarch64 Darwin, existing local JRE',
        'adaptation':'owner source built locally; not an upstream binary or archived measurement replication'})
    print(json.dumps({'source_blobs':len(verified),'manifest_files':len(manifests),'matches':matches,'workload_bytes':16777216}))

if __name__=='__main__':main()
