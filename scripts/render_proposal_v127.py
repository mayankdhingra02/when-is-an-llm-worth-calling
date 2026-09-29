"""Descriptive paired gains on six exposed families; no inferential intervals."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'results/v127_analysis/comparison.json').read_text());fs=s['families'];fig,ax=plt.subplots(figsize=(10,5.3));xs=list(range(len(fs)))
for k,(mode,label,color) in enumerate([('full_sequential_3nn','Full-domain sequential3NN','#24748b'),('random_projection','Matched random proposals','#ac7444'),('full_batch_3nn','Full-domain batch3NN','#777777')]):
 ax.bar([x+(k-1)*.25 for x in xs],[100*f['means'][mode] for f in fs],.24,label=label,color=color)
ax.axhline(0,color='#333333',linewidth=.9);ax.set_xticks(xs,[f['system_group'] for f in fs]);ax.set_ylabel('Model relative gain over comparator (%)');ax.set_title('Real full-domain proposals: family means over five paired prefixes');ax.legend(frameon=False,fontsize=9);ax.spines[['top','right']].set_visible(False)
fig.text(.01,.02,'Exposed development data; failed responses retain their declared classical fallback and model cost.\nPositive bars favor the model; no held-out routing, significance or journal-readiness claim.',fontsize=9);fig.tight_layout(rect=[0,.09,1,1]);fig.savefig(ROOT/'results/v127_analysis/proposals.png',dpi=160,metadata={'Software':'llm-escalation-study v127'});plt.close(fig)
