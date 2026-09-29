"""Outcome-free development diagnostics: sensitivity is NOT optimization gain."""
import itertools,json,statistics,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results/v48_sensitivity';OUT=ROOT/'results/v48_analysis'
def read(p):return json.loads(Path(p).read_text())
def overlap(a,b):return len(set(a)&set(b))/10
def main():
    if OUT.exists():raise ValueError('Preserve analysis')
    started=time.monotonic();jobs=read(ROOT/'artifacts/study_v48/jobs.json');ledger=read(SRC/'ledger.json')
    assert len(jobs)==108
    intended=[{**j,'status':'missing'} for j in jobs]
    if ledger['completed_cases']!=108:raise ValueError('Incomplete denominator; no complete-case aggregation')
    rows=[]
    for j in jobs:
        p=read(ROOT/j['prefix']);c=read(SRC/'choices'/f"{j['key']}.json")
        if c['status']!='completed' or len(c['selected_ids'])!=len(set(c['selected_ids'])) or len(c['selected_ids'])!=10:
            raise ValueError('Incomplete/failed condition; retain logs, refuse aggregate')
        ids=c['selected_ids'];selected=[p['mapping'][i] for i in ids]
        rows.append({**j,'selected_ids':ids,'selected_rows':selected,
            'lowest_ten_ID_set':set(ids)==set('0123456789'),
            'lowest_ten_ID_sequence':ids==list('0123456789'),
            'displayed_first_ten_fraction':len(set(ids)&set(p['presentation'][:10]))/10,
            'case_seconds':c['case_seconds']})
    index={(r['base_case'],r['representation'],r['loss_mode'],r['presentation_mode']):r for r in rows}
    bases=sorted({r['base_case'] for r in rows});paired=[]
    for base,rep in itertools.product(bases,('symbols','values')):
        for order in ('base','reverse','relabel'):
            a=index[base,rep,'observed',order];b=index[base,rep,'withheld',order]
            ov=overlap(a['selected_rows'],b['selected_rows'])
            paired.append({'base_case':base,'system_group':a['system_group'],'representation':rep,
                'intervention':'loss_removal','context':order,'overlap':ov,'set_changed':ov<1})
        for labels,order in itertools.product(('observed','withheld'),('reverse','relabel')):
            a=index[base,rep,labels,'base'];b=index[base,rep,labels,order]
            ov=overlap(a['selected_rows'],b['selected_rows'])
            paired.append({'base_case':base,'system_group':a['system_group'],'representation':rep,
                'intervention':order,'context':labels,'overlap':ov,'set_changed':ov<1})
    summaries=[]
    for rep in ('symbols','values'):
        for intervention,context in [('loss_removal',x) for x in ('base','reverse','relabel')]+[(x,y) for x in ('reverse','relabel') for y in ('observed','withheld')]:
            rr=[r for r in paired if (r['representation'],r['intervention'],r['context'])==(rep,intervention,context)]
            family={g:{'mean_overlap':statistics.mean(r['overlap'] for r in rr if r['system_group']==g),
                'set_changes':sum(r['set_changed'] for r in rr if r['system_group']==g),'cases':sum(r['system_group']==g for r in rr)} for g in sorted({r['system_group'] for r in rr})}
            summaries.append({'representation':rep,'intervention':intervention,'context':context,'families':family,
                'family_mean_overlap':statistics.mean(x['mean_overlap'] for x in family.values()),
                'set_changes':sum(r['set_changed'] for r in rr),'paired_cases':len(rr)})
    screens={}
    for rep in ('symbols','values'):
        selected={ (s['intervention'],s['context']):s for s in summaries if s['representation']==rep}
        responsive=sum(g['set_changes']>=2 for g in selected['loss_removal','base']['families'].values())>=2
        stable=all(selected[o,'observed']['family_mean_overlap']>=.8 for o in ('reverse','relabel'))
        screens[rep]={'loss_responsiveness_pass':responsive,'row_stability_pass':stable,'screen_pass':responsive and stable,
            'qualification':'Necessary representation screen only; does not measure useful optimization or routing.'}
    rates=[]
    for rep,labels,order in itertools.product(('symbols','values'),('observed','withheld'),('base','reverse','relabel')):
        rr=[r for r in rows if (r['representation'],r['loss_mode'],r['presentation_mode'])==(rep,labels,order)]
        rates.append({'representation':rep,'loss_mode':labels,'presentation_mode':order,'cases':len(rr),
            'lowest_ten_ID_sets':sum(r['lowest_ten_ID_set'] for r in rr),
            'lowest_ten_ID_sequences':sum(r['lowest_ten_ID_sequence'] for r in rr),
            'mean_displayed_first_ten_fraction':statistics.mean(r['displayed_first_ten_fraction'] for r in rr)})
    responses=[json.loads(s) for s in (SRC/'responses.jsonl').read_text().splitlines()]
    assert ledger['requests']==len(responses)==1080
    summary={'conditions':108,'base_prefixes':9,'families':3,'paired_sensitivities':summaries,'ordering_rates':rates,'screens':screens,
        'cost':{'requests':ledger['requests'],'stage_seconds':ledger['stage_seconds'],'input_full_context_tokens':sum(r['response']['tokens_evaluated'] for r in responses),
            'actual_prefill_tokens_reported':sum(r['response']['timings']['prompt_n'] for r in responses),'generated_choice_tokens':sum(r['response']['tokens_predicted'] for r in responses),
            'request_wall_seconds':sum(r['wall_seconds'] for r in responses),'new_objective_accesses':0,'external_spend_usd':0,'new_download_bytes':0,
            'previous_followup_requests_including_hardware':652,'cumulative_followup_requests_including_hardware':652+ledger['requests'],
            'cumulative_requests_including_original100':752+ledger['requests'],'cumulative_recorded_objective_accesses':14708},
        'analysis_seconds':time.monotonic()-started,'qualification':'Exploratory, development-only, output-sensitivity diagnostics. No performance/quality results.'}
    OUT.mkdir()
    for filename,data in [('cases.json',rows),('paired.json',paired),('summary.json',summary)]:
        (OUT/filename).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'screens':screens,'cost':summary['cost'],'paired_sensitivities':summaries},indent=2))
if __name__=='__main__':main()
