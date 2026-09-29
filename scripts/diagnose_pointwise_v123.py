"""Post-hoc score/tie attribution; descriptive only, no new target acquisition."""
from collections import Counter
from collect_smollm_v47 import ROOT,read,write

def main():
    cases=read(ROOT/'results/v123_analysis/summary.json')['cases'];rows=[]
    for r in cases:
        values=sorted(r['scores'].values());cutoff=values[9] if len(values)==20 else None
        below=None if cutoff is None else sum(v<cutoff for v in values);at=None if cutoff is None else sum(v==cutoff for v in values)
        ys=[y[0] for y in r['state']['labels'][:10]];lo,hi=min(ys),max(ys);span=hi-lo;calibration=[]
        for cid,y in zip(r['selected_ids'],r['state']['labels'][10:]):
            signed=None if span==0 else ((y[0]-lo)/span if r['direction']=='-' else (hi-y[0])/span)
            calibration.append({'candidate_id':cid,'prediction':r['scores'].get(cid),'acquired_target':y[0],'signed_prefix_scaled_loss':signed})
        rows.append({'selected_outcome_diagnostic':calibration,'key':r['key'],'system_group':r['system_group'],'histogram':dict(sorted(Counter(f'{v:.2f}' for v in values).items())),'floor_predictions':sum(v==0 for v in values),'ceiling_predictions':sum(v==1 for v in values),'cutoff':cutoff,'strictly_below_cutoff':below,'tied_at_cutoff':at,'selected_from_cutoff_tie':None if cutoff is None else 10-below,'selection_boundary_tied':cutoff is not None and values[9]==values[10],'matches_first10_set':r['matches_first10_set'],'selected_ids':r['selected_ids']})
    write(ROOT/'results/v123_analysis/attribution.json',{'scope':'Post-hoc descriptive diagnosis prompted by repeated zeros seen during generation; not a frozen confirmatory test or quality gate','cases':rows})
    lines=['# V123 post-hoc attribution: numeric predictions and fixed ties','','Repeated zero predictions were noticed during generation. This descriptive analysis was added after that observation. It changes no model inputs, selection rules, acquisitions or predeclared criteria. A tied cutoff uses the free fixed ID-order rule. We cannot infer how the model would rank tied configurations with a different prompt or output range.','','| Family | At floor0 /20 | Distinct values | Cutoff | Tied at cutoff | Selected from tie | Same set as first-ten |','|---|---:|---:|---:|---:|---:|---|']
    for r in rows:lines.append(f"| {r['system_group']} | {r['floor_predictions']} | {len(r['histogram'])} | {r['cutoff']} | {r['tied_at_cutoff']} | {r['selected_from_cutoff_tie']} | {r['matches_first10_set']} |")
    lines+=['','Selected-only outcome diagnostic (already charged labels):']
    for r in rows:
        measured=[x for x in r['selected_outcome_diagnostic'] if x['prediction']==0 and x['signed_prefix_scaled_loss'] is not None];better=sum(x['signed_prefix_scaled_loss']<0 for x in measured);worse=sum(x['signed_prefix_scaled_loss']>.05 for x in measured);lines.append(f"- {r['system_group']}: {len(measured)}selected floor predictions; {better}actually beat the prefix best, while{worse}were worse by more than0.05of the acquired prefix range.")
    lines+=['','This is conditioned on selected configurations and is not full-shortlist predictive accuracy. It uses only the10already charged continuation labels per family; no new objective probes.','','These counts describe the measured adapter. Floor saturation may reflect the clipping contract, greedy numeric decoding, acquired examples, or model behavior; this experiment does not identify which cause dominates. Loss-removal responsiveness can coexist with uninformative within-condition rankings. A diagnostic pass alone is insufficient: the frozen quality comparison and cheap controls remain decisive. Further range/prompt changes would be another development adaptation and need a new protocol, not a reinterpretation of this test.']
    (ROOT/'reports/pointwise_attribution_v123.md').write_text('\n'.join(lines)+'\n');print(rows)
if __name__=='__main__':main()
