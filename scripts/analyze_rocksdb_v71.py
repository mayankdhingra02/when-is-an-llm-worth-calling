"""Descriptive confirmed incumbents; no global optimum, learned router or gate."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    source=ROOT/'results/v71_rocksdb_classical';summary=json.loads((source/'summary.json').read_text());assert summary['complete']
    out=ROOT/'results/v71_rocksdb_analysis';out.mkdir(exist_ok=False)
    rows=[];comparisons=[]
    for case in summary['cases']:
        medians={}
        for method in ['random','nn','rf_lcb']:
            search=case['arms'][method];values=[x['value_ms'] for x in case['confirmation'][method]]
            median=statistics.median(values);medians[method]=median
            minimum=min(o['value_ms'] for o in search)
            rows.append({'seed':case['seed'],'method':method,'selected_config_id':case['selected_config_ids'][method],
                'search_evaluations':17,'confirmation_evaluations':3,'inclusive_budget':20,
                'search_minimum_ms':minimum,'confirmation_ms':values,'confirmed_median_ms':median,
                'confirmation_cv':statistics.stdev(values)/statistics.mean(values),
                'confirmation_minus_search_percent':100*(median-minimum)/minimum})
        comparisons.append({'seed':case['seed'],'rf_vs_random_percent':100*(medians['random']-medians['rf_lcb'])/medians['random'],
            'rf_vs_nn_percent':100*(medians['nn']-medians['rf_lcb'])/medians['nn']})
    acquisitions=json.loads((source/'acquisitions.json').read_text())
    result={'scope':'one development family, descriptive live measurements; no global optimum or LLM comparison',
        'cases':rows,'comparisons':comparisons,'physical_evaluations':200,'logical_arm_evaluations':300,
        'distinct_measured_configuration_vectors':len({r['config_id'] for r in acquisitions}),
        'mean_confirmed_median_ms':{m:statistics.mean(r['confirmed_median_ms'] for r in rows if r['method']==m) for m in ['random','nn','rf_lcb']},
        'median_confirmation_cv':statistics.median(r['confirmation_cv'] for r in rows),
        'rf_faster_than_random_count':sum(x['rf_vs_random_percent']>0 for x in comparisons),
        'rf_faster_than_nn_count':sum(x['rf_vs_nn_percent']>0 for x in comparisons),
        'independent_families':1,'model_requests':0}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    with (out/'incumbents.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    fig,ax=plt.subplots(figsize=(8,4.5));colors={'random':'#666666','nn':'#387ca3','rf_lcb':'#bc5d38'}
    labels={'random':'Random','nn':'3NN','rf_lcb':'RF-LCB'}
    for offset,m in enumerate(['random','nn','rf_lcb']):
        subset=[r for r in rows if r['method']==m];x=[i+(offset-1)*.19 for i in range(5)];y=[r['confirmed_median_ms'] for r in subset]
        ax.errorbar(x,y,yerr=[[r['confirmed_median_ms']-min(r['confirmation_ms']) for r in subset],[max(r['confirmation_ms'])-r['confirmed_median_ms'] for r in subset]],fmt='o',capsize=3,color=colors[m],label=labels[m])
    ax.set_xticks(range(5),[11,23,37,53,71]);ax.set_xlabel('Seed (all from one software family)');ax.set_ylabel('Confirmed verified-loop time (ms)')
    ax.set_title('V71: selected configuration, median and range of three repeats');ax.legend(frameon=False);ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.01,'Budget: 10 shared prefix + 7 search + 3 confirmation. Ranges are not confidence intervals.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,1]);fig.savefig(out/'confirmed_incumbents.png',dpi=160);fig.savefig(out/'confirmed_incumbents.svg');plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','comparisons']},indent=2))

if __name__=='__main__':main()
