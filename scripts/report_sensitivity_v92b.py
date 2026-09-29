"""Regenerate the frozen diagnostic's tables and scientific figure from real logs."""
import json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
    out=ROOT/'results/v92b_analysis';s=json.loads((out/'summary.json').read_text())
    rows=['| Representation | Intervention | Context | Changed sets / 9 | Mean row overlap |',
          '|---|---|---|---:|---:|']
    for r in s['paired_sensitivities']:
        rows.append(f"| {r['representation']} | {r['intervention']} | {r['context']} | {r['set_changes']} / 9 | {100*r['family_mean_overlap']:.1f}% |")
    (out/'sensitivity_table.md').write_text('\n'.join(rows)+'\n')
    rows=['| Representation | Losses | Presentation | Lowest-ten-ID sets / 9 | Fraction selected from first ten displayed |',
          '|---|---|---|---:|---:|']
    for r in s['ordering_rates']:
        rows.append(f"| {r['representation']} | {r['loss_mode']} | {r['presentation_mode']} | {r['lowest_ten_ID_sets']} / 9 | {100*r['mean_displayed_first_ten_fraction']:.1f}% |")
    (out/'ordering_table.md').write_text('\n'.join(rows)+'\n')
    fig,ax=plt.subplots(figsize=(9,4.3),layout='constrained')
    categories=[('loss_removal','base'),('reverse','observed'),('relabel','observed')]
    for i,(rep,color) in enumerate([('symbols','#405f8c'),('values','#b77638')]):
        vals=[100*next(r['family_mean_overlap'] for r in s['paired_sensitivities'] if (r['representation'],r['intervention'],r['context'])==(rep,change,context)) for change,context in categories]
        ax.bar([x+(.18 if i else -.18) for x in range(3)],vals,width=.34,label=rep,color=color)
    ax.set_xticks(range(3),['Remove observed losses','Reverse display order','Rotate arbitrary IDs'])
    ax.set_ylim(0,112);ax.set_ylabel('Selected configuration overlap (%)')
    ax.set_title('Qwen3-8B development diagnostic: three systems × three prefixes\nHigh overlap means choices stayed similar; it does not measure quality')
    ax.legend(loc='upper right',frameon=False,ncol=2);ax.spines[['top','right']].set_visible(False)
    fig.savefig(out/'sensitivity.png',dpi=180);fig.savefig(out/'sensitivity.svg');plt.close(fig)
    print('Regenerated tables and PNG/SVG; no new inference or objective access.')
if __name__=='__main__':main()
