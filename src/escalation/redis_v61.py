"""Fixed Redis design and exact-exit child timing; no objective-derived encoding."""
import itertools,subprocess,threading,time
import numpy as np

def grid():
    return [dict(zip(['hash-max-listpack-entries','hash-max-listpack-value','io-threads','io-threads-do-reads','hz','activerehashing'],[e,v,t,r,h,a]))
            for e,v,(t,r),h,a in itertools.product([64,512],[32,64],[(1,'no'),(2,'no'),(2,'yes'),(4,'no'),(4,'yes')],[10,100],['no','yes'])]

def encode(configs):
    # Numeric levels scaled by declared domains; Boolean controls encoded explicitly.
    return np.array([[(np.log2(c['hash-max-listpack-entries'])-6)/3,
                      np.log2(c['hash-max-listpack-value'])-5,np.log2(c['io-threads'])/2,
                      int(c['io-threads-do-reads']=='yes'),(c['hz']-10)/90,
                      int(c['activerehashing']=='yes')] for c in configs])

def timed_child(command,log_path,env,cap=15):
    start=time.monotonic();done=threading.Event();receipt={}
    with log_path.open('xb') as log:
        child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env)
        def waiter():
            receipt['exit_code']=child.wait();receipt['wall_seconds']=time.monotonic()-start;done.set()
        thread=threading.Thread(target=waiter,daemon=True);thread.start()
        try:
            if not done.wait(cap):child.kill();raise TimeoutError('Benchmark child cap')
        finally:
            if child.poll() is None:child.kill()
            done.wait(3);thread.join(timeout=1)
    if not done.is_set():raise RuntimeError('Child failed to terminate')
    if receipt['wall_seconds']>cap:raise TimeoutError('Completion past child cap')
    return receipt
