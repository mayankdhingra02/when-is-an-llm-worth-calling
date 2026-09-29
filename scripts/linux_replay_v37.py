"""Standalone in-container validation harness; stdlib only, fixed archive evidence."""
import argparse,hashlib,json,os,platform,stat,subprocess,sys,time
from pathlib import Path,PurePosixPath
from zipfile import ZipFile

def require(ok,message):
    if not ok:raise ValueError(message)
def scientific(result):return {k:v for k,v in result.items() if k!='runtime'}
def archive_ok(path,expected):require(hashlib.sha256(path.read_bytes()).hexdigest()==expected,'Archive SHA256 mismatch')
def safe_extract(archive,destination):
    with ZipFile(archive) as z:
        names=set()
        for entry in z.infolist():
            p=PurePosixPath(entry.filename)
            require(not p.is_absolute() and '..' not in p.parts and entry.filename not in names,'Unsafe/duplicate archive path')
            require(not stat.S_ISLNK(entry.external_attr>>16),'Archive symlink rejected');names.add(entry.filename)
        require(sum(e.file_size for e in z.infolist())<60*1024**2,'Extraction size limit')
        z.extractall(destination)

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--sha256',required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    started=time.perf_counter();archive_ok(a.archive,a.sha256);safe_extract(a.archive,a.work)
    project=a.work/'llm-escalation-v34-reproduction'
    def replay():
        t=time.perf_counter();r=subprocess.run([sys.executable,'-I','-S','scripts/verify_reproduction_v35_1.py'],cwd=project,text=True,capture_output=True,timeout=30)
        return {'exit_code':r.returncode,'wall_seconds':time.perf_counter()-t,'stdout':r.stdout,'stderr':r.stderr}
    clean=replay();require(clean['exit_code']==0,'Initial Linux replay failed: '+clean['stderr']);decoded=json.loads(clean['stdout'])
    require(decoded['verified'] and decoded['isolated_flag']==decoded['site_disabled']==1,'Isolated successful verification')
    controls=[];summary=project/'results/v34_constrained/summary.json';original=summary.read_bytes();index=project/'REPRODUCTION_MANIFEST.json';old_index=index.read_bytes()
    for case in ('raw_byte_change','rebound_aggregate_score'):
        try:
            if case=='raw_byte_change':summary.write_bytes(original+b' ');expected='Changed bundle file'
            else:
                value=json.loads(original);value['summaries'][0]['equal_family_constrained_gain']=.5;summary.write_text(json.dumps(value,indent=2)+'\n')
                updated=json.loads(old_index);raw=summary.read_bytes();updated['files'][summary.relative_to(project).as_posix()]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
                index.write_text(json.dumps(updated,indent=2)+'\n');expected='Independent aggregate summary'
            check=replay();controls.append({'case':case,'expected_rejection':expected,**check})
            require(check['exit_code']!=0 and expected in check['stderr'],'Wrong corruption outcome: '+case)
        finally:summary.write_bytes(original);index.write_bytes(old_index)
    restored=replay();require(restored['exit_code']==0,'Restored Linux replay failed')
    require(scientific(json.loads(restored['stdout']))==scientific(decoded),'Restored scientific result differs')
    proc={}
    for line in Path('/proc/self/status').read_text().splitlines():
        if line.split(':')[0] in ('Uid','Gid','CapEff','NoNewPrivs'):k,value=line.split(':',1);proc[k]=value.strip()
    require(platform.system()=='Linux' and os.getuid()==65534 and int(proc['CapEff'],16)==0 and proc['NoNewPrivs']=='1','Expected Linux process constraints')
    print(json.dumps({'verified':True,'archive_sha256':a.sha256,'runtime':sys.version,'platform':platform.platform(),'os':platform.system(),
        'architecture':platform.machine(),'uid':os.getuid(),'process_constraints':proc,'clean':clean,'negative_controls':controls,'restored':restored,
        'scientific_result':decoded,'wall_seconds':time.perf_counter()-started,
        'scope':'Local Docker Linux VM, same physical host; saved-result reconstruction only'},indent=2))
if __name__=='__main__':main()
