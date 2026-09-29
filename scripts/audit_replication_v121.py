"""Feature/source/exposure audit, never convert a target value."""
import csv,json,re,hashlib,time
from table_check_v121 import ROOT,read,write,sha,candidates

def main():
    spec,c,subset=candidates();assert len(c.x)==270
    for n,h in read(ROOT/'reports/source_v121.freeze.json')['sha256'].items():assert sha(ROOT/n)==h
    hits=[];files=0;total=0;start=time.monotonic();pat=re.compile(rb'(?<![a-z0-9])(?:mongodb|ss-v)(?![a-z0-9])',re.I)
    for p in sorted((ROOT/'results').rglob('*')):
        if p.suffix not in ['.json','.jsonl'] or 'v121' in str(p):continue
        assert time.monotonic()-start<180
        b=p.read_bytes();files+=1;total+=len(b)
        if pat.search(b):hits.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(b).hexdigest()})
    write(ROOT/'artifacts/study_v121/admission.json',{'scope':'Published owner runtime only, original run correctness unverified','source_manifest':read(ROOT/'artifacts/sources/v121/manifest.json'),'feature_partition':subset,'fixed':spec['fixed_features'],'exposure_scan':{'files':files,'bytes':total,'hits':hits,'certifies_external_or_deleted_history':False},'excluded_exastencils':'Owner README version/workload unknown; exact performance-stage mapping unresolved','objective_values_converted':0})
    print('270 feature-only candidates; exposure hits:',[x['path'] for x in hits])
if __name__=='__main__':main()
