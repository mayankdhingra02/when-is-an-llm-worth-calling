"""Generate fixed inputs and freeze utility-admission trials before timings."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.candidate_tasks_v66 import SORT_N,IMAGE_SIDE,DUCK_N,expected_query,sorted_digest,sort_line,image_pixels,grids
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    out=ROOT/'data/generated_v66';out.mkdir(exist_ok=False)
    with (out/'sort_input.txt').open('wb') as stream:
        for i in range(SORT_N):stream.write(sort_line((104729*i+314159)%SORT_N))
    (out/'input.pgm').write_bytes(f'P5\n{IMAGE_SIDE} {IMAGE_SIDE}\n255\n'.encode()+image_pixels())
    (out/'query_expected.json').write_text(json.dumps(expected_query())+'\n')
    manifest={'sort_rows':SORT_N,'sort_permutation':{'multiplier':104729,'offset':314159,'modulus':SORT_N},'sort_expected_sha256':sorted_digest(),'duckdb_fact_rows':DUCK_N,'duckdb_dimension_rows':4096,'image_side':IMAGE_SIDE,'generated_application_workloads':True,'production_representativeness_claim':False,'roles':{f:'development_admission_only' for f in grids()},'sha256':{p.name:sha(p) for p in sorted(out.iterdir())}}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'grids.json').write_text(json.dumps(grids(),indent=2)+'\n')
    pairs={'duckdb':([1,'256MB',12],[8,'64MB',0]),'gnu_sort':([1,'16M',16],[8,'1M',2]),'openjpeg':([64,5,1024,1],[16,3,128,2])}
    schedule=[]
    for family,(reference,contrast) in pairs.items():
        for label,config in [('reference',reference),('contrast',contrast),('reference_repeat',reference)]:
            assert tuple(config) in grids()[family]
            schedule.append({'trial':len(schedule),'family':family,'condition':label,'configuration':config})
    (ROOT/'artifacts/study_v66/schedule.json').write_text(json.dumps(schedule,indent=2)+'\n')
    paths=[ROOT/p for p in ['reports/protocol_v66_admission.md','scripts/prepare_candidates_v66.py','scripts/worker_candidates_v66.py','scripts/collect_candidates_v66.py','src/escalation/candidate_tasks_v66.py','src/escalation/bounded_process_v57.py','src/escalation/redis_v61.py','scripts/run_planning_v55.py','src/escalation/legal_proposals_v66.py','artifacts/study_v66/schedule.json','artifacts/study_v66/binaries.json','artifacts/study_v66/exposure.json','artifacts/sources/v66/manifest.json','requirements.lock.txt']]
    paths+=list(out.iterdir())+[ROOT/name for name in json.loads((ROOT/'artifacts/study_v66/binaries.json').read_text())]
    freeze=ROOT/'reports/protocol_v66_admission.freeze.json';assert not freeze.exists()
    freeze.write_text(json.dumps({'before_timed_application_trials':True,'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}},indent=2)+'\n')
    print(sha(freeze))
