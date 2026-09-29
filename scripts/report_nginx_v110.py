"""Replay multiprocess receipts and frozen gates; never collect objectives."""
import json,statistics,sys
from pathlib import Path
from native_nginx_v105 import sha
ROOT=Path(__file__).resolve().parents[1]
def verify(root=ROOT):
 for n,h in json.loads((root/'reports/protocol_v110.freeze.json').read_text())['sha256'].items():assert sha(root/n)==h,n
 cfg=json.loads((root/'configs/nginx_feasibility_v110.json').read_text());domain=json.loads((root/'configs/nginx_domain_v108.json').read_text())['rows'];out=root/'results/v110_nginx';summary=json.loads((out/'summary.json').read_text())
 starts=[json.loads(s) for s in (out/'starts.jsonl').read_text().splitlines()];cases=summary['cases'];assert len(cases)==6 and len(starts)==summary['charged_native_configuration_attempts']<=6
 rows=[]
 for i,c in enumerate(cases):
  assert c['index']==i and c['row_id']==cfg['cases'][i]
  if c['status']=='unattempted':continue
  assert starts[i]==dict(index=i,row_id=c['row_id'],charged_native_configuration_attempt=True)
  folder=out/f'{i:02d}';raw=json.loads((folder/'result.json').read_text());assert dict(index=i,row_id=c['row_id'],**raw)==c
  assert c['configuration']==domain[c['row_id']]
  assert sha(folder/'nginx.conf')==c['config_sha256'] and sha(folder/'www/payload.bin')==c['payload_sha256']
  if c['status']!='valid':continue
  m=c['measurement'];assert c['owned_process_group_absent'] and c['server_returncode']==0 and m['valid']
  receipts=json.loads((folder/'clients.json').read_text());assert m['clients']==receipts['clients'] and m['workload_seconds']==receipts['workload_seconds']
  assert len(m['clients'])==4;cpu=0;ratios=[]
  for j,child in enumerate(m['clients']):
   a=child['measurement'];assert child['index']==j and child['returncode']==0 and child['owned_process_group_absent']
   assert a==json.loads((folder/f'client_{j}.stdout').read_text())
   assert a['valid'] and a['requests_sent']==a['responses_byte_valid']==262144 and a['per_connection_valid']==[65536]*4
   assert abs(a['client_cpu_to_wall']-a['client_cpu_seconds']/a['workload_seconds'])<1e-7
   assert 0<=child['launch_offset_seconds']<m['workload_seconds']
   cpu+=a['client_cpu_seconds'];ratios.append(a['client_cpu_to_wall'])
  assert abs(m['client_cpu_seconds']-cpu)<1e-8 and abs(m['client_cpu_to_wall']-cpu/m['workload_seconds'])<1e-8
  assert m['requests_sent']==m['responses_byte_valid']==1048576
  rows.append(dict(index=i,row_id=c['row_id'],seconds=m['workload_seconds'],cpu_seconds=cpu,aggregate_cpu_ratio=m['client_cpu_to_wall'],max_individual_cpu_ratio=max(ratios),max_launch_offset=max(x['launch_offset_seconds'] for x in m['clients'])))
 ref=[r['seconds'] for r in rows if r['row_id']==cfg['reference_row']]
 rr=(max(ref)-min(ref))/statistics.mean(ref) if len(ref)==4 else None
 gates=dict(correctness=len(rows)==6,min_duration=len(rows)==6 and all(r['seconds']>=2 for r in rows),reference_repeatability=rr is not None and rr<=.1,individual_client_headroom=len(rows)==6 and all(r['max_individual_cpu_ratio']<=.8 for r in rows))
 return dict(verified=True,rows=rows,gates=gates,all_gates_passed=all(gates.values()),reference_relative_range=rr,native_attempts=len(starts),valid_responses=sum(c.get('measurement',{}).get('responses_byte_valid',0) for c in cases),lifecycle_seconds=summary['lifecycle_seconds'],new_model_requests=0,new_objectives_on_replay=0)
def main():
 d=verify();out=ROOT/'results/v110_analysis';out.mkdir(exist_ok=True);(out/'verification.json').write_text(json.dumps(d,indent=2)+'\n')
 lines=['# V110 multiprocess native feasibility','',f"Actual collection: {d['native_attempts']} native attempts, {d['valid_responses']:,} byte-valid responses; zero LLM calls. Lifecycle {d['lifecycle_seconds']:.3f}s.",'',f"Frozen gates: {d['gates']}. All passed: **{d['all_gates_passed']}**. Reference relative range: {d['reference_relative_range']:.2%}.",'','|Attempt|Row|Wall seconds|Client CPU seconds|Max individual CPU/wall|Aggregate CPU/wall|','|---|---|---|---|---|---|']
 for r in d['rows']:lines.append(f"|{r['index']}|{r['row_id']}|{r['seconds']:.3f}|{r['cpu_seconds']:.3f}|{r['max_individual_cpu_ratio']:.3f}|{r['aggregate_cpu_ratio']:.3f}|")
 lines+=['','All responses were checked byte-for-byte. Aggregate CPU/wall covers four cores and is not compared with the single-core ceiling. Parent wall includes process launch/wait overhead; launch offsets are preserved. Source/binary/config hashes and cleanup receipts were replayed.','', 'Exploratory engineering on one exposed NGINX development group. Stress case selected from V109 outcomes. This is neither an independent optimization result nor evidence for a learned router or a journal tier. Passing these screens would not prove freedom from host contention or qualify every configuration. Failed screens block dependent LLM comparison. No deployment-cost savings are estimated from this harness screen.']
 (ROOT/'reports/nginx_v110.md').write_text('\n'.join(lines)+'\n');print(json.dumps(d))
if __name__=='__main__':main()
