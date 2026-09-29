import csv,json
import pytest
from escalation.h2_v82 import validate,PROFILES

@pytest.mark.parametrize('corrupt',['none','reuse','answer','index'])
def test_result_contract(tmp_path,corrupt):
    c=PROFILES['reference'];truth={(q,t):(1,2) for q in range(3) for t in range(16)}
    (tmp_path/'metrics.json').write_text(json.dumps(dict(version='2.3.232',rows=100000,scored_queries=192,warmup_queries=48,**c)))
    (tmp_path/'settings.txt').write_text('RECOMPILE_ALWAYS=false\nQUERY_CACHE_SIZE=8\nANALYZE_AUTO=0\nOPTIMIZE_REUSE_RESULTS_ENGINE='+('true' if corrupt=='reuse' else 'false')+'\n')
    (tmp_path/'indexes.csv').write_text('IDX0,GRP,1\n' if corrupt=='index' else '')
    with (tmp_path/'answers.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['round','query','parameter','count','sum'])
        for r in range(4):
            for q in range(3):
                for t in range(16):w.writerow([r,q,t,1,3 if corrupt=='answer' else 2])
    if corrupt=='none':validate(tmp_path,c,truth)
    else:
        with pytest.raises(AssertionError):validate(tmp_path,c,truth)
