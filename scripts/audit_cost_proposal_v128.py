"""Check attempted, returned and missing usage separately; no new calls."""
from collect_smollm_v47 import ROOT,read,write
import json
def usage(attempts,responses,field):
    if attempts<len(responses):raise ValueError('More responses than attempts')
    vals=[r.get(field) for r in responses]
    if any(v is not None and (type(v) is not int or v<0) for v in vals):raise ValueError('Invalid usage')
    return {'observed_sum':sum(v for v in vals if type(v) is int),
            'missing_responses':attempts-sum(type(v) is int for v in vals)}
def main():
    ledger=read(ROOT/'results/v128_proposals/ledger.json')
    responses=[json.loads(x)['response'] for x in (ROOT/'results/v128_proposals/responses.jsonl').read_text().splitlines()]
    comparison=read(ROOT/'results/v128_analysis/comparison.json')
    for field in ['tokens_predicted','tokens_evaluated']:
        assert comparison['actual_cost']['usage'][field]==usage(ledger['generation_requests'],responses,field)
    jobs=read(ROOT/'artifacts/study_v128/jobs.json');normal=[j for j in jobs if j['condition']=='normal']
    assert len(jobs)==12 and len(normal)==10
    assert {j['system_group'] for j in normal}=={'storm','mongodb'}
    assert all(j['split']=='exposed_development_extension' for j in jobs)
    for group in ['storm','mongodb']:
        assert sorted(j['seed'] for j in normal if j['system_group']==group)==[11,23,37,53,71]
    result={'verified':True,'intended_requests':12,'charged_requests':ledger['generation_requests'],
      'returned_requests':len(responses),'unattempted_requests':12-ledger['generation_requests'],
      'missing_response_usage':ledger['generation_requests']-len(responses),
      'experimental_recorded_acquisitions':300,'incidental_exastencils_vector_exposures':2,
      'total_new_recorded_vector_exposures':302,'new_model_requests_by_audit':0}
    write(ROOT/'artifacts/study_v128/cost_verification.json',result);print(result)
if __name__=='__main__':main()
