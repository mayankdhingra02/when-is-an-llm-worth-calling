"""Frozen-method descriptive comparisons; fresh FFTW validation stays separate."""
import json,os,statistics
from fractions import Fraction
from collect_smollm_v47 import ROOT,read,write
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
SEEDS=[11,23,37,53,71];MODES=['sequential_3nn','batch_3nn','random_projection','random_full']
def stats(gains):
 return {'mean_fraction':str(sum(gains)/len(gains)),'mean_percent':float(sum(gains)/len(gains)*100),'wins':sum(g>0 for g in gains),'ties':sum(g==0 for g in gains),'losses':sum(g<0 for g in gains),'paired_percent':[float(g*100) for g in gains]}
def main():
 o=ROOT/'results/v131_native';val=read(o/'fresh_validation.json')['records'];rows=[];summary={}
 for task in ['wavpack','fftw']:
  comparisons={m:[] for m in MODES+['expert','default']}
  for seed in SEEDS:
   prefix=read(o/'prefixes'/f'{task}_{seed}.json');arms={m:read(o/'arms'/f'{task}_{seed}_{m}.json') for m in MODES+['llm']}
   r={'task':task,'seed':seed,'prefix_best':min(y[0] for y in prefix['labels']),'expert':prefix['labels'][0][0],'default':prefix['labels'][1][0],**{m:arms[m]['best'] for m in arms},'model_status':arms['llm']['model_status'],'fallback':arms['llm']['fallback']}
   for m in comparisons:comparisons[m].append(Fraction(r[m]-r['llm'],r[m]))
   if task=='fftw':
    medians={m:statistics.median([z['target'] for z in val if z['seed']==seed and z['mode']==m]) for m in ['sequential_3nn','llm','expert']}
    blocks=[]
    for b in range(3):
     values={z['mode']:z['target'] for z in val if z['seed']==seed and z['block']==b};blocks.append(float(Fraction(values['sequential_3nn']-values['llm'],values['sequential_3nn'])*100))
    r['fresh_medians_ns']=medians;r['fresh_gain_fraction']=str(Fraction(medians['sequential_3nn']-medians['llm'],medians['sequential_3nn']));r['fresh_gain_percent']=float(Fraction(r['fresh_gain_fraction'])*100);r['fresh_block_gain_percent']=blocks
    r['same_selected_configuration']=arms['sequential_3nn']['incumbent']==arms['llm']['incumbent']
   rows.append(r)
  summary[task]={'selection_time_comparisons':{m:stats(g) for m,g in comparisons.items()}}
 summary['fftw']['fresh_validation_primary']=stats([Fraction(r['fresh_gain_fraction']) for r in rows if r['task']=='fftw'])
 ledgers=[read(o/p/'ledger.json') for p in ['classical','continuations']];model=read(ROOT/'results/v131_proposals/ledger.json');raw=[json.loads(l) for l in (ROOT/'results/v131_proposals/responses.jsonl').read_text().splitlines()]
 usage={'generated_observed':sum(r['response'].get('tokens_predicted',0) for r in raw),'prefill_observed':sum(r['response'].get('tokens_evaluated',0) for r in raw),'attempts_missing_usage':model['generation_requests']-sum(type(r['response'].get('tokens_predicted')) is int and type(r['response'].get('tokens_evaluated')) is int for r in raw)}
 result={'groups':2,'paired_cases':10,'rows':rows,'summary':summary,'native_ledgers':ledgers,'model_ledger':model,'usage':usage,'scope':'Two prospectively fixed task groups; no router fitting, no group-level inference or journal claim'};write(o/'comparison.json',result)
 lines=['# V131 native WavPack and FFTW extension','','Two newly executed implementation families, five paired seeds each. Shared speech source is acknowledged; seeds/windows are not independent systems. Method/domain/validation protocol frozen before outcomes.','', '| Family | Evaluation | Mean model gain | Wins/ties/losses |','|---|---|---:|---:|']
 for task in summary:
  for m,s in summary[task]['selection_time_comparisons'].items():lines.append(f"|{task}|Selection vs {m}|{s['mean_percent']:+.4f}%|{s['wins']}/{s['ties']}/{s['losses']}|")
 s=summary['fftw']['fresh_validation_primary'];lines.append(f"|fftw|**Fresh validation vs sequential (primary)**|{s['mean_percent']:+.4f}%|{s['wins']}/{s['ties']}/{s['losses']}|")
 lines+=['','| FFTW seed | Fresh sequential median ns | Fresh model median ns | Relative gain | Three block gains | Same configuration? |','|---:|---:|---:|---:|---|---|']
 for r in rows:
  if r['task']=='fftw':lines.append(f"|{r['seed']}|{r['fresh_medians_ns']['sequential_3nn']}|{r['fresh_medians_ns']['llm']}|{r['fresh_gain_percent']:+.4f}%|{', '.join(f'{v:+.3f}%' for v in r['fresh_block_gain_percent'])}|{r['same_selected_configuration']}|")
 lines+=['','Fresh validation runs each frozen FFTW incumbent three more times in mixed order alongside the expert reference. Its45trials are charged separately and never fed into B20search. Different measured times for the same configuration are measurement variability, not a policy/configuration improvement. WavPack byte outcomes are deterministic checks; FFTW selection-time diagnostics should not replace the fresh primary comparison.',f"\nActual collection: {sum(l['configuration_attempts'] for l in ledgers)} configuration attempts, {sum(l['wavpack_encodes'] for l in ledgers)} WavPack encodes/{sum(l['wavpack_decodes'] for l in ledgers)} decodes and {sum(l['fftw_worker_calls'] for l in ledgers)} FFTW workers. Native stage time total {sum(l['seconds'] for l in ledgers):.3f}s. Each numerical result checked against independent NumPy pocketfft reference; full sample equality for codec outputs. Raw results retain all correctness errors/timings/commands.",f"\nModel: {model['generation_requests']} actual requests, {len(raw)} returns, {sum(r['model_status']=='valid' for r in rows)}/10 valid responses, {sum(r['fallback'] for r in rows)} fallbacks, {model['retries']} retries; observable generated/prefill tokens {usage['generated_observed']}/{usage['prefill_observed']}, missing-usage attempts {usage['attempts_missing_usage']}. Allocated output tokens {model['allocated_output_tokens']}. Lifecycle {model['stage_seconds']:.3f}s, startup {model.get('startup_seconds',float('nan')):.3f}s, peak sampled server RSS {model['peak_server_rss_bytes']}bytes; server exit{model['server_exit_code']}, resource stop{model['resource_stop_reason']!r}.",'','Deployment estimate: one selected B20path plus one model call on escalation. Paired controls, three codec repeats,45timing-validation trials, build/startup/decoding and reference computation are actual collection overhead. FFT planning cost is reported separately and would require an explicit deployment amortization assumption. No dollar/energy guarantee.','', 'Limitations: small finite domains, short correlated speech workloads, one host/model, sampled machine-load noise, approximate FFT planner time limit and possible pretraining familiarity. Only two family groups: no learned-router fit, group confidence interval, significance, journal-readiness or novelty claim. Keep prior adaptive stages and unlike task metrics separate.','', 'Reproduce `.venv/bin/python scripts/analyze_native_v131.py`; raw native data `results/v131_native/`; real model provenance `results/v131_proposals/`; frozen protocol `reports/protocol_v131.md`.']
 (ROOT/'reports/native_v131.md').write_text('\n'.join(lines)+'\n')
 import matplotlib
 matplotlib.use('Agg');import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(10,3.8))
 for ax,task in zip(axes,['wavpack','fftw']):
  selection=summary[task]['selection_time_comparisons']['sequential_3nn']['paired_percent'];ax.scatter(SEEDS,selection,label='B20 selection outcome',s=44)
  if task=='fftw':
   ax.scatter(SEEDS,summary['fftw']['fresh_validation_primary']['paired_percent'],marker='x',s=70,label='Fresh validation (primary)')
   ax.text(.98,.03,'Seeds 23, 37, 53: same configuration;\ndifferences are timing variability',transform=ax.transAxes,ha='right',fontsize=7)
  ax.axhline(0,color='black',lw=.8);ax.set_title(task);ax.set_xticks(SEEDS);ax.set_xlabel('Seed within one family');ax.set_ylabel('Model gain vs sequential (%)');ax.legend(fontsize=8)
 fig.suptitle('V131: locked native comparison, shared B10 / B20 arms');fig.tight_layout();fig.savefig(o/'comparison.png',dpi=180,metadata={'Software':'llm-escalation-study V131'});plt.close(fig)
 print(json.dumps({'summary':summary,'usage':usage},indent=2))
if __name__=='__main__':main()
