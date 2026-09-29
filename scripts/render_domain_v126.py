"""Descriptive figure of acquired-domain bounds, never achieved optimizer scores."""
import json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'results/v126_domain_audit/comparison.json').read_text());families=s['families'];names=[f['system_group'] for f in families];pool=[]
for n in names:
 rs=[r for r in s['cases'] if r['system_group']==n]
 pool.append(100*statistics.mean((r['references']['full_sequential_3nn']-r['shortlist_best'])/r['references']['full_sequential_3nn']*(1 if r['direction']=='-' else -1) for r in rs))
fig,ax=plt.subplots(figsize=(9.5,5.1));xs=list(range(6))
ax.bar([x-.18 for x in xs],pool,.36,label='Best possible within original shortlist',color='#7f8c8d')
ax.bar([x+.18 for x in xs],[100*f['mean_global_gain_vs_sequential'] for f in families],.36,label='Best possible in admitted domain',color='#24748b')
ax.axhline(0,color='#333333',linewidth=.8);ax.axhline(5,color='#a64632',linestyle='--',linewidth=1,label='Predeclared 5% practical margin')
ax.set_xticks(xs,['BerkeleyDB','Dune/HSMGP','HIPAcc','LLVM','OpenVPN','SAC']);ax.set_ylabel('Mean maximum relative gain vs sequential3NN (%)');ax.set_title('Hindsight headroom: six exposed families, five prefixes each');ax.legend(frameon=False,fontsize=9,loc='upper right');ax.spines[['top','right']].set_visible(False)
fig.text(.01,.02,'Non-deployable bounds from charged recorded outcomes. These bars are not achieved LLM gains.\nDomain is feature-restricted/subsampled; seeds do not constitute independent systems.',fontsize=9)
fig.tight_layout(rect=[0,.09,1,1]);fig.savefig(ROOT/'results/v126_domain_audit/headroom.png',dpi=160,metadata={'Software':'llm-escalation-study v126'});plt.close(fig)
