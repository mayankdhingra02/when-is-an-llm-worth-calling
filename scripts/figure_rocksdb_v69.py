"""Plot requested/applied cache settings from actual engine logs, not scores."""
import csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    out=ROOT/'results/v69_validity_audit';rows=[]
    for folder in sorted((ROOT/'results/v69_1_rocksdb_feasibility').glob('trial_*')):
        spec=json.loads((folder/'spec.json').read_text())
        actual=[int(x) for x in re.findall(r'^\s*capacity\s*:\s*(\d+)\s*$',(folder/'db/LOG').read_text(),re.M)]
        assert len(set(actual))==1
        rows.append({'trial':spec['trial'],'requested_cache_mib':spec['config']['cache_mib'],'applied_cache_mib':actual[0]/1024**2})
    with (out/'cache_readback.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    fig,ax=plt.subplots(figsize=(7,4));x=list(range(3));width=.34
    ax.bar([i-width/2 for i in x],[r['requested_cache_mib'] for r in rows],width,label='Requested',color='#355c7d')
    ax.bar([i+width/2 for i in x],[r['applied_cache_mib'] for r in rows],width,label='Active engine log',color='#c06c51')
    ax.set_xticks(x,['Reference 1','Contrast: INVALID','Reference 2']);ax.set_ylabel('Block cache capacity (MiB)')
    ax.set_ylim(0,10);ax.set_title('V69.1: reopen changed the contrast cache setting');ax.legend(frameon=False)
    ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.01,'Configuration diagnostic only — not evidence of optimization or LLM benefit.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,1]);fig.savefig(out/'cache_readback.png',dpi=160);fig.savefig(out/'cache_readback.svg');plt.close(fig)

if __name__=='__main__':main()
