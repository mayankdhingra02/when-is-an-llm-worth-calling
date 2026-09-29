"""Frozen descriptive analysis; invalid/missing runs retain their denominator."""
import itertools,json,statistics,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/v49_analysis';SRC=ROOT/'results/v49_decoder'
def read(p):return json.loads(Path(p).read_text())
def overlap(a,b):return len(set(a)&set(b))/10
def summarize_pairs(rr):
    families={}
    for g in sorted({r['system_group'] for r in rr}):
        subset=[r for r in rr if r['system_group']==g];v=[r['overlap'] for r in subset if r['overlap'] is not None]
        families[g]={'intended':len(subset),'valid':len(v),'set_changes':sum(x<1 for x in v),
            'overlap_lower':sum(v)/len(subset),'overlap_upper':(sum(v)+len(subset)-len(v))/len(subset),
            'valid_only_overlap':statistics.mean(v) if v else None}
    return {'intended':len(rr),'valid':sum(f['valid'] for f in families.values()),'set_changes':sum(f['set_changes'] for f in families.values()),
        'family_mean_overlap_lower':statistics.mean(f['overlap_lower'] for f in families.values()),
        'family_mean_overlap_upper':statistics.mean(f['overlap_upper'] for f in families.values()),'families':families}
def main():
    assert not OUT.exists(),'Preserve original analysis'
    started=time.monotonic();jobs=read(ROOT/'artifacts/study_v49/jobs.json');ledger=read(SRC/'ledger.json');rows=[]
    for j in jobs:
        p=read(ROOT/j['prefix']);f=SRC/'choices'/f"{j['key']}.json";c=read(f) if f.exists() else {'status':'missing','selected_ids':[],'reasons':['not_completed']}
        valid=c['status']=='valid';ids=c['selected_ids']
        if valid:assert len(ids)==len(set(ids))==10 and all(i in p['mapping'] for i in ids)
        old=read(ROOT/'results/v48_sensitivity/choices'/f"{j['source_key']}.json")
        selected=[p['mapping'][i] for i in ids] if valid else None;historical=[p['mapping'][i] for i in old['selected_ids']]
        rows.append({**j,'status':c['status'],'reasons':c['reasons'],'selected_ids':ids,'selected_rows':selected,
            'historical_selected_rows':historical,'historical_overlap':overlap(selected,historical) if valid else None,
            'duplicate':c.get('duplicate',False),'displayed_first_ten_fraction':len(set(ids)&set(p['presentation'][:10]))/10 if valid else None,
            'lowest_ten_ID_set':set(ids)==set('0123456789') if valid else None})
    native=[r for r in rows if r['decoder']=='native'];forced=[r for r in rows if r['decoder']=='forced']
    index={(r['base_case'],r['loss_mode'],r['presentation_mode']):r for r in native};pairs=[]
    def pair(a,b,intervention,context):
        ov=overlap(a['selected_rows'],b['selected_rows']) if a['status']==b['status']=='valid' else None
        pairs.append({'base_case':a['base_case'],'system_group':a['system_group'],'intervention':intervention,'context':context,'a':a['key'],'b':b['key'],'overlap':ov})
    for base in sorted({r['base_case'] for r in native}):
        for order in ('base','reverse','relabel'):pair(index[base,'observed',order],index[base,'withheld',order],'loss_removal',order)
        for loss,order in itertools.product(('observed','withheld'),('reverse','relabel')):pair(index[base,loss,'base'],index[base,loss,order],order,loss)
    summaries=[{'intervention':intervention,'context':context,**summarize_pairs([p for p in pairs if (p['intervention'],p['context'])==(intervention,context)])}
        for intervention,context in [('loss_removal',x) for x in ('base','reverse','relabel')]+[(x,y) for x in ('reverse','relabel') for y in ('observed','withheld')]]
    chosen={(s['intervention'],s['context']):s for s in summaries}
    native_valid=sum(r['status']=='valid' for r in native)
    screen={'format_reliability_pass':native_valid/54>=.95,
        'loss_responsiveness_pass':sum(g['set_changes']>=2 for g in chosen['loss_removal','base']['families'].values())>=2,
        'row_stability_pass':all(chosen[o,'observed']['family_mean_overlap_lower']>=.8 for o in ('reverse','relabel')),
        'forced_reproduction_pass':all(r['historical_overlap']==1 for r in forced)}
    screen['screen_pass']=all(screen.values())
    rates=[]
    for loss,order in itertools.product(('observed','withheld'),('base','reverse','relabel')):
        rr=[r for r in native if (r['loss_mode'],r['presentation_mode'])==(loss,order)];valid=[r for r in rr if r['status']=='valid']
        rates.append({'loss_mode':loss,'presentation_mode':order,'intended':len(rr),'valid':len(valid),
            'lowest_ten_ID_sets':sum(r['lowest_ten_ID_set'] for r in valid),
            'valid_only_first_displayed_fraction':statistics.mean(r['displayed_first_ten_fraction'] for r in valid) if valid else None})
    responses=[json.loads(s) for s in (SRC/'responses.jsonl').read_text().splitlines()] if (SRC/'responses.jsonl').exists() else []
    starts=[json.loads(s) for s in (SRC/'request_starts.jsonl').read_text().splitlines()] if (SRC/'request_starts.jsonl').exists() else []
    assert len(starts)==ledger['requests']<=144
    by_key={j['key']:j for j in jobs};cost_by_mode={}
    for mode in ('native','forced'):
        rr=[r for r in responses if by_key[r['case']]['decoder']==mode];ss=[r for r in starts if by_key[r['case']]['decoder']==mode]
        cost_by_mode[mode]={'requests':len(ss),'responses':len(rr),'generated_tokens':sum(r['response']['tokens_predicted'] for r in rr),
            'input_full_context_tokens':sum(r['response']['tokens_evaluated'] for r in rr),
            'actual_prefill_tokens_reported':sum(r['response']['timings']['prompt_n'] for r in rr),'request_wall_seconds':sum(r['wall_seconds'] for r in rr)}
    family_reliability={g:{status:sum(r['system_group']==g and r['status']==status for r in native) for status in ('valid','invalid','missing')} for g in sorted({r['system_group'] for r in native})}
    cross=[]
    for mode in ('native','forced'):
        rr=[dict(r,overlap=r['historical_overlap']) for r in rows if r['decoder']==mode]
        cross.append({'decoder':mode,**summarize_pairs(rr)})
    summary={'intended_cases':63,'native_intended':54,'native_valid':native_valid,'forced_intended':9,
        'family_reliability':family_reliability,'paired_sensitivities':summaries,'historical_comparisons':cross,'ordering_rates':rates,'screen':screen,
        'cost':{'stage_seconds':ledger['stage_seconds'],'by_decoder':cost_by_mode,'requests':ledger['requests'],
            'new_objective_accesses':0,'external_spend_usd':0,'new_download_bytes':0,
            'cumulative_followup_requests_including_hardware':1732+ledger['requests'],
            'cumulative_requests_including_original100':1832+ledger['requests'],'cumulative_recorded_objective_accesses':14708},
        'analysis_seconds':time.monotonic()-started,'qualification':'Exploratory development diagnostic; no optimization-quality measurement or router validation.'}
    OUT.mkdir()
    for name,data in [('cases.json',rows),('paired.json',pairs),('summary.json',summary)]: (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
