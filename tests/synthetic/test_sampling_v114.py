"""Prepared-study invariants; no model requests or hidden outcome access."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_fixed_prefix_replicas():
 jobs=json.loads((ROOT/'artifacts/study_v114/jobs.json').read_text());old=[j for j in json.loads((ROOT/'artifacts/study_v103/jobs.json').read_text()) if j['mode']=='nonthinking']
 assert len(jobs)==len({j['key'] for j in jobs})==36
 assert {j['base_key'] for j in jobs}=={j['base_key'] for j in old}
 for original in old:
  replicas=[j for j in jobs if j['base_key']==original['base_key']]
  assert {j['sampling_seed'] for j in replicas}=={1009,2027,3041}
  assert all(j['seed']==j['sampling_seed'] and j['optimization_seed']==original['seed'] and j['prefix']==original['prefix'] for j in replicas)
 assert len({j['system_group'] for j in jobs})==6

def test_caps_and_paid_disabled():
 c=json.loads((ROOT/'configs/study_v114.json').read_text())
 assert c['new_generation_request_cap']==c['scientific_request_cap']==36
 assert c['max_allocated_output_tokens']==36*128 and c['max_new_recorded_objective_acquisitions']==36*10
 assert c['allow_paid_api'] is False and c['allow_cloud'] is False and c['max_external_spend_usd']==c['stage_download_cap_bytes']==c['retries']==c['compatibility_request_cap']==0
 assert c['max_generation_stage_seconds']==1800 and c['max_server_rss_bytes']==8*1024**3
