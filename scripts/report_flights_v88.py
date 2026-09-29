"""Post-collection descriptive plot and independent source-answer replay."""
import hashlib,json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.flights_v88 import reference,typed_rows,dimension,QUERIES
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RAW=ROOT/'results/v88_flights_feasibility';OUT=ROOT/'results/v88_flights_analysis';DATA=ROOT/'data/flights_v88'
def read(p):return json.loads(p.read_text())
def main():
    independent=reference(typed_rows(DATA/'flights.csv','flights'),dimension(typed_rows(DATA/'airlines.csv','airlines'),'carrier'),dimension(typed_rows(DATA/'airports.csv','airports'),'faa'),dimension(typed_rows(DATA/'planes.csv','planes'),'tailnum'))
    assert independent==read(DATA/'query_contract.json')['expected']
    summary=read(OUT/'summary.json');rows=read(RAW/'acquisitions.json');perquery=[]
    for row in rows:
        folder=RAW/f"trial_{row['trial']:02d}";answers=read(folder/'answers.json');plans=read(folder/'plans.json')
        for name in QUERIES:
            perquery.append({'trial':row['trial'],'config':row['configuration']['name'],'query':name,'scored_seconds':sum(a['seconds'] for a in answers if a['scored'] and a['query']==name),'plan_sha256':hashlib.sha256(json.dumps(plans[name],sort_keys=True).encode()).hexdigest()})
    (OUT/'source_replay_and_query_times.json').write_text(json.dumps({'source_answer_replay_passed':True,'source_rows':independent['input_flights'],'analysis':'Post-collection descriptive breakdown, not additional objective acquisitions','per_query':perquery},indent=2)+'\n')
    fig,(ax,bx)=plt.subplots(1,2,figsize=(10,4.5));labels=['1 thread','4 threads','1 thread\njoin order off']
    for i,r in enumerate(summary['results']):
        ax.scatter([i-.06,i,i+.06],r['seconds'],color='#245e87',s=40);ax.plot([i-.2,i+.2],[r['median_seconds']]*2,color='black',lw=2)
        bx.bar(i,100*r['range_over_median'],color='#c65b38' if not r['precision_screen_pass'] else '#245e87')
    for a in [ax,bx]:a.set_xticks(range(3),labels);a.spines[['top','right']].set_visible(False)
    ax.set_ylabel('Seconds for 16 three-query suites');ax.set_ylim(bottom=0);ax.set_title('Observed repeats; black line = median')
    bx.axhline(20,color='black',ls='--',lw=1);bx.set_ylabel('Range / median (%)');bx.set_title('Frozen coarse stability screen: ≤20%')
    fig.suptitle('DuckDB on real flight records: 9 classical feasibility trials')
    fig.text(.5,.02,'One exposed workload, three repeats per setting. No LLM, optimizer comparison or confidence interval.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.05,1,.93));fig.savefig(OUT/'feasibility.png',dpi=180);fig.savefig(OUT/'feasibility.pdf');plt.close(fig)
    print(json.dumps({'source_replay_passed':True,'query_timings':len(perquery),'median_four_thread_reduction':1-summary['results'][1]['median_seconds']/summary['results'][0]['median_seconds'],'max_sampled_rss_bytes':max(r['process']['sampled_maxima']['rss_bytes'] for r in rows)},indent=2))
if __name__=='__main__':main()
