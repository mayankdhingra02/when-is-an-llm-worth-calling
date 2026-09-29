"""One bounded offline Docker reconstruction; no pulls, installs or cloud services."""
import hashlib,json,subprocess,sys,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/study_v37'
IMAGE='sha256:dbf1de478a55d6763afaa39c2f3d7b54b25230614980276de5cacdde79529d0c'
ARCHIVE=ROOT/'output/llm_escalation_v34_reproduction_v35_1.zip'
EXPECTED='75333386b2ab80ac5a49ec554050fc1f4ba92e708a2c1908c1cdfcccecb663f9'
def read(p):return json.loads(Path(p).read_text())
def save(n,v):(OUT/n).write_text(json.dumps(v,indent=2)+'\n')
def scientific(r):return {k:v for k,v in r.items() if k!='runtime'}
def main():
    if (OUT/'execution.json').exists():raise FileExistsError('Preserve attempted container execution')
    for n,h in read(ROOT/'reports/protocol_v37_linux.freeze.json')['sha256'].items():
        if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input mismatch: '+n)
    if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()!=EXPECTED:raise ValueError('Archive changed')
    inspect=subprocess.run(['docker','image','inspect',IMAGE,'--format','{{.Id}} {{.Os}} {{.Architecture}}'],text=True,capture_output=True,timeout=10)
    save('image_confirmation.json',{'exit_code':inspect.returncode,'stdout':inspect.stdout,'stderr':inspect.stderr})
    if inspect.returncode or inspect.stdout.strip()!=IMAGE+' linux arm64':raise RuntimeError('Pinned local image unavailable')
    name='llm-escalation-v37-'+uuid.uuid4().hex[:10]
    command=['docker','run','--rm','--pull=never','--name',name,'--network=none','--read-only','--user=65534:65534','--cap-drop=ALL',
        '--security-opt=no-new-privileges','--memory=256m','--cpus=1','--pids-limit=64','--tmpfs','/work:rw,noexec,nosuid,size=64m,mode=1777',
        '--mount',f'type=bind,src={ARCHIVE},dst=/input/reproduction.zip,readonly',
        '--mount',f'type=bind,src={ROOT}/scripts/linux_replay_v37.py,dst=/input/replay.py,readonly',
        '--entrypoint','/usr/local/bin/python3',IMAGE,'-I','-S','/input/replay.py','--archive','/input/reproduction.zip','--sha256',EXPECTED,'--work','/work']
    start=time.perf_counter();result=None
    try:
        proc=subprocess.run(command,text=True,capture_output=True,timeout=90)
        result={'command':command,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'wall_seconds':time.perf_counter()-start}
    except subprocess.TimeoutExpired as e:
        result={'command':command,'timed_out':True,'wall_seconds':time.perf_counter()-start,'stdout':str(e.stdout),'stderr':str(e.stderr)}
    finally:
        if result is not None:save('execution.json',result)
        # Only this invocation's UUID-named container can be cleaned up.
        remaining=subprocess.run(['docker','container','ls','-a','--filter','name=^/'+name+'$','--format','{{.ID}}'],text=True,capture_output=True,timeout=10)
        if remaining.returncode:raise RuntimeError('Cannot verify container cleanup')
        if remaining.stdout.strip():
            cleanup=subprocess.run(['docker','container','rm','-f',name],text=True,capture_output=True,timeout=10)
            save('cleanup.json',{'name':name,'exit_code':cleanup.returncode,'stdout':cleanup.stdout,'stderr':cleanup.stderr})
            if cleanup.returncode:raise RuntimeError('Task container cleanup failed')
        else:save('cleanup.json',{'name':name,'automatic_removal_verified':True})
    if result.get('exit_code')!=0:raise RuntimeError('Linux run failed; see execution.json')
    linux=json.loads(result['stdout']);save('linux_receipt.json',linux)
    for version in ('python310','python312'):
        prior=json.loads(read(ROOT/f'artifacts/reproduction_v35_1/{version}.json')['stdout'])
        if scientific(prior)!=scientific(linux['scientific_result']):raise ValueError('Scientific output mismatch: '+version)
    save('validation.json',{'verified':True,'image_id':IMAGE,'archive_sha256':EXPECTED,'os':linux['os'],'architecture':linux['architecture'],
        'runtime':linux['runtime'],'matches_macos_python310_and312':True,'negative_controls_rejected':len(linux['negative_controls']),
        'restored_passed':linux['restored']['exit_code']==0,'wall_seconds':result['wall_seconds'],'new_model_calls':0,'new_objective_acquisitions':0,
        'new_downloads':0,'scope':'Different OS/Python version via local Linux VM on same physical host; not independent machine'})
    print(json.dumps(read(OUT/'validation.json'),indent=2))
if __name__=='__main__':main()
