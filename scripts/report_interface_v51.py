"""Regenerate scientific tables and figures from V50/V51 measured records."""
import json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'));os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
 out=ROOT/'results/v51_analysis';s=json.loads((out/'summary.json').read_text());cases=json.loads((ROOT/'results/v51_classical/cases.json').read_text())
 diagnostics=[]
 for c in cases:
  key=f"{c['mode']}_{c['family']}_{c['seed']}"
  prefix=json.loads((ROOT/'results/v51_classical/prefixes'/f'{key}.json').read_text())
  best=min(y[0] for y in prefix['labels'] if y[1]<=prefix['size_cap'])
  diagnostics.append({'mode':c['mode'],'family':c['family'],'seed':c['seed'],'best_after10_ms':best,'best_recorded_ms':c['hindsight_ms'],'headroom_after10':(best-c['hindsight_ms'])/best,'already_at_recorded_best_after10':best==c['hindsight_ms']})
 (out/'checkpoint_diagnostic.json').write_text(json.dumps({'label':'Post-hoc diagnostic from saved acquired prefixes and evaluator-only minima, not a changed primary endpoint','cases':diagnostics},indent=2)+'\n')
 groups=[]
 for f in ('zstd','lz4'):
  for mode in ('api','cli'):
   rr=[r for r in cases if (r['family'],r['mode'])==(f,mode)]
   groups.append({'family':f,'mode':mode,'cases':len(rr),'mean_classical_gain_over_random':statistics.mean(r['classical_gain_over_random'] for r in rr),'mean_hindsight_headroom':statistics.mean(r['hindsight_headroom'] for r in rr),'max_hindsight_headroom':max(r['hindsight_headroom'] for r in rr),'cases_above5pct':sum(r['hindsight_headroom']>=.05 for r in rr),'wins':sum(r['classical_gain_over_random']>0 for r in rr),'ties':sum(r['classical_gain_over_random']==0 for r in rr),'harms':sum(r['classical_gain_over_random']<0 for r in rr),'size_caps':sorted({r['size_cap'] for r in rr})})
 (out/'classical_summary.json').write_text(json.dumps(groups,indent=2)+'\n')
 table=['| Family | Interface | Mean classical gain over random | W / T / H | Mean hindsight headroom | Maximum headroom |','|---|---|---:|---:|---:|---:|']
 for g in groups:table.append(f"| {g['family']} | {g['mode']} | {g['mean_classical_gain_over_random']:.3%} | {g['wins']} / {g['ties']} / {g['harms']} | {g['mean_hindsight_headroom']:.3%} | {g['max_hindsight_headroom']:.3%} |")
 (out/'classical_table.md').write_text('\n'.join(table)+'\n')
 fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
 for ax,f in zip(axes,('zstd','lz4')):
  ss=[r for r in s['settings'] if r['family']==f]
  ax.scatter([r['api_median_ms'] for r in ss],[r['cli_median_ms'] for r in ss],s=25,color='#405f8c',alpha=.75)
  low=min(min(r['api_median_ms'],r['cli_median_ms']) for r in ss);high=max(max(r['api_median_ms'],r['cli_median_ms']) for r in ss)
  ax.plot([low,high],[low,high],color='#999999',linestyle='--',linewidth=1,label='equal time')
  ax.set_xscale('log');ax.set_yscale('log');ax.set_title(f+' — 48 settings, five paired trials each');ax.set_xlabel('Native API median (ms)');ax.set_ylabel('CLI median (ms)');ax.legend(frameon=False)
 fig.suptitle('Same small workload, different interfaces\nAPI allocation/copy included; output bytes may differ')
 fig.savefig(out/'interface_timings.png',dpi=180);fig.savefig(out/'interface_timings.svg');plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
 for i,(mode,color) in enumerate([('api','#b77638'),('cli','#405f8c')]):
  values=[100*next(g['mean_hindsight_headroom'] for g in groups if g['family']==f and g['mode']==mode) for f in ('zstd','lz4')]
  ax.bar([j+(-.18 if i==0 else .18) for j in range(2)],values,width=.34,label=mode,color=color)
 ax.set_xticks(range(2),['Zstandard','LZ4']);ax.set_ylabel('Mean remaining recorded headroom (%)');ax.legend(frameon=False);ax.set_title('After 20 classical evaluations, five seeds per family\nHindsight upper reference; not an achieved LLM gain')
 fig.savefig(out/'headroom.png',dpi=180);fig.savefig(out/'headroom.svg');plt.close(fig)
 print(json.dumps(groups,indent=2))
if __name__=='__main__':main()
