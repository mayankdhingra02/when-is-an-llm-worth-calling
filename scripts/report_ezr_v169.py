"""Descriptive same-session validation analysis; no optimizer/model calls."""
import json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collect_smollm_v47 import ROOT,read,write,sha
A=ROOT/'artifacts/study_v169';O=ROOT/'results/v169_ezr'
MODELS=['smollm3_3b','qwen3_8b'];NEW=['ezr_upstream_centroid','ezr_upstream_bayes'];COMPARATORS=['sequential_3nn','adaptive_neighbor','gp_ei']+NEW
def lines(path):return [json.loads(s) for s in path.read_text().splitlines()]
def analyze(selections,acquisitions):
    arms=[]
    for s in selections:
        rows=[r for r in acquisitions if r['case']==s['case'] and r['arm']==s['arm'] and r['phase']=='validation']
        assert len(rows)==3 and all(r['row_id']==s['row_id'] for r in rows)
        ys=[r['value'] for r in rows];median=statistics.median(ys);mad=statistics.median(abs(y-median) for y in ys)/median
        arms.append({**s,'validation_values':ys,'median':median,'relative_mad':mad,'quality_valid':all(r['status']=='correct' for r in rows),'stable':mad<=.05,'above_floor':median>=.01})
    lookup={(r['case'],r['arm']):r for r in arms};cases=[]
    for case in sorted({r['case'] for r in arms}):
        for model in MODELS:
            m=lookup[case,model];gains={};robust={};same={}
            for control in COMPARATORS:
                c=lookup[case,control];gain=(c['median']-m['median'])/c['median'];gains[control]=gain;same[control]=c['row_id']==m['row_id']
                robust[control]=gain>.1 and not same[control] and all(x['quality_valid'] and x['stable'] and x['above_floor'] for x in [c,m])
            cases.append({'case':case,'engine':m['engine'],'model':model,'gains':gains,'same_configuration':same,'robust_practical_wins':robust,'joint_robust_win':all(robust.values())})
    return arms,cases
