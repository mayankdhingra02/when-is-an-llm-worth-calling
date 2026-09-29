"""Post-collection plot; no new acquisition or selected-subset aggregation."""
import json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'results/v90_flights_analysis'
def main():
    s=json.loads((OUT/'summary.json').read_text());fig,ax=plt.subplots(figsize=(10,7))
    for i,r in enumerate(s['results']):
        values=[100*g for g in r['block_relative_gains']];ax.scatter(values,[i]*5,s=20,color='#245e87',alpha=.75);ax.plot([100*r['median_block_gain']]*2,[i-.28,i+.28],color='black',lw=2)
    ax.axvline(0,color='gray',lw=1);ax.axvline(10,color='#c65b38',ls='--',lw=1);ax.set_yticks(range(12),[r['configuration']['name'] for r in s['results']]);ax.invert_yaxis();ax.set_xlabel('Within-block time reduction versus 4-thread default (%)');ax.set_title('All 12 settings × 5 blocks: exposed-workload classical grid');ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.02,'t = threads; j/f = disabled join-order/filter-pushdown pass. Dots = blocks; bars = medians.\nDashed line = frozen 10% practical margin. Descriptive only; no LLM or held-out result.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.07,1,1));fig.savefig(OUT/'grid.png',dpi=180);fig.savefig(OUT/'grid.pdf');plt.close(fig)
if __name__=='__main__':main()
