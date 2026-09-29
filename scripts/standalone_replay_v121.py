"""Standard-library saved-evidence replay; no model calls or new acquisitions."""
from pathlib import Path
import json,hashlib,csv,math,sys
ROOT=Path(__file__).resolve().parent

def read(n):return json.loads((ROOT/n).read_text())
def lines(n):return [json.loads(s) for s in (ROOT/n).read_text().splitlines()]
def main():
    manifest=read('manifest.json')
    for n,m in manifest['files'].items():
        b=(ROOT/n).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],n
    spec=read('data/manifest_v121.json')['datasets'][0];p=ROOT/spec['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==spec['sha256']
    raw=p.read_text().splitlines();head=next(csv.reader([raw[0]],delimiter=';'));sources=[];seen=set()
    for line,text in enumerate(raw[1:],2):
        row=dict(zip(head,next(csv.reader([text],delimiter=';'))));x=tuple(float(row[k]) for k in spec['feature_names'])
        if x in seen:continue
        seen.add(x)
        if all(float(row[k])==v for k,v in spec['fixed_features'].items()):sources.append(line)
    assert len(sources)==270
    journals=lines('results/v121_classical/acquisitions.jsonl')+lines('results/v121_analysis/acquisitions.jsonl');assert len(journals)==400
    for e in journals:
        assert e['source_line']==sources[e['row_id']];row=dict(zip(head,next(csv.reader([raw[e['source_line']-1]],delimiter=';'))));assert row['performance']==e['raw_target'] and math.isfinite(float(e['raw_target'])) and float(e['raw_target'])>0
    starts=lines('results/v121_qwen/generation_starts.jsonl');responses=lines('results/v121_qwen/responses.jsonl');sm={s['identity']:s for s in starts};rm={s['request_id']:s for s in responses}
    ledger=read('results/v121_qwen/ledger.json');assert len(sm)==len(rm)==len(starts)==len(responses)==ledger['generation_requests']==100 and ledger['server_exit_code']==0
    assert ledger['retries']==ledger['external_spend_usd']==0 and ledger['allocated_output_tokens']==100
    summary=read('results/v121_analysis/summary.json');cases={r['key']:r for r in summary['cases']};first=0;unchanged=0;normalids={}
    for job in read('artifacts/study_v121/model_jobs.json'):
        key=job['key'];p=read(job['prefix']);orig=read(job['original_prefix']);assert p['state']==orig['state'] and p['pool']==orig['pool']
        origbody=json.loads(orig['messages'][1]['content'].split('\n',1)[1]);body=json.loads(p['messages'][1]['content'].split('\n',1)[1])
        if job['condition']=='loss_blind':
            for row in origbody['observations']:row['loss']=.5
        assert origbody==body
        pre=read(f'results/v121_qwen/preflight/{key}.json');assert pre['messages']==p['messages'];used=[]
        for step in range(10):
            k=f'{key}_{step}';payload=sm[k]['payload'];response=rm[k];assert response['payload']==payload
            assert payload['prompt']==pre['rendered']['prompt']+''.join(i+'\n' for i in used)
            assert payload['grammar']=='root ::= '+' | '.join(json.dumps(i) for i in '0123456789ABCDEFGHIJ' if i not in used)
            assert payload['n_predict']==1 and payload['temperature']==0 and payload['cache_prompt']==bool(step)
            out=response['response'];v=out['content'];assert v in '0123456789ABCDEFGHIJ' and len(v)==1 and v not in used and out['tokens_predicted']==1 and out['truncated'] is False;used.append(v)
        choice=read(f'results/v121_qwen/choices/{key}.json');assert choice['selected_ids']==used and choice['status']=='completed'
        arm=read(f'results/v121_analysis/arms/{key}.json');selected=[p['pool']['mapping'][i] for i in used];assert arm['state']['ids']==p['state']['ids']+selected and len(set(arm['state']['ids']))==20
        es=[e for e in journals if e['namespace']=='measured_v121_recorded' and e['key']==key];assert len(es)==10 and [e['row_id'] for e in es]==selected
        assert arm['state']['labels']==p['state']['labels']+[[float(e['raw_target'])] for e in es]
        target=min(y[0] for y in arm['state']['labels']);assert target==cases[key]['target']
        for mode,reference in cases[key]['references'].items():
            c=read(f"results/v121_classical/arms/{job['base_key']}_{mode}.json");assert c['state']['ids'][:10]==p['state']['ids'];assert reference==min(y[0] for y in c['state']['labels']);assert cases[key]['gains'][mode]==(reference-target)/reference
        if job['condition']=='normal':first+=used==list('0123456789');normalids[job['base_key']]=used
        else:unchanged+=used==normalids[job['base_key']]
    assert first==5 and unchanged==4
    for old in read('results/v120_analysis/summary.json')['cases']:
        p=read(f"results/v119_classical/prefixes/{old['key']}.json");a=read(f"results/v120_analysis/arms/{old['key']}.json");assert [p['pool']['mapping'][i] for i in '0123456789']==a['state']['ids'][10:]==old['selected_rows'];assert old['target']==min(v[0] for v in a['state']['labels'])
    print(json.dumps({'verified':True,'hashed_files':len(manifest['files']),'recorded_events':400,'real_requests_replayed':100,'normal_first10_matches':first,'loss_blind_identical_cases':unchanged,'storm_first10_matches':5,'new_model_requests':0,'new_acquisitions':0}))
if __name__=='__main__':main()
