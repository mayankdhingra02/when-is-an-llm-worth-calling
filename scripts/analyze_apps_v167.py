"""Independent correctness/configuration replay and prospectively fixed admission."""
import json, math, statistics, sys
from pathlib import Path
import numpy as np
from collect_smollm_v47 import ROOT,read,write,sha,now
A=ROOT/'artifacts/study_v167'; OUT=ROOT/'results/v167_feasibility'
def cell_summary(rows,cfg):
    vals=[r['seconds'] for r in rows if r['valid_native']]
    complete=len(rows)==cfg['repeats'] and len(vals)==len(rows)
    med=statistics.median(vals) if vals else None
    mad=statistics.median(abs(v-med) for v in vals)/med if vals else None
    quality=complete and all(r['quality_valid'] for r in rows)
    return {'count':len(rows),'valid_native':sum(r['valid_native'] for r in rows),'quality_valid':sum(r['quality_valid'] for r in rows),'median_seconds':med,'relative_mad':mad,'eligible':bool(quality and med>=cfg['minimum_median_seconds'] and mad<=cfg['maximum_relative_mad'])}
def main():
    cfg=read(ROOT/'configs/feasibility_v167.json');prep=read(ROOT/'artifacts/study_v166/preparation.json');candidates=read(ROOT/'artifacts/study_v166/candidates.json')
    for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    for n,h in prep['files'].items():assert sha(ROOT/n)==h,n
    data=np.load(ROOT/'artifacts/study_v166/covertype.npz');truth=data['valid_y'];expected=read(ROOT/'data/flights_v88/query_contract.json')['expected']['answers']
    rows=[]
    for job in read(A/'plan.json'):
        path=OUT/f"{job['order']:03d}";errors=[];raw=None
        r={**job,'seconds':None,'valid_native':False,'quality_valid':False,'accuracy':None,'errors':errors}
        try:
            start=read(path/'start.json');end=read(path/'end.json')
            assert all(start[k]==v for k,v in job.items())
            assert end['return_code']==0 and end['error'] is None
            raw=read(path/'stdout.json');config=candidates[job['engine']][job['candidate']]
            assert raw['config']==config and raw['engine']==job['engine'] and raw['candidate']==job['candidate']
            assert isinstance(raw['seconds'],(int,float)) and math.isfinite(raw['seconds']) and raw['seconds']>0
            r['seconds']=raw['seconds']
            if job['engine']=='polars':
                assert raw['version']=='1.35.2' and raw['thread_pool_size']==config['threads']
                assert raw['answers']==expected and raw['query_executions']==3
                for values in raw['answers'].values():assert all(type(v) in (str,int) for row in values for v in row)
                quality=True
            else:
                assert raw['version']=='3.1.1' and raw['query_executions']==1
                assert len(raw['predictions'])==8192 and all(type(v)==int and 0<=v<7 for v in raw['predictions'])
                accuracy=float(np.mean(np.asarray(raw['predictions'])==truth));assert accuracy==raw['accuracy'];r['accuracy']=accuracy
                l=raw['booster_config']['learner'];g=l['gradient_booster'];tp=g['tree_train_param']
                assert int(l['generic_param']['nthread'])==config['threads'] and l['generic_param']['device']=='cpu'
                assert int(tp['max_bin'])==config['max_bin'] and int(tp['max_depth'])==config['max_depth']
                assert int(g['gbtree_model_param']['num_trees'])==config['rounds']*7
                assert l['objective']['name']=='multi:softmax' and int(l['learner_model_param']['num_class'])==7
                quality=accuracy>=cfg['accuracy_floor']
            r.update(valid_native=True,quality_valid=quality)
        except Exception as exc:errors.append(repr(exc))
        rows.append(r)
    cells={};admissions={}
    for engine,ids in cfg['candidate_ids'].items():
        cells[engine]={str(i):cell_summary([r for r in rows if r['engine']==engine and r['candidate']==i],cfg) for i in ids}
        native_valid=all(r['valid_native'] for r in rows if r['engine']==engine)
        count=sum(c['eligible'] for c in cells[engine].values());admissions[engine]={'admitted':native_valid and count>=cfg['minimum_eligible_cells_per_engine'],'eligible_cells':count,'required_eligible':cfg['minimum_eligible_cells_per_engine'],'all_native_valid':native_valid}
    ledger=read(OUT/'ledger.json');assert ledger['outcomes']==sum((OUT/f"{r['order']:03d}/start.json").exists() for r in rows)
    result={'scope':'prospective feasibility only, not LLM efficacy','intended_outcomes':20,'ledger':ledger,'cells':cells,'admissions':admissions,'rows':rows,'raw_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file()}}
    write(A/'analysis.json',result)
    lines=['# V167 Polars schema repair feasibility','','Twenty intended Polars native outcomes after correcting the NA null marker; V166 failures remain charged, no LLM calls. Admission is based on the frozen correctness/quality and timing rule, not model benefit.','', '| Application | Candidate | Quality-valid / 5 | Median seconds | Relative MAD | Eligible |','|---|---:|---:|---:|---:|---|']
    for engine,cs in cells.items():
        for cid,c in cs.items():lines.append(f"| {engine} | {cid} | {c['quality_valid']} | {c['median_seconds']} | {c['relative_mad']} | {c['eligible']} |")
    lines+=['','Admission: '+json.dumps(admissions), '',f"Actual charges: {ledger['outcomes']} configuration outcomes; {ledger['query_executions']} query/training executions; {ledger['seconds']:.3f} seconds collector wall time. No model requests or retries.",'','Polars reuses a previously exposed flight workload and adds CSV scan/parsing to the timed objective. XGBoost validation accuracy is an optimization constraint; it is not an untouched test result. Both tasks are now exposed development applications. Five repeats estimate local noise, not five independent systems. Failed admissions and quality-failing settings remain in the denominator. No generalized router or journal-readiness conclusion follows from admission.']
    (ROOT/'reports/feasibility_v167.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'admissions':admissions,'errors':[r for r in rows if r['errors']]}))
if __name__=='__main__':main()
