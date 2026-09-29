"""One charged native configuration: three solves, all correctness checked."""
import json, sys, time, resource
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import numpy as np
from scipy.io import mmread
from scipy.sparse.linalg import splu
from escalation.numerical_v94 import options, linear_certificate, lp_certificate

def main():
    request = json.loads(Path(sys.argv[1]).read_text())
    output = Path(sys.argv[2]); family = request['family']
    opts = options(family, request['configuration'])
    measurements, vectors = [], {}
    # macOS reports ru_maxrss in bytes; parent timeout bounds the whole worker.
    if family == 'superlu':
        a = mmread(ROOT/'data/native_v94/orsreg_1.mtx').tocsc()
        truth = 1. + (np.arange(a.shape[0]) % 17)/17.
        b = a @ truth
    else:
        import highspy
        assert highspy.Highs().version() == '1.7.2'
    for rep in range(3):
        with output.with_suffix('.attempts.jsonl').open('a') as f:
            f.write(json.dumps({'rep':rep,'at_unix':time.time(),'status':'started'})+'\n')
        if family == 'superlu':
            start = time.perf_counter(); lu = splu(a, **opts); x = lu.solve(b)
            elapsed = time.perf_counter()-start
            cert = linear_certificate(a, b, x, truth)
            vectors[f'x{rep}'] = x
            extra = {'factor_nonzeros': int(lu.nnz)}
            del lu
        else:
            h = highspy.Highs()
            for k, v in {**opts, 'output_flag': False, 'threads': 1, 'parallel': 'off',
                         'solver': 'simplex', 'simplex_strategy': 1, 'random_seed': 11,
                         'time_limit': 5., 'primal_feasibility_tolerance': 1e-7,
                         'dual_feasibility_tolerance': 1e-7}.items():
                assert h.setOptionValue(k,v) == highspy.HighsStatus.kOk, k
                assert h.getOptionValue(k)[1] == v, k
            assert h.readModel(str(ROOT/'artifacts/sources/v94/25fv47.mps')) == highspy.HighsStatus.kOk
            lp = h.getLp()
            start=time.perf_counter(); status=h.run(); elapsed=time.perf_counter()-start
            solution=h.getSolution(); info=h.getInfo()
            cert=lp_certificate(lp, solution.col_value, solution.row_dual, solution.col_dual)
            cert['valid'] = cert['valid'] and status == highspy.HighsStatus.kOk and h.getModelStatus() == highspy.HighsModelStatus.kOptimal
            extra={'model_status': str(h.getModelStatus()), 'run_status': str(status),
                   'simplex_iterations': info.simplex_iteration_count}
            for key, val in [('x', solution.col_value), ('y', solution.row_dual), ('z', solution.col_dual)]:
                vectors[f'{key}{rep}']=np.asarray(val)
        measurements.append({'rep':rep,'seconds':elapsed,'certificate':cert,**extra})
        with output.with_suffix('.attempts.jsonl').open('a') as f:
            f.write(json.dumps({'rep':rep,'at_unix':time.time(),'status':'returned','valid':cert['valid']})+'\n')
    valid=all(r['certificate']['valid'] for r in measurements)
    np.savez_compressed(output.with_suffix('.npz'), **vectors)
    output.write_text(json.dumps({'request':request,'options':opts,'measurements':measurements,
        'valid':valid,'objective_seconds':float(np.median([r['seconds'] for r in measurements])) if valid else 30.,
        'peak_worker_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
if __name__=='__main__':main()
