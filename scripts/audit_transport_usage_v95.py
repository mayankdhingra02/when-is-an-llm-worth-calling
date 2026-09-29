"""Reproduce separately observable server usage for the sole lost response."""
import json,re
from collect_smollm_v47 import ROOT,read,write,sha

def main():
    model=ROOT/'results/v95b_reasoning';log=model/'server.log'
    starts=[json.loads(r) for r in (model/'generation_starts.jsonl').read_text().splitlines()]
    responses=[json.loads(r) for r in (model/'responses.jsonl').read_text().splitlines()]
    missing=[r for r in starts if r['identity'] not in {s['key'] for s in responses}]
    assert len(missing)==1 and missing[0]==starts[-1]
    lines=[l for l in log.read_text().splitlines() if 'slot print_timing' in l and ('prompt eval time' in l or '|        eval time' in l)]
    last=lines[-2:];assert len(last)==2
    assert len({re.search(r'task (\d+)',l).group(1) for l in last})==1
    counts=[int(re.search(r'/\s*(\d+) tokens',l).group(1)) for l in last]
    p=read(model/'preflight'/f"{missing[0]['identity']}.json")
    assert counts[0]==len(p['prompt_tokens']) and counts[1]<=missing[0]['payload']['n_predict']
    known=sum(r['response']['tokens_predicted'] for r in responses)
    write(ROOT/'results/v95_analysis/transport_timeout_usage.json',{
        'scope':'server-side usage for sole final unreturned request; no reconstructed output',
        'key':missing[0]['identity'],'source':str(log.relative_to(ROOT)),'source_sha256':sha(log),'exact_source_lines':last,
        'server_reported_prefill_tokens':counts[0],'server_reported_generated_tokens':counts[1],
        'returned_generated_tokens':known,'total_observable_generated_tokens':known+counts[1],
        'raw_response_and_final_answer':'unavailable; timeout charged and fallback retained',
        'attribution':'single serialized slot, exactly one unreturned request, last request matches final server task before shutdown'})
    print('Observable generated tokens including unreturned request:',known+counts[1])
if __name__=='__main__':main()
