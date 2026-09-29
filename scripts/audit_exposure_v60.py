"""Bounded historical identifier scan, never opens raw objective tables."""
import hashlib,json,re,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    start=time.monotonic();out=ROOT/'artifacts/study_v60/exposure_audit.json'
    if out.exists():raise FileExistsError('Preserve audit receipt')
    registry=json.loads((ROOT/'data/registry_v5.json').read_text())
    tokens={}
    for d in registry['datasets']:
        if d['system_group'] in ['redis','mongodb','storm']:
            for token in [d['system_group'],d['dataset_id'],d['path'],Path(d['path']).stem]:
                tokens.setdefault(token.lower(),set()).add(d['system_group'])
    compiled={k:re.compile(rb'(?<![a-z0-9])'+re.escape(k.encode())+rb'(?![a-z0-9])',re.I) for k in tokens}
    hits=[];files=0;total=0
    # Scan saved research JSON/JSONL and admitted manifests, not downloaded tables.
    paths=set((ROOT/'results').rglob('*.json'))|set((ROOT/'results').rglob('*.jsonl'))|set((ROOT/'data').glob('*manifest*.json'))
    for path in sorted(paths):
        if time.monotonic()-start>120:raise TimeoutError('Exposure audit 120s cap')
        data=path.read_bytes();files+=1;total+=len(data)
        found=[t for t,pattern in compiled.items() if pattern.search(data)]
        if found:
            name=str(path.relative_to(ROOT))
            category='admission_or_manifest_context' if path.parent==ROOT/'data' or name.startswith(('results/v13_admission/','results/v13_1_admission/','results/v52_admission/')) else 'new_v60_feasibility' if name.startswith('results/v60_redis_feasibility/') else 'needs_manual_review'
            hits.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'tokens':found,'possible_groups':sorted(set().union(*(tokens[t] for t in found))),'category':category})
    result={'scope':'Identifier presence audit of saved research logs/manifests; no raw downloaded objective table read',
            'not_a_proof_of_historically_untouched_labels':True,'remaining_blind_spots':['deleted or external sessions/files','unidentified aliases','unstructured text or binary records'],
            'scanned_files':files,'scanned_bytes':total,'runtime_seconds':time.monotonic()-start,'hits':hits,
            'unclassified_hit_files':sum(h['category']=='needs_manual_review' for h in hits),
            'new_objective_acquisitions':0,'new_model_calls':0}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='hits'},indent=2))
if __name__=='__main__':main()
