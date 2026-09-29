"""Distinguish observable response totals from unknown timed-out request usage."""
import json
from collect_smollm_v47 import ROOT,read,write

def main():
    raw=ROOT/'results/v98_reasoning';out=ROOT/'results/v98_analysis'
    starts=[json.loads(x) for x in (raw/'generation_starts.jsonl').read_text().splitlines()]
    responses=[json.loads(x) for x in (raw/'responses.jsonl').read_text().splitlines()]
    received={r['key']:r for r in responses};phases={}
    for phase in ['thought','final']:
        requests=[r for r in starts if r['identity'].endswith('_'+phase)]
        records=[received[r['identity']]['response'] for r in requests if r['identity'] in received]
        missing=[r['identity'] for r in requests if r['identity'] not in received]
        phases[phase]={'charged_requests':len(requests),'returned_responses':len(records),
            'missing_response_ids':missing,
            'returned_generated_tokens':sum(r['tokens_predicted'] for r in records),
            'returned_actual_prefill_tokens':sum(r['timings']['prompt_n'] for r in records),
            'total_generated_tokens':None if missing else sum(r['tokens_predicted'] for r in records),
            'total_actual_prefill_tokens':None if missing else sum(r['timings']['prompt_n'] for r in records)}
    write(out/'usage_completeness.json',{'scope':'authoritative missing-usage qualification for phase_costs.json',
        'phases':phases,'note':'phase_costs.json contains sums over returned responses only; empty sums are not zero cost for a timed-out request',
        'server_log':'incomplete prompt progress and cancellation; no final timing/output record for timed-out task',
        'inference_claim':'No thinking final phase ran; the intended reasoning comparison remains untested'})
    print(json.dumps(phases,indent=2))

if __name__=='__main__':main()
