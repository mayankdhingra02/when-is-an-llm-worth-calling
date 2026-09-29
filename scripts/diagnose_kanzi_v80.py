"""Explicit post-hoc descriptive checks of observed proposal patterns only."""
import collections,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid
from escalation.kanzi_v79 import PRESET_IDS

def read(p):return json.loads(p.read_text())
def main():
    data=read(ROOT/'results/v80_kanzi_analysis/summary.json');raw=ROOT/'results/v80_kanzi_paired';configs=grid()
    byworkload={};allrows=[]
    for w in data['mean_seed_median_bytes_by_workload']:
        proposals=[];incumbents=[];prefix_kept=[]
        for c in data['cases']:
            if c['workload']!=w:continue
            seed=c['seed'];inc=c['arms']['llm']['config_id'];incumbents.append(inc)
            prefix_kept.append(not c['arms']['llm']['incumbent_from_real_model_proposal'])
            for step in range(1,8):
                folder=raw/f'v80_{w}_seed{seed}_step{step}'
                if not (folder/'request.json').exists():continue
                req=read(folder/'request.json');dec=read(folder/'decision.json')
                if not dec['valid']:continue
                cid=dec['selected_id'];eligible=req['eligible_ids'];assert cid in eligible
                row={'workload':w,'seed':seed,'step':step,'config_id':cid,'within_preset_candidate_family':cid in PRESET_IDS,'lowest_eligible_id':cid==min(eligible),'highest_eligible_id':cid==max(eligible)}
                allrows.append(row);proposals.append(cid)
        byworkload[w]={'valid_proposals':len(proposals),'unique_proposals':len(set(proposals)),'proposal_frequencies':dict(collections.Counter(proposals)),'incumbent_ids_in_seed_order':incumbents,'distinct_incumbents':len(set(incumbents)),'incumbents_with_preset_transform_entropy':sum(i in PRESET_IDS for i in incumbents),'prefix_incumbents_retained':sum(prefix_kept)}
    out=ROOT/'results/v80_proposal_diagnostic';out.mkdir(exist_ok=True)
    result={'label':'post-hoc descriptive pattern audit; no causal mechanism, counterfactual outcome or fitted policy','workloads':byworkload,'valid_observed_proposals':len(allrows),'within_preset_candidate_family':sum(r['within_preset_candidate_family'] for r in allrows),'lowest_eligible_id_matches':sum(r['lowest_eligible_id'] for r in allrows),'highest_eligible_id_matches':sum(r['highest_eligible_id'] for r in allrows),'incumbent_configurations':{str(i):configs[i] for i in sorted({i for w in byworkload.values() for i in w['incumbent_ids_in_seed_order']})},'new_model_calls':0,'new_physical_trials':0}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');(out/'observed_proposals.json').write_text(json.dumps(allrows,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
