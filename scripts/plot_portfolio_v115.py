"""Descriptive group means, with original and exploratory controls distinguished."""
import os,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/sampling_v114'))
import matplotlib
matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='portfolio-v115'
import matplotlib.pyplot as plt

def main():
 old=json.loads((ROOT/'results/v114_analysis/sampling_reliability.json').read_text());new=json.loads((ROOT/'results/v115_analysis/summary.json').read_text());groups=sorted(new['groups'])
 fig,ax=plt.subplots(figsize=(9,4.7),layout='constrained')
 for offset,color,name in [(-.17,'#0072B2','batch_3nn'),(0,'#D55E00','full_sequential_3nn'),(.17,'#009E73','portfolio')]:
  gains=[100*(new['groups'][g] if name=='portfolio' else old['groups'][g][name]) for g in groups]
  label={'batch_3nn':'Original batch 3NN','full_sequential_3nn':'Original sequential 3NN','portfolio':'Exploratory single portfolio'}[name]
  ax.scatter(gains,[i+offset for i in range(6)],color=color,label=label)
 ax.set(yticks=range(6),yticklabels=groups,xlabel='Mean LLM relative gain (%); positive favors LLM',title='Same 36 real LLM replicas against three B20 classical controls\nReplicas averaged within prefix, then optimization seeds within group')
 ax.axvline(0,color='gray',lw=1);ax.invert_yaxis();fig.legend(loc='outside lower center',ncol=3,fontsize=9)
 out=ROOT/'results/v115_analysis';fig.savefig(out/'controls.png',dpi=170,metadata={'Software':'matplotlib'});fig.savefig(out/'controls.svg',metadata={'Date':None});plt.close(fig)
if __name__=='__main__':main()
