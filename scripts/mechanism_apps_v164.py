"""Descriptive mechanism/cost figure from the full completed development cohort."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'results/v164_native'
def main():
 d=json.loads((O/'comparison.json').read_text());totals={}
 for cond in ['numeric','catalog']:
  rows=[r for r in d['mechanisms'] if r['condition']==cond];totals[cond]={k:sum(r[k] for r in rows) for k in ['observed_evaluated_proposals','evaluated_projected','evaluated_duplicates','all_proposals','all_projected','all_duplicates']}
 costs=[]
 for model in ['smollm3_3b','qwen3_8b']:
  n=next(x for x in d['model_costs'] if x['model']==model and x['condition']=='numeric');c=next(x for x in d['model_costs'] if x['model']==model and x['condition']=='catalog');costs.append({'model':model,'input_token_ratio_catalog_over_numeric':c['observed_usage']['tokens_evaluated']/n['observed_usage']['tokens_evaluated'],'request_time_ratio_catalog_over_numeric':c['request_seconds']/n['request_seconds']})
 result={'scope':'Post-outcome descriptive mechanism summary, not causal mediation or independent-system significance','totals':totals,'cost_ratios':costs,'interface_robust_wins':sum(x['catalog_robust_win'] for x in d['contrasts']),'interface_robust_losses':sum(x['catalog_robust_loss'] for x in d['contrasts']),'same_setting_pairs':sum(x['same_setting'] for x in d['contrasts']),'secondary_joint_robust_wins':sum(x['joint_robust_win'] for x in d['secondary'])};(O/'mechanism.json').write_text(json.dumps(result,indent=2)+'\n')
 plt.rcParams['svg.hashsalt']='v164-mechanism';fig,axs=plt.subplots(1,2,figsize=(11,4));fig.subplots_adjust(left=.08,right=.98,top=.76,bottom=.18,wspace=.3)
 for k,cond in enumerate(['numeric','catalog']):
  vals=[totals[cond]['evaluated_projected'],totals[cond]['evaluated_duplicates']];xs=[i+(k-.5)*.32 for i in range(2)];bars=axs[0].bar(xs,vals,width=.32,label=cond,color=['#b95c2d','#176d8c'][k]);axs[0].bar_label(bars,fontsize=10,padding=3)
 axs[0].set_xticks([0,1],['Projected','Duplicate proposals']);axs[0].set_ylabel('Count among 140 evaluated proposals');axs[0].set_ylim(0,100);axs[0].legend(frameon=False)
 for k,key in enumerate(['input_token_ratio_catalog_over_numeric','request_time_ratio_catalog_over_numeric']):
  bars=axs[1].bar([i+(k-.5)*.32 for i in range(2)],[c[key] for c in costs],width=.32,label=['Input tokens','Request time'][k],color=['#677b8f','#a68047'][k]);axs[1].bar_label(bars,fmt='%.2f',padding=3,fontsize=9)
 axs[1].set_xticks([0,1],['SmolLM3-3B','Qwen3-8B']);axs[1].axhline(1,color='gray',ls=':');axs[1].set_ylim(0,3.3);axs[1].set_ylabel('Catalog / numeric ratio');axs[1].legend(frameon=False)
 for ax in axs:ax.grid(axis='y',alpha=.15)
 fig.suptitle('The catalog reduced proposal corrections and increased inference cost\nNo robust 10% interface gain; 17/20 pairs selected the same setting');fig.savefig(O/'mechanism.png',dpi=160,metadata={'Software':'V164'});fig.savefig(O/'mechanism.svg',metadata={'Date':None});plt.close(fig);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
