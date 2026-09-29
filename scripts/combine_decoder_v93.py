"""Derived view only. Preserve raw attempts and bind each copy to its origin."""
import json,shutil
from collect_smollm_v47 import ROOT,read,write,sha,now
OUT=ROOT/'results/v93_combined';SOURCES=[ROOT/'results/v93_decoder',ROOT/'results/v93b_decoder']

def main():
    assert not OUT.exists();a,b=[read(p/'ledger.json') for p in SOURCES]
    assert a['generation_requests']==67 and a['resource_stop_reason']=='server_rss_cap' and a['server_exit_code']==-9
    assert b['generation_requests']==77 and b['server_exit_code']==0 and b['resource_stop_reason'] is None
    assert a['stage_seconds']+b['stage_seconds']<1800 and b['peak_server_rss_bytes']<=8589934592
    OUT.mkdir();origins={};context={};intended=read(ROOT/'artifacts/study_v93/jobs.json')
    def origin(p):
        n=str(p.relative_to(ROOT));origins[n]=sha(p);return n
    for folder in ['preflight','choices']:
        (OUT/folder).mkdir()
        for source in SOURCES:
            for p in sorted((source/folder).glob('*.json')):
                dest=OUT/folder/p.name
                if folder=='preflight' and dest.exists():
                    assert read(dest)['messages']==read(p)['messages']
                value=read(p);value['_origin_path']=origin(p);write(dest,value)
                if folder=='choices':
                    assert value['key'] not in context
                    context[value['key']]=8192 if source==SOURCES[0] else 4096
    for name in ['request_starts.jsonl','responses.jsonl','generation_starts.jsonl','errors.jsonl']:
        rows=[]
        for source in SOURCES:
            p=source/name
            if not p.exists():continue
            n=origin(p)
            for i,line in enumerate(p.read_text().splitlines(),1):
                value=json.loads(line);value.update(_origin_path=n,_origin_line=i)
                if name=='generation_starts.jsonl':value['collection_generation']=len(rows)+1
                rows.append(value)
        (OUT/name).write_text(''.join(json.dumps(v)+'\n' for v in rows))
    seals=[read(p/'preflight_seal.json') for p in SOURCES]
    for p in SOURCES:origin(p/'ledger.json');origin(p/'preflight_seal.json')
    write(OUT/'preflight_seal.json',{'at':now(),'original_preflight_at':[s['at'] for s in seals],'qualification':'Original per-stage preflight times and hashes retained; this derived view was created after collection.', 'original_seals':[str((p/'preflight_seal.json').relative_to(ROOT)) for p in SOURCES], 'sha256':{str(p.relative_to(ROOT)):sha(p) for p in (OUT/'preflight').glob('*.json')}})
    starts=[json.loads(x) for x in (OUT/'request_starts.jsonl').read_text().splitlines()];responses=[json.loads(x) for x in (OUT/'responses.jsonl').read_text().splitlines()]
    assert len(starts)==144 and len(responses)==143 and len({s['request_id'] for s in starts})==144
    ids={s['request_id'] for s in responses};failed=[s for s in starts if s['request_id'] not in ids];assert len(failed)==1
    coverage=[]
    for j in intended:
        p=OUT/'choices'/f"{j['key']}.json"
        coverage.append({**j,'status':read(p)['status'] if p.exists() else ('failed_after_request' if any(s['case']==j['key'] for s in starts) else 'unattempted'), 'context_tokens':context.get(j['key'],8192)})
    write(OUT/'coverage.json',coverage)
    write(OUT/'ledger.json',{'generation_requests':144,'scientific_requests':144,'compatibility_requests':0,'http_requests':a['http_requests']+b['http_requests'],'stage_seconds':a['stage_seconds']+b['stage_seconds'],'completed_cases':a['completed_cases']+b['completed_cases'],'valid_cases':a['valid_cases']+b['valid_cases'],'peak_server_rss_bytes':max(a['peak_server_rss_bytes'],b['peak_server_rss_bytes']),'server_exit_codes':[a['server_exit_code'],b['server_exit_code']],'resource_stop_reason':'first_stage_rss_cap','retries':0,'objective_accesses':0,'external_spend_usd':0,'returned_generated_tokens':a['generated_tokens']+b['generated_tokens'],'failed_request_usage':'unknown; up to its allocated 128-token cap, never zero-imputed','failed_requests':1,'unattempted_cases':sum(x['status']=='unattempted' for x in coverage),'source_ledgers':[str((p/'ledger.json').relative_to(ROOT)) for p in SOURCES],'qualification':'Derived two-context view with one unretried failure; not a clean single-runtime replication'})
    write(OUT/'origins.json',{'sha256':origins,'failed_request_ids':[s['request_id'] for s in failed]})
    print('Combined 144 charges, 143 responses, 62 completed cases, one unretried failure; originals unchanged')
if __name__=='__main__':main()
