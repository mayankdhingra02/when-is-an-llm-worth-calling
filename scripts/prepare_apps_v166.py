"""Prepare real inputs and bounded candidate domains without benchmark outcomes."""
import csv, gzip, hashlib, itertools, json, re, shutil, zipfile
from pathlib import Path
import numpy as np
from collect_smollm_v47 import ROOT,read,write,sha,now
A=ROOT/'artifacts/study_v166'; S=ROOT/'artifacts/sources/v166'
def main():
    assert not (A/'preparation.json').exists()
    receipt=read(S/'receipt.json');assert receipt['error'] is None
    for item in receipt['files']:assert sha(ROOT/item['path'])==item['sha256']
    with zipfile.ZipFile(S/'covertype.zip') as z:
        assert 'covtype.data.gz' in z.namelist()
        assert z.getinfo('covtype.data.gz').file_size<20000000
        body=gzip.decompress(z.read('covtype.data.gz'));assert len(body)<100000000
        (A/'covtype.data').write_bytes(body)
        for n in ['covtype.info','old_covtype.info']:
            if n in z.namelist(): (A/n).write_bytes(z.read(n))
    data=np.loadtxt(A/'covtype.data',delimiter=',',dtype=np.int32)
    assert data.shape==(581012,55) and np.isin(data[:,-1],range(1,8)).all()
    assert np.isin(data[:,10:54],[0,1]).all()
    assert (data[:,10:14].sum(axis=1)==1).all() and (data[:,14:54].sum(axis=1)==1).all()
    order=np.random.default_rng(16601).permutation(len(data));train=order[:65536];valid=order[65536:73728]
    assert not set(train)&set(valid)
    # Remaining rows are deliberately unused, not a claimed independent test.
    np.savez(A/'covertype.npz',train_x=data[train,:54].astype(np.float32),train_y=data[train,54]-1,valid_x=data[valid,:54].astype(np.float32),valid_y=data[valid,54]-1,train_indices=train,valid_indices=valid)
    manifest=read(ROOT/'artifacts/study_v88/data_manifest.json')
    for n,h in manifest['normalized_files'].items():assert sha(ROOT/n)==h
    polars=[dict(zip(['threads','engine','predicate_pushdown','projection_pushdown','comm_subplan_elim'],values)) for values in itertools.product([1,2,4,6],['in-memory','streaming'],[False,True],[False,True],[False,True])]
    xgb=[dict(zip(['threads','max_bin','max_depth','rounds'],values)) for values in itertools.product([1,2,4,6],[32,64,128,256],[3,6,9,12],[16,32])]
    write(A/'candidates.json',{'polars':polars,'xgboost':xgb})
    # Audit a defined prior evidence scope, preserving hits including dependency names.
    paths={ROOT/x['path'] for x in read(ROOT/'artifacts/study_v160/preparation.json')['exposure_files']}
    for folder in ['reports','configs']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and 'v166' not in p.name)
    patterns={'polars':r'\b(?:polars|pola-rs|py-polars)\b','xgboost':r'\b(?:xgboost|dmlc)\b'}
    hits={k:[] for k in patterns};scope=[]
    for p in sorted(paths):
        if not p.is_file():continue
        s=p.read_text(errors='replace');scope.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
        for key,pattern in patterns.items():
            for match in re.finditer(pattern,s,re.I):hits[key].append({'path':str(p.relative_to(ROOT)),'context':s[max(0,match.start()-70):match.end()+100]})
    write(A/'exposure_audit.json',{'scope':scope,'hits':hits,'limitation':'Scoped retained files, not proof about deleted/external histories; Polars bridges inside DuckDB do not establish native Polars execution. Shared flights workload is previously exposed.'})
    write(A/'preparation.json',{'at':now(),'objective_calls':0,'covertype_shape':list(data.shape),'train_rows':len(train),'validation_rows':len(valid),'unused_rows':len(data)-len(train)-len(valid),'split_seed':16601,'validation_role':'acquired quality constraint, not untouched prediction test','class_counts_train':np.bincount(data[train,54]-1).tolist(),'class_counts_validation':np.bincount(data[valid,54]-1).tolist(),'files':{str(p.relative_to(ROOT)):sha(p) for p in [A/'covertype.npz',A/'covtype.data',A/'candidates.json',ROOT/'data/flights_v88/query_contract.json']}|manifest['normalized_files'],'candidate_counts':{'polars':len(polars),'xgboost':len(xgb)}})
    print(json.dumps({'prepared':True,'shapes':list(data.shape),'exposure_hits':{k:len(v) for k,v in hits.items()}}))
if __name__=='__main__':main()
