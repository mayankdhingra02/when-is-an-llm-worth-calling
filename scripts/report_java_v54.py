"""Regenerate static scientific figures/tables from saved V54 evidence."""
import csv
import json
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    out = ROOT/'results/v54_java_screen'
    table = json.loads((out/'table.json').read_text()); s = json.loads((out/'summary.json').read_text())
    with (out/'configuration_times.csv').open('w', newline='') as f:
        w=csv.writer(f); w.writerow(['config_id','gc_threads','new_ratio','survivor_ratio','median_ms','rep1_ms','rep2_ms','rep3_ms','cv'])
        for r in table: w.writerow([r['config_id'],*r['configuration'],r['median_ms'],*r['repetition_ms'],r['cv']])
    fig, ax=plt.subplots(figsize=(10,4.5),layout='constrained')
    for rep in range(3):
        ax.scatter([r['config_id'] for r in table],[r['repetition_ms'][rep] for r in table],s=12,alpha=.45,label=f'Repetition {rep+1}')
    ax.plot([r['config_id'] for r in table],[r['median_ms'] for r in table],color='#222222',lw=1,label='Median')
    ax.set(xlabel='Fixed lexicographic configuration ID (48 settings)',ylabel='Whole Xalan iteration time (ms)',title='Fresh JVM, one warmup then one timed iteration\nAll final outputs required to equal the released reference execution')
    ax.legend(ncol=4,frameon=False)
    fig.savefig(out/'physical_times.png',dpi=170);fig.savefig(out/'physical_times.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
    for method,label,color in [('random','Random','#888888'),('nn','Greedy 3NN','#347ba4'),('rf_lcb','RF lower confidence bound','#ad7134')]:
        ax.plot(range(5),[c['best_ms'][method] for c in s['cases']],marker='o',label=label,color=color)
    ax.axhline(s['table_minimum_ms'],ls='--',color='#333333',label='Table minimum (hindsight)')
    ax.set(xticks=range(5),xticklabels=[str(c['seed']) for c in s['cases']],xlabel='Seed (one software family)',ylabel='Best acquired median time (ms)',title='Shared 10-evaluation prefix, 20 evaluations per arm\nRecorded medians; no LLM results\n' + f"Median per-setting timing CV: {s['median_configuration_cv_percent']:.2f}%")
    ax.legend(frameon=False,fontsize=8)
    fig.savefig(out/'classical_screen.png',dpi=170,bbox_inches='tight');fig.savefig(out/'classical_screen.svg',bbox_inches='tight');plt.close(fig)
    rows=['| Seed | Random ms | 3NN ms | RF-LCB ms | Portfolio headroom % |','|---|---:|---:|---:|---:|']
    for c in s['cases']:
        b=c['best_ms'];rows.append(f"| {c['seed']} | {b['random']:.0f} | {b['nn']:.0f} | {b['rf_lcb']:.0f} | {c['portfolio_headroom_percent']:.3f} |")
    (out/'case_table.md').write_text('\n'.join(rows)+'\n')
    print('Rendered two PNG/SVG scientific figures and reproducible tables.')


if __name__ == '__main__': main()
