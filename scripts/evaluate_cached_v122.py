"""Charge only the selected cached-proposal continuations after selection seal."""
import time,json
from table_check_v119 import ROOT,read,write,append,sha,candidates,MODES
from project_cached_v122 import frozen
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,best,relative_gain

def main():
    frozen();out=ROOT/'results/v122_analysis';out.mkdir(exist_ok=False);seal=read(ROOT/'results/v122_projection/selection_seal.json')
    for n,h in seal['sha256'].items():assert sha(ROOT/n)==h
    spec,c,_=candidates();count=0;start=time.monotonic();rows=[];error=None
    try:
        for choice in seal['choices']:
            key=choice['key'];p=read(ROOT/choice['prefix']);state=State(**p['state']).clone();oracle=IndexedOracle(spec,c,p['state'],lambda e:append(out/'acquisitions.jsonl',{'key':key,**e}))
            for i in choice['selected_rows']:
                if count>=50 or time.monotonic()-start>180:raise RuntimeError('Stage cap')
                count+=1;state.observe(i,oracle.acquire(i),c.directions)
            refs={m:best(State(**read(ROOT/f'results/v119_classical/arms/{key}_{m}.json')['state']),'-') for m in MODES}
            first=read(ROOT/f'results/v120_analysis/arms/{key}.json');assert first['state']['ids'][10:]==[p['pool']['mapping'][i] for i in '0123456789'];refs['presentation_first10']=best(State(**first['state']),'-')
            target=best(state,'-');r={**choice,'target':target,'references':refs,'gains':{m:relative_gain(v,target,'-') for m,v in refs.items()},'state':state.record()};write(out/'arms'/f'{key}.json',r);rows.append(r)
    except Exception as e:error=repr(e)
    finally:write(out/'summary.json',{'complete':error is None and len(rows)==5,'error':error,'intended_cases':5,'cases':rows,'actual_new_acquisitions':count,'new_model_requests':0,'historical_cache_requests':5,'historical_generated_tokens':300,'stage_seconds':time.monotonic()-start,'scope':'Exposed development cases; new projection adaptation of real V119 cached responses; original V119 format failures preserved'})
    if error:raise RuntimeError(error)
    print('Acquired',count,'recorded outcomes; zero new model requests')
if __name__=='__main__':main()
