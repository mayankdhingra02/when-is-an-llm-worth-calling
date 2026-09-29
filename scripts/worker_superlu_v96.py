"""One charged diagnostic configuration, three actual native solves."""
import ctypes, faulthandler, json, resource, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import scipy.sparse.linalg._dsolve._superlu as native
from scipy.io import mmread
from scipy.sparse.linalg import splu
from escalation.numerical_v94 import PERMUTATIONS, linear_certificate

def main():
    faulthandler.enable()
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    req = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]); config = req['configuration']
    library = ctypes.CDLL(native.__file__)
    library.sp_ienv.argtypes = [ctypes.c_int]
    library.sp_ienv.restype = ctypes.c_int
    defaults = [library.sp_ienv(i) for i in (1, 2)]
    assert defaults == [20, 10], defaults
    a = mmread(ROOT / 'data/native_v94/orsreg_1.mtx').tocsc()
    truth = 1. + (np.arange(a.shape[0]) % 17) / 17.
    b = a @ truth
    opts = dict(permc_spec=PERMUTATIONS[config[0]], diag_pivot_thresh=config[1],
                relax=config[2], panel_size=config[3])
    measurements = []
    def journal(row):
        with out.with_suffix('.attempts.jsonl').open('a') as f:
            f.write(json.dumps({'at_unix':time.time(), **row}) + '\n')
    journal(dict(status='native_defaults', defaults=defaults, options=opts))
    for rep in range(3):
        journal(dict(rep=rep, status='started'))
        start = time.perf_counter()
        lu = splu(a, **opts); x = lu.solve(b)
        elapsed = time.perf_counter() - start
        cert = linear_certificate(a, b, x, truth)
        np.save(out.with_name(out.stem + f'_x{rep}.npy'), x, allow_pickle=False)
        measurement = dict(rep=rep, seconds=elapsed, certificate=cert)
        measurements.append(measurement)
        journal(dict(status='returned', **measurement))
        del lu
    out.write_text(json.dumps(dict(request=req, measurements=measurements,
        peak_worker_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss), indent=2) + '\n')

if __name__ == '__main__':
    main()
