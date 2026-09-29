"""Post-collection cross-check of compatibility, traces, limits and costs."""
import json,hashlib,math
from pathlib import Path
from collect_smollm_v47 import sha
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def main():
    cfg=read('configs/resource_proposal_v91.json');approval=read('artifacts/study_v91/approval.json');assert approval['proposal_sha256']==sha(ROOT/'configs/resource_proposal_v91.json') and approval['explicit_resource_change_approved'] is True
    d=read('artifacts/study_v91/downloads.json');assert sum(x['bytes'] for x in d['transfers'])==d['bytes']<=cfg['stage_download_cap_bytes'];assert d['model_bytes']==cfg['model_file_bytes']
    manifest=read('artifacts/study_v91/model_manifest.json');assert sha(ROOT/manifest['path'])==manifest['sha256']==cfg['model_sha256'];assert (ROOT/manifest['path']).stat().st_size==cfg['model_file_bytes']
    for e in d['transfers']:
        if e['status']=='complete':assert sha(ROOT/e['path'])==e['sha256'] and (ROOT/e['path']).stat().st_size==e['bytes']
        else:assert e['bytes']==0 and e['status']=='failed'
    ledger=read('results/v91_qwen/ledger.json');assert ledger['generation_requests']==303 and ledger['scientific_requests']==300 and ledger['compatibility_requests']==3 and ledger['completed_cases']==30 and ledger['server_exit_code']==0 and ledger['resource_stop_reason'] is None
    assert ledger['stage_seconds']<=1800 and ledger['peak_server_rss_bytes']<=8*1024**3 and ledger['retries']==ledger['external_spend_usd']==0
    starts=[json.loads(x) for x in (ROOT/'results/v91_qwen/generation_starts.jsonl').read_text().splitlines()];assert len(starts)==303 and [x['generation'] for x in starts]==list(range(1,304)) and len({x['identity'] for x in starts})==303
    assert [x['kind'] for x in starts]==['compatibility']*3+['scientific']*300
    responses=[json.loads(x) for x in (ROOT/'results/v91_qwen/responses.jsonl').read_text().splitlines()];byid={x['request_id']:x for x in responses}
    for entry in starts[3:]:assert byid[entry['identity']]['payload']==entry['payload']
    compat=[]
    for i,letter in enumerate('ABC'):
        p=read(f'results/v91_qwen/compatibility/probe_{i}.json');assert p['payload']==starts[i]['payload'];r=p['response'];assert r['content']==letter and r['tokens_predicted']==1 and r['truncated'] is False;compat.append(p)
    runtime=read('results/v91_qwen/runtime.json')['command'];assert runtime[runtime.index('--host')+1]=='127.0.0.1' and runtime[runtime.index('--port')+1]=='18591' and '--offline' in runtime and '--no-warmup' in runtime
    for x in responses+[{'response':x['response']} for x in compat]:
        r=x['response'];assert r['tokens_predicted']==1 and r['truncated'] is False
    record={'verified':True,'scientific_requests':300,'compatibility_requests':3,'all_generation_requests':303,'all_http_requests_including_metadata':ledger['http_requests'],'all_generated_tokens':sum(x['response']['tokens_predicted'] for x in responses)+sum(x['response']['tokens_predicted'] for x in compat),'model_download_bytes':d['model_bytes'],'stage_download_bytes_including_metadata':d['bytes'],'cumulative_download_bytes':cfg['previous_total_download_bytes']+d['bytes'],'remaining_total_download_bytes':cfg['proposed_total_download_cap_bytes']-cfg['previous_total_download_bytes']-d['bytes'],'cumulative_model_download_bytes':cfg['previous_model_download_bytes']+d['model_bytes'],'remaining_model_download_bytes':cfg['proposed_model_download_cap_bytes']-cfg['previous_model_download_bytes']-d['model_bytes'],'inference_lifecycle_seconds':ledger['stage_seconds'],'peak_sampled_server_rss_bytes':ledger['peak_server_rss_bytes'],'gpu_scope':'GPU offload requested; default server log does not enumerate actual device/offloaded layers, so exact residency is unverified','external_spend_usd':0,'electricity_hardware_cost':'unknown'}
    (ROOT/'artifacts/study_v91/runtime_cost_audit.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
if __name__=='__main__':main()