def main():
    completion=read(O/'completion.json');assert completion['status']=='completed' and completion['acquisitions']==410
    acq=[read(p) for p in sorted((O/'acquisitions').glob('*.json'))];assert len(acq)==410
    arms,cases=analyze(read(O/'selections.json'),acq);summary=[]
    for engine in ['polars','xgboost']:
        for arm in ['sequential_3nn','adaptive_neighbor','gp_ei','random_full','random_proposal']+NEW+MODELS:
            rs=[r for r in arms if r['engine']==engine and r['arm']==arm];summary.append({'engine':engine,'arm':arm,'mean_of_validation_medians_seconds':statistics.mean(r['median'] for r in rs),'quality_valid_cells':sum(r['quality_valid'] for r in rs),'unstable_cells':sum(not r['stable'] for r in rs)})
    cpu=sum(read(p)['source_result']['optimizer_process_cpu_seconds'] for p in (O/'search').glob('*.json'))
    result={'scope':'secondary same-host revalidation on exposed tasks; historical model/control selections fixed','arms':arms,'cases':cases,'system_arm_summary':summary,'collection':{**completion,'quality_penalties':sum(r['status']=='quality_penalty' for r in acq),'native_objective_seconds':sum(r['measurement']['objective_seconds'] for r in acq),'subprocess_seconds':sum(r['collection_seconds'] for r in acq),'source_optimizer_process_cpu_seconds':cpu,'historical_prefix_outcomes_reused':100,'new_source_B20_arms':20,'historical_selections_revalidated':70,'new_validation_outcomes':270,'historical_model_requests_reused':20,'new_model_requests':0}}
    write(O/'comparison.json',result)
    text=['# V169: source-executed EZR continuation controls','','Executed unchanged pinned EZR0.9.4 acquire/centroid/Naive Bayes code with an explicit saved-prefix wrapper. This is a checkpoint adaptation, not full from-scratch EZR or SNAP2 replication. Unknown objective slots were question marks; callbacks acquired one label at a time.','','20 new continuation arms used10historical prefix labels +7new native outcomes +3fresh validations each. All70historical V168 model/control selections were additionally revalidated in the same randomized blocks. Those210extra measurements are diagnostic research costs outside the original closed budgets.','','## Same-session validated outcomes','','| Application | Arm | Mean of five validation medians (seconds) | Quality-valid /5 | Unstable /5 |','|---|---|---:|---:|---:|']
    for row in summary:text.append(f"| {row['engine']} | {row['arm']} | {row['mean_of_validation_medians_seconds']:.6f} | {row['quality_valid_cells']} | {row['unstable_cells']} |")
    text+=['','Positive paired gain favors the historical model-selected configuration. Gains below are means of per-case ratios; they differ from ratios of mean runtimes.','','| Application | Model | vs sequential | vs adaptive | vs GP | vs EZR centroid | vs EZR Bayes | Joint robust wins /5 |','|---|---|---:|---:|---:|---:|---:|---:|']
    for engine in ['polars','xgboost']:
        for model in MODELS:
            rs=[r for r in cases if r['engine']==engine and r['model']==model];g=[f"{100*statistics.mean(r['gains'][c] for r in rs):+.3f}%" for c in COMPARATORS]
            text.append('| '+ ' | '.join([engine,model]+g+[str(sum(r['joint_robust_win'] for r in rs))])+' |')
    text+=['','Robust joint gain requires >10% over all five listed comparators, different configurations, all fresh quality-valid results, medians>=10ms and relativeMAD<=5%. No case is dropped for failing that diagnostic. Candidate-level outputs and every gain remain in comparison.json.','','## Cost and provenance','',f"410new acquired outcomes;820query/training executions;140new search outcomes and270fresh validation outcomes. Actual stage {completion['seconds']:.3f}s/1800s, native objective time {result['collection']['native_objective_seconds']:.3f}s, subprocess wall {result['collection']['subprocess_seconds']:.3f}s. Owner-optimizer/bridge process CPU {cpu:.6f}s excludes child native execution. Quality penalties: {result['collection']['quality_penalties']}. No new model request, download, retry, cloud use or payment. Original source/input/model collection remains a historical cost.",'','The source is pinned to bfda80b3b797d142378f7fb8746c3485610fb17e with MIT notice retained. Native workers remain the unchanged Polars/XGBoost versions. The existing Python3.13.3 interpreter supports owner syntax; its binary hash is frozen. Acquire itself is unchanged; warm-start order, ten cached labels, seven additional acquisitions, feature typing, single scalar loss and raw-loss incumbent selection are documented adaptations. Literal normalization, smoothing and cached-centroid behavior are preserved.','','## Limits','','New EZR search occurred later than the original classical/model search. Simultaneous randomized validation reduces final-scoring timing differences but cannot remove temporal effects on historical search selection. No LLM response was regenerated, synthesized or substituted; all model selections derive from the exact retained real responses and prefixes. This is an exploratory control extension after prior outcome exposure, not a new held-out model study. Two implementation groups, one host, repeated seeds and shared flight workload do not establish population generalization. Source execution narrows an implementation gap; full prior methods and independent-host replication remain untested.','','Evidence: artifacts/study_v169/{freeze.json,plan.json,runtime.json}; results/v169_ezr/{optimizer_inputs,optimizer_events,search,acquisitions,selections.json,validation_plan.json,comparison.json}. Prior V168 results remain unchanged.']
    (ROOT/'reports/ezr_v169.md').write_text('\n'.join(text)+'\n')
    plt.rcParams['svg.hashsalt']='v169';fig,axs=plt.subplots(1,2,figsize=(11,4));fig.subplots_adjust(bottom=.31,top=.79,wspace=.32)
    for ax,engine in zip(axs,['polars','xgboost']):
        for mi,model in enumerate(MODELS):
            rs=[r for r in cases if r['engine']==engine and r['model']==model];ys=[100*statistics.mean(r['gains'][c] for r in rs) for c in COMPARATORS]
            ax.plot(range(5),ys,marker='o',label=model)
        ax.set_xticks(range(5),['3NN','Adaptive','GP-EI','EZR\ncentroid','EZR\nBayes']);ax.axhline(0,color='gray',lw=.8);ax.axhline(10,color='gray',ls=':',lw=.8);ax.set_title(engine);ax.set_ylabel('Mean paired gain favoring model (%)');ax.grid(axis='y',alpha=.2)
    axs[1].legend(fontsize=8);fig.suptitle('Historical model selections vs source-executed EZR controls\nFresh randomized validation; five seeds per application',fontsize=11)
    fig.text(.5,.05,'Descriptive means on exposed tasks. Dotted line is a margin, not a confidence bound.',ha='center',fontsize=8)
    fig.savefig(O/'baseline_gains.png',dpi=160,metadata={'Software':'V169'});fig.savefig(O/'baseline_gains.svg',metadata={'Date':None});plt.close(fig)
    print(json.dumps({'collection':result['collection'],'joint_robust_wins':sum(c['joint_robust_win'] for c in cases)}))
if __name__=='__main__':main()
