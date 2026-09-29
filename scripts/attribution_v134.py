"""Retrospective measured-prefix attribution audit; no native/model/oracle imports."""
import json,hashlib,os
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))

def frac(x):return Fraction(str(x))
def gain(old,new,direction):
 a,b=frac(old),frac(new)
 if a<=0 or direction not in ['minimize','maximize']:raise ValueError('Invalid direction or positive metric')
 return (a-b)/a if direction=='minimize' else (b-a)/a

def main():
 out=ROOT/'results/v134_attribution';out.mkdir(parents=True,exist_ok=True);inputs={};rows=[]
 def read(n):
  p=ROOT/n;inputs[n]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
 def add(stage,group,seed,prefix,llm,seq,direction,fallback,source,primary=None,same=None):
  g=gain(seq,llm,direction) if primary is None else primary
  rows.append({'stage':stage,'group':group,'seed':seed,'direction':direction,'prefix':prefix,'llm_policy':llm,'sequential':seq,'fallback':fallback,'valid_model':not fallback,'gain_from_prefix_fraction':str(gain(prefix,llm,direction)),'selection_paired_gain_fraction':str(gain(seq,llm,direction)),'primary_paired_gain_fraction':str(g),'source':source,'same_configuration':same,'role':'historical_exposed_development_or_failure' if stage in [127,129,130] else 'prospective_frozen_router_test','timing_caution':group=='fftw'})
 for stage,jv in [(127,127),(129,128)]:
  source=f'results/v{stage}_analysis/comparison.json';pairs=read(source)['cases'];jobs=[j for j in read(f'artifacts/study_v{jv}/jobs.json') if j['condition']=='normal'];assert len(jobs)==len(pairs)==(30 if stage==127 else 10)
  for c in pairs:
   job=next(j for j in jobs if j['base_key']==c['key']);p=read(job.get('prefix',job.get('prefix_path')));s=p.get('state',p);direction=json.loads(read(job['messages_path'])[1]['content'])['direction'];best=(min if direction=='minimize' else max)(y[0] for y in s['labels']);assert len(s['ids'])==10
   add(stage,c['system_group'],c['seed'],best,c['target'],c['references']['full_sequential_3nn'],direction,c['fallback'],source)
   assert abs(float(Fraction(rows[-1]['primary_paired_gain_fraction']))-c['gains']['full_sequential_3nn'])<1e-9
 source='results/v130_native/comparison.json'
 for c in read(source)['rows']:add(130,'flac',c['seed'],c['prefix_best_bytes'],c['llm_bytes'],c['sequential_3nn_bytes'],'minimize',c['fallback'],source)
 source='results/v131_native/comparison.json'
 for c in read(source)['rows']:add(131,c['task'],c['seed'],c['prefix_best'],c['llm'],c['sequential_3nn'],'minimize',c['fallback'],source,Fraction(c['fresh_gain_fraction']) if c['task']=='fftw' else None,c.get('same_selected_configuration'))
 source='results/v133_native/comparison.json'
 for c in read(source)['rows']:add(133,'libjpeg',c['seed'],c['prefix_best'],c['llm'],c['sequential_3nn'],'minimize',c['fallback'],source)
 assert len(rows)==60 and len({r['group'] for r in rows})==12 and len({(r['group'],r['seed']) for r in rows})==60
 groups={}
 for group in sorted({r['group'] for r in rows}):
  rs=[r for r in rows if r['group']==group];assert len(rs)==5
  groups[group]={'stage':rs[0]['stage'],'intended':5,'fallbacks':sum(r['fallback'] for r in rs),'improved_prefix':sum(Fraction(r['gain_from_prefix_fraction'])>0 for r in rs),'beats_sequential':sum(Fraction(r['primary_paired_gain_fraction'])>0 for r in rs),'beats_sequential_over_1pct':sum(Fraction(r['primary_paired_gain_fraction'])>Fraction(1,100) for r in rs),'mean_paired_gain_fraction':str(sum(Fraction(r['primary_paired_gain_fraction']) for r in rs)/5),'role':rs[0]['role']}
 counts={}
 for name,rs in [('all_intended',rows),('valid_model_only',[r for r in rows if r['valid_model']])]:counts[name]={'cases':len(rs),'improved_prefix':sum(Fraction(r['gain_from_prefix_fraction'])>0 for r in rs),'beats_sequential':sum(Fraction(r['primary_paired_gain_fraction'])>0 for r in rs),'beats_sequential_over_1pct':sum(Fraction(r['primary_paired_gain_fraction'])>Fraction(1,100) for r in rs)}
 result={'scope':'Retrospective heterogeneous full-domain proposal-series audit, not population inference or a new held-out cohort','rows':rows,'groups':groups,'counts':counts,'new_model_requests':0,'new_objective_acquisitions':0,'prospective_router_test_groups':['fftw','libjpeg','wavpack']};(out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['# V134: where did the apparent improvement occur?','','**Retrospective audit, not a new held-out evaluation.** Sixty intended normal-condition cases from twelve families in V127/V129/V130/V131/V133. Older methods and label-rotation probes remain preserved outside this method-defined scope. No new model/native calls.','', '| Family | Stage | Intended / fallback | Improves B10 prefix | Beats sequential | Beats sequential >1% | Mean paired gain |','|---|---:|---:|---:|---:|---:|---:|']
 for g,s in groups.items():lines.append(f"|{g}|{s['stage']}|{s['intended']} / {s['fallbacks']}|{s['improved_prefix']}|{s['beats_sequential']}|{s['beats_sequential_over_1pct']}|{float(Fraction(s['mean_paired_gain_fraction'])*100):+.4f}%|")
 lines+=['','Counts are repeated-run descriptions, not independent-system success estimates. Never infer population confidence from sixty seeds. No overall mean across these unlike metrics/contracts is reported.','']
 for n,c in counts.items():lines.append(f"- {n}: {c['cases']} cases; {c['improved_prefix']} improve their prefix, {c['beats_sequential']} beat continued sequential search, {c['beats_sequential_over_1pct']} exceed 1% paired gain.")
 lines+=['','FFTW prefix attribution uses original selection times; paired efficacy uses independently remeasured medians. Its one >1% raw win uses identical selected settings and is measurement variability, not a better model choice. Do not erase that raw primary value or combine it with deterministic byte gains without this qualification.','', 'SAC has five fallback cases from the old impossible 512-token representation. Retaining their executed outcomes does not mean five successful LLM proposals. Valid-only counts are a supplementary view, not a replacement denominator. Other historical tasks differ in output capacity, initialization, native versus recorded metrics and prior exposure.','', 'Only WavPack/FFTW/libjpeg have the new frozen V132-controller decisions; the other nine groups include historical development and a failed-contract group. Those three new groups still cannot establish broad generalization. Mean gains in a group may be positive while benefits remain practically tiny. No refit, statistical significance, journal quartile or novelty claim follows from this table.','', 'V133 illustrates attribution directly: +4.5716% relative to a weak left-predictor anchor, zero improvement over its B10 prefixes, and −0.0455% versus continued search. The measurable improvement against that anchor predates escalation. This is a bounded example of why the counterfactual matters, not evidence that all earlier papers made this error.','', 'Reproduce with `.venv/bin/python scripts/attribution_v134.py`; input hashes and exact rational case rows are saved. The preregistration status is explicitly retrospective, including selection of this synthesis after these outcomes were available.']
 (ROOT/'reports/attribution_v134.md').write_text('\n'.join(lines)+'\n')
 (out/'inputs.json').write_text(json.dumps({'scope':'post-outcome source mapping; not prospective preregistration','sha256':inputs},indent=2)+'\n')
 import matplotlib
 matplotlib.use('Agg');import matplotlib.pyplot as plt
 names=list(groups);fig,ax=plt.subplots(figsize=(10,4.8));pos=list(range(len(names)));ax.barh([x+.18 for x in pos],[groups[g]['improved_prefix'] for g in names],height=.32,label='Improves B10 (selection outcome)');ax.barh([x-.18 for x in pos],[groups[g]['beats_sequential'] for g in names],height=.32,label='Beats sequential (primary outcome)');ax.set_yticks(pos,names);ax.set_xlim(0,5.7);ax.set_xticks(range(6));ax.set_xlabel('Count out of five seeds within each family');ax.legend(fontsize=8,loc='lower right');ax.set_title('Retrospective attribution audit: improvement is not incremental benefit');fig.tight_layout();fig.savefig(out/'attribution.png',dpi=180,metadata={'Software':'llm-escalation-study V134'});plt.close(fig)
 print(json.dumps({'groups':groups,'counts':counts},indent=2))
if __name__=='__main__':main()
