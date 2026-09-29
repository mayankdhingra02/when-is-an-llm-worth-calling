"""One correctness-checked application trial. No inference or network accesses."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.candidate_tasks_v66 import DUCK_N,read_pgm
from escalation.redis_v61 import timed_child
BASE=ROOT/'.local-runtime/candidates-v66'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(command, *, cwd, log_path, wall_cap, env=None):
    # Inherit the worker group so the outer watchdog kills all descendants.
    return {**timed_child(command,log_path,os.environ if env is None else env,cap=wall_cap),'termination_reason':None}
if __name__=='__main__':
    spec=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[1]).parent
    family=spec['family'];config=spec['configuration'];data=ROOT/'data/generated_v66'
    result={'family':family,'configuration':config,'status':'invalid','program_invocations':0};started=time.monotonic()
    try:
        if family=='duckdb':
            sys.path.insert(0,str(BASE/'duckdb'));import duckdb
            threads,memory,threshold=config
            c=duckdb.connect(config={'threads':str(threads),'memory_limit':memory,'enable_external_access':'false','autoload_known_extensions':'false','autoinstall_known_extensions':'false','preserve_insertion_order':'false','temp_directory':str(out/'duck_tmp')})
            result['program_invocations']=1
            c.execute('SET perfect_ht_threshold='+str(threshold))
            c.execute(f'CREATE TABLE fact AS SELECT i%4096 AS k,i%256 AS g,i%97 AS v FROM range({DUCK_N}) t(i)')
            c.execute('CREATE TABLE dim AS SELECT i AS k,i%17+1 AS w FROM range(4096) t(i)')
            result['version']=c.execute('PRAGMA version').fetchall()
            result['settings']=c.execute("SELECT name,value FROM duckdb_settings() WHERE name IN ('threads','memory_limit','perfect_ht_threshold','enable_external_access','autoload_known_extensions','autoinstall_known_extensions','preserve_insertion_order') ORDER BY name").fetchall()
            t=time.monotonic()
            rows=c.execute('SELECT g,SUM(v*w),COUNT(*) FROM fact JOIN dim USING(k) GROUP BY g ORDER BY g').fetchall()
            result['objective_ms']=1000*(time.monotonic()-t)
            rows=[list(row) for row in rows];(out/'answer.json').write_text(json.dumps(rows)+'\n')
            assert rows==json.loads((data/'query_expected.json').read_text()),'SQL answer mismatch'
            result['answer_sha256']=sha(out/'answer.json');c.close()
        elif family=='gnu_sort':
            threads,buffer,batch=config;binary=BASE/'coreutils-9.7/src/sort';tmp=out/'scratch';tmp.mkdir()
            cmd=[str(binary),'--parallel='+str(threads),'--buffer-size='+buffer,'--batch-size='+str(batch),'--temporary-directory='+str(tmp),'-o',str(out/'sorted.txt'),str(data/'sort_input.txt')]
            r=run(cmd,cwd=ROOT,log_path=out/'sort.log',wall_cap=20,env={**os.environ,'LC_ALL':'C'})
            result.update(command=cmd,execution=r,program_invocations=1)
            assert r['exit_code']==0 and r['termination_reason'] is None,'sort noncompletion'
            result['objective_ms']=1000*r['wall_seconds'];result['answer_sha256']=sha(out/'sorted.txt')
            assert result['answer_sha256']==json.loads((data/'manifest.json').read_text())['sort_expected_sha256'],'sorted output mismatch'
        elif family=='openjpeg':
            block,res,tile,threads=config;binpath=BASE/'openjpeg-210a8a5690d0da66f02d49420d7176a21ef409dc/build/bin'
            cmd=[str(binpath/'opj_compress'),'-i',str(data/'input.pgm'),'-o',str(out/'encoded.j2k'),'-r','1','-b',f'{block},{block}','-n',str(res),'-t',f'{tile},{tile}','-threads',str(threads)]
            r=run(cmd,cwd=ROOT,log_path=out/'encoder.log',wall_cap=20)
            result.update(command=cmd,execution=r,program_invocations=1)
            assert r['exit_code']==0 and r['termination_reason'] is None,'encoder noncompletion'
            result['objective_ms']=1000*r['wall_seconds'];result['compressed_bytes']=(out/'encoded.j2k').stat().st_size
            cmd2=[str(binpath/'opj_decompress'),'-i',str(out/'encoded.j2k'),'-o',str(out/'decoded.pgm'),'-threads','1']
            r2=run(cmd2,cwd=ROOT,log_path=out/'decoder.log',wall_cap=20)
            result.update(validation_command=cmd2,validation_execution=r2,program_invocations=2)
            assert r2['exit_code']==0 and r2['termination_reason'] is None,'decoder noncompletion'
            assert read_pgm((out/'decoded.pgm').read_bytes())==read_pgm((data/'input.pgm').read_bytes()),'pixel mismatch'
            result['decoded_pixels_sha256']=hashlib.sha256(read_pgm((out/'decoded.pgm').read_bytes())[2]).hexdigest()
        else:raise ValueError('Unknown family')
        result['status']='valid'
    except Exception as error:
        result.update(status='failed',error=f'{type(error).__name__}: {error}')
    result['worker_seconds']=time.monotonic()-started
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],flush=True)
