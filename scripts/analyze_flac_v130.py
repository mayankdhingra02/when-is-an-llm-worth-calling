"""Post-collection descriptive analysis, with one implementation group."""
import json,os
from fractions import Fraction
from collect_smollm_v47 import ROOT,read,write
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
SEEDS=[11,23,37,53,71]
MODES=['sequential_3nn','batch_3nn','random_projection','random_full']

def main():
 o=ROOT/'results/v130_native';rows=[]
 for seed in SEEDS:
  arms={m:read(o/'arms'/f'{seed}_{m}.json') for m in MODES+['llm']}
  prefix=read(o/'prefixes'/f'{seed}.json');model=arms['llm']['best_bytes']
  rows.append({'seed':seed,'group':'flac','preset_bytes':prefix['labels'][0][0],'prefix_best_bytes':min(y[0] for y in prefix['labels']),'llm_bytes':model,'model_status':arms['llm']['model_status'],'fallback':arms['llm']['fallback'],**{m+'_bytes':arms[m]['best_bytes'] for m in MODES}})
 summary={}
 for m in MODES+['preset']:
  gains=[Fraction(r[m+'_bytes']-r['llm_bytes'],r[m+'_bytes']) for r in rows]
  summary[m]={'mean_gain_fraction':str(sum(gains)/5),'mean_gain_percent':float(sum(gains)/5*100),'wins':sum(g>0 for g in gains),'ties':sum(g==0 for g in gains),'losses':sum(g<0 for g in gains),'paired_gain_percent':[float(g*100) for g in gains]}
 ledger=read(ROOT/'results/v130_proposals/ledger.json')
 responses=[json.loads(l) for l in (ROOT/'results/v130_proposals/responses.jsonl').read_text().splitlines()]
 tokens={'generated_observed':sum(r['response'].get('tokens_predicted',0) for r in responses),'prefill_observed':sum(r['response'].get('tokens_evaluated',0) for r in responses),'attempts_with_missing_usage':ledger['generation_requests']-sum(type(r['response'].get('tokens_predicted')) is int and type(r['response'].get('tokens_evaluated')) is int for r in responses)}
 natives=[read(o/p/'ledger.json') for p in ['classical','continuations']]
 proposal_diagnostics=[d for s in SEEDS for d in read(o/'arms'/f'{s}_llm.json')['diagnostics']]
 diag={'proposals':len(proposal_diagnostics),'projected_nonzero':sum(d['hamming_distance']>0 for d in proposal_diagnostics),'repeated':sum(d['repeated_proposal'] for d in proposal_diagnostics),'matches_acquired':sum(d['matches_initial_observation'] for d in proposal_diagnostics)}
 result={'group_count':1,'paired_cases':5,'rows':rows,'comparisons':summary,'native_ledgers':natives,'model_ledger':ledger,'usage':tokens,'projection':diag,'determinism':read(o/'determinism.json'),'scope':'Prospective new-family descriptive pilot; all seeds/clips grouped; no learned-router or population/journal claim'}
 write(o/'comparison.json',result)
 text=['# V130: native FLAC result','','One newly executed implementation family, three fixed speech clips (26.655 seconds), five paired B10/B20 seeds. This is a descriptive pilot, not a held-out router study. Every prefix includes the strongest documented preset.','', '| Seed | Preset bytes | Sequential bytes | Model bytes | Model gain vs sequential |','|---:|---:|---:|---:|---:|']
 for r in rows:text.append(f"|{r['seed']}|{r['preset_bytes']}|{r['sequential_3nn_bytes']}|{r['llm_bytes']}|{100*(r['sequential_3nn_bytes']-r['llm_bytes'])/r['sequential_3nn_bytes']:+.4f}%|")
 text+=['','| Comparator | Mean model gain | Wins/ties/losses |','|---|---:|---:|']
 for m,v in summary.items():text.append(f"|{m}|{v['mean_gain_percent']:+.4f}%|{v['wins']}/{v['ties']}/{v['losses']}|")
 text+=['',f"Model: {ledger['generation_requests']} charged requests, {len(responses)} returned responses, {sum(r['model_status']=='valid' for r in rows)}/5 valid; {sum(r['fallback'] for r in rows)} fallback cases. Observable usage: {tokens['generated_observed']} generated and {tokens['prefill_observed']} prefill tokens; {tokens['attempts_with_missing_usage']} attempts lack complete usage. Allocated output capacity {ledger['allocated_output_tokens']}; lifecycle {ledger['stage_seconds']:.3f}s; startup {ledger.get('startup_seconds',float('nan')):.3f}s; sampled peak RSS {ledger['peak_server_rss_bytes']} bytes; resource stop {ledger['resource_stop_reason']!r}; server exit {ledger['server_exit_code']}.",f"Projection: {diag['projected_nonzero']}/{diag['proposals']} proposals needed nonzero Hamming projection, {diag['repeated']} repeated a proposal and {diag['matches_acquired']} matched acquired settings.",'',f"Actual native collection: {sum(l['configuration_attempts'] for l in natives)} configuration attempts, {sum(l['encode_attempts'] for l in natives)} encoder and {sum(l['decode_attempts'] for l in natives)} external decoder calls, plus three corpus-preparation decodes. All completed encodings passed exact sample hash/length checks and internal encoder verification. Native collection lifecycle total {sum(l['seconds'] for l in natives):.3f}s; encoder/decoder timings are raw costs, not latency-optimization evidence.",f"Separately charged post-selection preset repeats: {result['determinism']['targets']} bytes; excluded from arm budgets/selection. Actual trials comprise50 shared prefixes+250 continuations+3 repeats. Logical25 arms each useB20. No native trial was made free by overlap with another arm.",'','Estimated deployment:20 configuration trials and one model request when escalating, versus20 classical trials or one preset-only trial. Model loading, paired controls and reliability repeats are collection overhead. No dollar/energy savings estimated.','', 'The 96 argument vectors can produce identical bytes; different maxima are not necessarily different effective codec decisions. Only acquired values are analyzed, without full-domain normalization or hidden-label headroom. The three clips are correlated speech workloads of one encoder, and seeds do not add independent systems. Same-implementation decoding is a correctness limitation. No second host, music workload, extra model, routing fit, statistical generalization, novelty or journal readiness is established.','', 'Reproduce: `.venv/bin/python scripts/analyze_flac_v130.py`. Native trial records/encoded files: `results/v130_native/{classical,continuations}/`; model requests/raw outputs: `results/v130_proposals/`; frozen protocol: `reports/protocol_v130.md`.']
 (ROOT/'reports/flac_v130.md').write_text('\n'.join(text)+'\n')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,ax=plt.subplots(figsize=(7,3.8))
 for i,m in enumerate(MODES):ax.scatter([j+(i-1.5)*.08 for j in range(5)],summary[m]['paired_gain_percent'],label=m.replace('_',' '),s=45)
 ax.axhline(0,color='black',lw=.8);ax.set_xticks(range(5),SEEDS);ax.set_xlabel('Paired seed (all one FLAC group)');ax.set_ylabel('Model gain in encoded bytes (%)');ax.set_title('Native FLAC: same B10 prefix, B20 arms');ax.legend(fontsize=8);fig.tight_layout();fig.savefig(o/'comparison.png',dpi=180,metadata={'Software':'llm-escalation-study V130'});plt.close(fig)
 print(json.dumps({'comparisons':summary,'costs':tokens,'native_configurations':sum(l['configuration_attempts'] for l in natives)},indent=2))
if __name__=='__main__':main()
