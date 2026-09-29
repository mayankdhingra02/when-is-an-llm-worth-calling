"""Rebind existing V42 hindsight ceilings to the current development designs.

No new inference, source-target parsing, acquisitions or controller inputs.
This rediscovers a prior recorded limitation; it is not a new theorem/result.
"""
from fractions import Fraction
import json
from collect_smollm_v47 import ROOT,read,write,sha

def gain(reference,target,direction='-'):
    reference,target=Fraction(reference),Fraction(target)
    if reference<=0 or target<=0 or direction not in ['-','+']:raise ValueError('Positive targets and known direction required')
    return (reference-target)/reference if direction=='-' else (target-reference)/reference

def attainable(ceiling,references,margin):
    return all(gain(v,ceiling)>=Fraction(margin) for v in references.values())

def main():
    old=read(ROOT/'results/v42_selection_reference/summary.json');jobs=read(ROOT/'artifacts/study_v124/cases.json');out=ROOT/'results/v125_design_audit';out.mkdir(exist_ok=True);rows=[]
    for j in jobs:
        p=read(ROOT/j['prefix']);c=next(c for c in old['cases'] if c['dataset']==j['dataset'] and c['seed']==j['seed']);assert c['candidate_ids']==p['pool']['ranked'] and set(c['candidate_ids'])==set(p['pool']['mapping'].values());assert Fraction(c['prefix_best'])==Fraction(str(min(y[0] for y in p['state']['labels'])))
        ceiling=min([Fraction(c['prefix_best'])]+[Fraction(y) for y in c['acquired_candidate_targets']]);assert ceiling==Fraction(c['shortlist_ceiling'])
        arm=read(ROOT/f"results/v124_analysis/arms/{j['key']}_ei.json");refs={m:Fraction(str(v)) for m,v in arm['references'].items()};bound={m:gain(v,ceiling) for m,v in refs.items()};primary={m:refs[m] for m in ['batch_3nn','full_sequential_3nn','presentation_first10']}
        for v in old['ceiling_comparisons']:
            if v['dataset']==j['dataset'] and v['seed']==j['seed']:assert bound[v['reference']]==Fraction(v['exact_ceiling_gain'])
        rows.append({'key':j['key'],'system_group':j['system_group'],'prefix_sha256':sha(ROOT/j['prefix']),'hindsight_ceiling_exact':str(ceiling),'max_relative_gains':{m:float(v) for m,v in bound.items()},'max_relative_gains_exact':{m:str(v) for m,v in bound.items()},'joint_5pct_attainable':attainable(ceiling,primary,'0.05'),'v124_ei_attains_ceiling':Fraction(str(arm['target']))==ceiling})
    batch=[r for r in old['ceiling_comparisons'] if r['reference']=='batch_3nn'];assert len(batch)==30
    all_possible=sum(Fraction(r['exact_ceiling_gain'])>=Fraction('0.05') for r in batch);inputs=['results/v42_selection_reference/summary.json','reports/protocol_v42_selection_reference.freeze.json','reports/selection_reference_v42.md','reports/protocol_v123.md','reports/protocol_v124.md','artifacts/study_v124/cases.json']+[j['prefix'] for j in jobs]+[f"results/v124_analysis/arms/{j['key']}_ei.json" for j in jobs]
    result={'scope':'Post-hoc revalidation of existing outcome-informed V42 bounds; not deployable, not a new discovery, not case selection','current_cases':rows,'current_joint_5pct_attainable_cases':sum(r['joint_5pct_attainable'] for r in rows),'historical_30cases_batch_5pct_attainable_cases':all_possible,'historical_max_gain_against_batch':float(max(Fraction(r['exact_ceiling_gain']) for r in batch)),'new_model_requests':0,'new_objective_acquisitions':0,'historical_labels_retained_cost':'V41covered all20candidates per case through charged branches; no new source targets read here','inputs_sha256':{n:sha(ROOT/n) for n in inputs}}
    write(out/'attainability.json',result);write(ROOT/'artifacts/study_v125/attainability_verification.json',{'verified':True,'current_prefix_pool_matches':3,'exact_bound_checks':6,'new_model_requests':0,'new_objective_acquisitions':0})
    lines=['# Attainability correction: V123/V124 quality screens had no possible passing case','','**The joint5%criterion was unattainable on all three selected fixed shortlists, regardless of the model.** V42had already computed these exact bounds from previously charged V41outcomes. This audit rebinds that existing result to the current prefixes/pools; it is not a new scientific discovery. I should have checked this prior evidence before using these cases for another optimization-quality screen.','','| Family | Maximum gain vs batch3NN | Maximum vs full sequential3NN | Maximum vs first-ten | Joint5%possible |','|---|---:|---:|---:|---|']
    for r in rows:
        b=r['max_relative_gains'];lines.append(f"| {r['system_group']} | {100*b['batch_3nn']:.3f}% | {100*b['full_sequential_3nn']:.3f}% | {100*b['presentation_first10']:.3f}% | {r['joint_5pct_attainable']} |")
    lines+=['',f"Across all30original V42prefixes, {all_possible}/30can improve5%over batch3NN within the frozen pool. Thus this is not fixed by choosing another seed from that same cohort. The maximum individual batch-relative ceiling is{100*result['historical_max_gain_against_batch']:.3f}%. These are outcome-informed hindsight ceilings, never controller features or achieved policies.",'','V123/V124raw responses, objective budgets, strict failures, paired outcomes and costs remain valid records. Their failure to meet this particular quality screen is not evidence against a capable unrestricted LLM optimizer: even perfect selection cannot pass. Dune/HSMGP full-domain sequential3NN beats the best possible fixed-pool result by enough that the latter has-45.630%relative gain. This search-space disadvantage must accompany the-16.264%V124mean comparison. The positive V125format result changes only parsing feasibility, not this bound.','','The original V42report and V43/V44pool experiments already identified this direction. V43tested uniform20and retained10+diverse10on all30prefixes; V44tested1.5Bselection on changed pools. Do not rediscover these as new methods. A future experiment must change the intervention/search region or ask a different scientific question, and first check development feasibility without selecting favorable held-out cases. A larger model or better formatting confined to these same pools cannot remove the bound.','','This audit reads existing charged-outcome summaries and checks exact rational gains and prefix/pool identities. It acquires no hidden source values and makes no model call. Development feasibility checks may motivate redesign; hindsight ceilings must not filter untouched test families after their outcomes are known. No threshold was lowered retrospectively, no old primary changed, and no Q2-readiness claim follows.']
    (ROOT/'reports/attainability_v125.md').write_text('\n'.join(lines)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
