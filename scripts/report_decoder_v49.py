"""Render measured decoder diagnostics, including intended denominators."""
import json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'));os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
    out=ROOT/'results/v49_analysis';s=json.loads((out/'summary.json').read_text());old=json.loads((ROOT/'results/v48_analysis/summary.json').read_text())
    table=['| Intervention | Context | Valid pairs / intended | Changed valid sets | Overlap bounds |','|---|---|---:|---:|---:|']
    for r in s['paired_sensitivities']:
        table.append(f"| {r['intervention']} | {r['context']} | {r['valid']} / {r['intended']} | {r['set_changes']} | {r['family_mean_overlap_lower']:.1%}–{r['family_mean_overlap_upper']:.1%} |")
    (out/'sensitivity_table.md').write_text('\n'.join(table)+'\n')
    rates=['| Losses | Presentation | Valid / intended | Lowest ten ID sets | First ten displayed (valid only) |','|---|---|---:|---:|---:|']
    for r in s['ordering_rates']:
        rate='unknown' if r['valid_only_first_displayed_fraction'] is None else f"{r['valid_only_first_displayed_fraction']:.1%}"
        rates.append(f"| {r['loss_mode']} | {r['presentation_mode']} | {r['valid']} / {r['intended']} | {r['lowest_ten_ID_sets']} | {rate} |")
    (out/'ordering_table.md').write_text('\n'.join(rates)+'\n')
    categories=[('loss_removal','base'),('reverse','observed'),('relabel','observed')]
    fig,ax=plt.subplots(figsize=(10,4.8),layout='constrained')
    previous=[100*next(r['family_mean_overlap'] for r in old['paired_sensitivities'] if (r['representation'],r['intervention'],r['context'])==('symbols',i,c)) for i,c in categories]
    low=[100*next(r['family_mean_overlap_lower'] for r in s['paired_sensitivities'] if (r['intervention'],r['context'])==(i,c)) for i,c in categories]
    high=[100*next(r['family_mean_overlap_upper'] for r in s['paired_sensitivities'] if (r['intervention'],r['context'])==(i,c)) for i,c in categories]
    ax.bar([i-.19 for i in range(3)],previous,width=.35,color='#405f8c',label='Forced IDs (V48)')
    ax.bar([i+.19 for i in range(3)],low,width=.35,color='#b77638',label='Native response (V49), lower bound')
    ax.bar([i+.19 for i in range(3)],[h-l for h,l in zip(high,low)],bottom=low,width=.35,color='none',edgecolor='#b77638',hatch='///',label='Uncertainty from invalid outputs')
    ax.set_xticks(range(3),['Remove observed losses','Reverse display order','Rotate arbitrary IDs'])
    ax.set_ylim(0,130);ax.set_yticks([0,20,40,60,80,100]);ax.set_ylabel('Selected configuration overlap (%)')
    ax.set_title('Decoder comparison: three development systems × three prefixes\nOverlap measures sensitivity, not optimization quality')
    ax.legend(loc='upper center',frameon=False,ncol=1,fontsize=8);ax.spines[['top','right']].set_visible(False)
    fig.savefig(out/'decoder_sensitivity.png',dpi=180);fig.savefig(out/'decoder_sensitivity.svg');plt.close(fig)
    print('Rendered tables and PNG/SVG from saved measured results.')
if __name__=='__main__':main()
