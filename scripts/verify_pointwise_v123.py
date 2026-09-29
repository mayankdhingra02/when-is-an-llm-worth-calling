"""Replay saved requests and source cells, without inference or new acquisitions."""
import json,csv
from collect_smollm_v47 import ROOT,read,write,sha
from analyze_pointwise_v123 import frozen,candidates,references,scores_and_diagnostics,selection,OUT
from pointwise_v123 import messages,payload,parse
from escalation.core import State,losses
from escalation.transfer_v41 import best,relative_gain

def main():
    frozen();ledger=read(ROOT/'results/v123_pointwise/ledger.json');jobs=read(ROOT/'artifacts/study_v123/jobs.json');jm={j['key']:j for j in jobs};starts=[json.loads(x) for x in (ROOT/'results/v123_pointwise/generation_starts.jsonl').read_text().splitlines()];raw=[json.loads(x) for x in (ROOT/'results/v123_pointwise/responses.jsonl').read_text().splitlines()]
    assert len(starts)==ledger['generation_requests']<=99 and len(raw)<=len(starts);assert ledger['allocated_output_tokens']==16*len(starts)<=1584 and ledger['retries']==ledger['external_spend_usd']==0 and ledger['peak_server_rss_bytes']<=8589934592 and ledger['stage_seconds']<=900
    assert [s['identity'] for s in starts]==[j['key'] for j in jobs[:len(starts)]]
    for n,h in read(ROOT/'results/v123_pointwise/preflight_seal.json')['sha256'].items():assert sha(ROOT/n)==h
    for s in starts:
        j=jm[s['identity']];p=read(ROOT/j['prefix']);spec,_=candidates(j['dataset']);expected=messages(p,j['candidate_id'],j['condition'],spec['meaning']);pre=read(ROOT/f"results/v123_pointwise/preflight/{j['key']}.json")
        assert expected==pre['messages']==read(ROOT/j['messages_path']);assert s['payload']==payload(pre['rendered']['prompt']);assert len(pre['prompt_tokens'])+16<=4096
    started={s['identity']:s for s in starts};assert len(started)==len(starts)
    for r in raw:assert r['key'] in started
    scores,diag=scores_and_diagnostics();assert diag==read(OUT/'diagnostics.json')
    for n,h in read(OUT/'selection_seal.json')['sha256'].items():assert sha(ROOT/n)==h
    summary=read(OUT/'summary.json');assert summary['complete'] and len(summary['cases'])==3 and summary['actual_new_acquisitions']==30
    events=[json.loads(x) for x in (OUT/'acquisitions.jsonl').read_text().splitlines()];assert len(events)==30
    for job in read(ROOT/'artifacts/study_v123/cases.json'):
        selected=selection(job,scores);assert selected==read(OUT/'choices'/f"{job['key']}.json");p=read(ROOT/job['prefix']);spec,c=candidates(job['dataset']);body=json.loads(p['messages'][1]['content'].split('\n',1)[1])
        assert [o['loss'] for o in body['observations']]==list(losses(p['state']['labels'],c.directions))
        state=State(**p['state']).clone();source=(ROOT/spec['path']).read_text().splitlines();header=next(csv.reader([source[0]],delimiter=spec['delimiter']))
        for cid,cond in [(i,'normal') for i in '0123456789ABCDEFGHIJ']:
            user=json.loads(messages(p,cid,cond,spec['meaning'])[1]['content']);assert user['new_configuration']==list(c.x[p['pool']['mapping'][cid]])
            assert [o['settings'] for o in user['observations']]==[list(c.x[i]) for i in state.ids]
        es=[e for e in events if e['key']==job['key']];assert [e['row_id'] for e in es]==selected['selected_rows']
        for e in es:
            assert e['source_line']==c.source_ids[e['row_id']];row=dict(zip(header,next(csv.reader([source[e['source_line']-1]],delimiter=spec['delimiter']))));assert row[spec['primary_objective']]==e['raw_target'];assert tuple(float(row[n]) for n in c.names)==c.x[e['row_id']];state.observe(e['row_id'],[float(e['raw_target'])],c.directions)
        arm=read(OUT/'arms'/f"{job['key']}.json");assert state.record()==arm['state'] and len(set(state.ids))==20 and best(state,spec['direction'])==arm['target'];refs=references(job,p,spec['direction']);assert refs==arm['references'];assert arm['gains']=={m:relative_gain(v,arm['target'],spec['direction']) for m,v in refs.items()}
    result={'verified':True,'charged_requests':len(starts),'responses_replayed':len(raw),'source_events_replayed':30,'paired_cases':3,'new_model_requests':0,'new_acquisitions':0};write(ROOT/'artifacts/study_v123/verification.json',result);print(result)
if __name__=='__main__':main()
