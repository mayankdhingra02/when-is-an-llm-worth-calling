"""Bounded native prefixes and paired continuations, isolated from inference."""
import argparse, json, os, random, signal, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read, write, append, sha, now
from escalation.core import initial_state, State
from escalation.finite_domain import recommend
from escalation.numerical_v97 import candidates
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import messages, rank
from run_planning_v55 import rss
OUT=ROOT/'results/v97_native'; ART=ROOT/'artifacts/study_v97'

def verify_freeze():
    for n,h in read(ROOT/'reports/protocol_v97.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)

class Acquisition:
    def __init__(self):
        self.started=time.monotonic()
        self.ledger=read(OUT/'ledger.json') if (OUT/'ledger.json').exists() else dict(acquisitions=0,worker_wall_seconds=0.,physical_solves_returned=0,failures=0)
    def acquire(self,family,seed,arm,state,row):
        if row in state.ids or len(state.ids)>=20:raise ValueError('Budget/duplicate violation')
        if self.ledger['acquisitions']>=250:raise RuntimeError('Collection cap')
        if self.ledger['worker_wall_seconds']+time.monotonic()-self.started>600-35:raise TimeoutError('Native stage wall reserve')
        key=f'{family}_{seed}_{arm}_{len(state.ids):02d}'
        path=OUT/'evaluations'/f'{key}.json';request=OUT/'requests'/f'{key}.json'
        if path.exists() or request.exists():raise ValueError('No repeat acquisition')
        write(request,{'key':key,'family':family,'seed':seed,'arm':arm,'row':row,
                       'configuration':candidates(family).x[row],'at':now()})
        self.ledger['acquisitions']+=1;write(OUT/'ledger.json',self.ledger)
        start=time.monotonic()
        env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','MKL_NUM_THREADS':'1'}
        try:
            peak=0;reason=None
            with (OUT/'stderr'/f'{key}.txt').open('x') as err, (OUT/'stdout'/f'{key}.txt').open('x') as log:
                run=subprocess.Popen([sys.executable,str(ROOT/'scripts/worker_numerical_v97.py'),str(request),str(path)],
                    cwd=ROOT,env=env,stdout=log,stderr=err,start_new_session=True)
                try:
                    while run.poll() is None:
                        peak=max(peak,rss(run.pid))
                        if peak>2*1024**3:reason='native_rss_guard'
                        if time.monotonic()-start>30:reason='native_wall_guard'
                        if reason:os.killpg(run.pid,signal.SIGKILL);break
                        time.sleep(.05)
                    run.wait(timeout=3)
                finally:
                    if run.poll() is None:os.killpg(run.pid,signal.SIGKILL);run.wait(timeout=3)
            append(OUT/'worker_exits.jsonl',{'key':key,'exit_code':run.returncode,'reason':reason,'peak_sampled_rss_bytes':peak})
            if reason or run.returncode or not path.exists():raise RuntimeError(f'worker exit {run.returncode}, {reason}')
            record=read(path)
            self.ledger['physical_solves_returned']+=len(record['measurements'])
            if record['peak_worker_rss_bytes']>2*1024**3:raise MemoryError('Native worker RSS over 2 GiB')
            y=record['objective_seconds']
            if not record['valid']:self.ledger['failures']+=1
        except Exception as e:
            self.ledger['failures']+=1;y=30.
            append(OUT/'failures.jsonl',{'key':key,'reason':repr(e),'penalty_seconds':30.,'physical_solves_unknown':True})
        elapsed=time.monotonic()-start
        append(OUT/'acquisitions.jsonl',{'key':key,'family':family,'seed':seed,'arm':arm,'row':row,'label':[y],
            'worker_wall_seconds':elapsed,'at':now()})
        write(OUT/'ledger.json',self.ledger)
        return [y]
    def close(self):
        self.ledger['worker_wall_seconds']+=time.monotonic()-self.started
        write(OUT/'ledger.json',self.ledger)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['prefix','branches']);args=ap.parse_args()
    verify_freeze();rss(-1);cfg=read(ROOT/'configs/study_v97.json')
    if args.phase=='prefix':
        if OUT.exists():raise ValueError('No implicit restart')
        for d in ['evaluations','requests','stderr','stdout','prefixes','branches']:(OUT/d).mkdir(parents=True)
    elif (OUT/'completed.json').exists():raise ValueError('Already completed')
    acquisition=Acquisition()
    try:
        jobs=[]
        for family in cfg['families']:
            c=candidates(family)
            for seed in cfg['seeds']:
                key=f'{family}_{seed}';prefixpath=OUT/'prefixes'/f'{key}.json'
                if args.phase=='prefix':
                    state=initial_state(c,seed)
                    for _ in range(10):
                        row=recommend(c,state);state.observe(row,acquisition.acquire(family,seed,'prefix',state,row),c.directions)
                    pool=shortlist(c,state,seed)
                    write(prefixpath,{'family':family,'seed':seed,'state':state.record(),'pool':pool,'messages':messages(c,state,pool)})
                    jobs.append({'key':key,'prefix':str(prefixpath.relative_to(ROOT)),'prefix_sha256':sha(prefixpath)})
                    print('prefix',key,flush=True)
                else:
                    p=read(prefixpath);prefix=State(**p['state']);pool=p['pool']['ranked']
                    modes=['batch_3nn','full_sequential_3nn','random_full','llm']
                    random.Random(seed+97000).shuffle(modes)
                    choicepath=ROOT/'results/v97_qwen/choices'/f'{key}.json'
                    choice=read(choicepath) if choicepath.exists() else {'selected_ids':[],'status':'unattempted'}
                    for mode in modes:
                        state=prefix.clone();available=[i for i in state.order if i not in state.ids]
                        if mode=='batch_3nn':batch=rank(c,state,pool)[:10]
                        elif mode=='random_full':batch=random.Random(seed+41000).sample(available,10)
                        elif mode=='llm':
                            batch=[p['pool']['mapping'][k] for k in choice['selected_ids']]
                            # Charged failures remain; complete budget with predeclared same-pool 3NN fallback.
                            batch += [i for i in rank(c,prefix,pool) if i not in batch][:10-len(batch)]
                        else:batch=None
                        for step in range(10):
                            row=batch[step] if batch is not None else rank(c,state,available)[0]
                            state.observe(row,acquisition.acquire(family,seed,mode,state,row),c.directions)
                        write(OUT/'branches'/f'{key}_{mode}.json',{'family':family,'seed':seed,'mode':mode,
                            'state':state.record(),'prefix_sha256':sha(prefixpath),'llm_status':choice['status'] if mode=='llm' else None,
                            'branch_order':modes})
                    print('paired',key,flush=True)
        if args.phase=='prefix':write(ART/'jobs.json',jobs)
        else:write(OUT/'completed.json',{'at':now(),'intended_pairs':5,'intended_branches':20})
    finally:acquisition.close()
if __name__=='__main__':main()
