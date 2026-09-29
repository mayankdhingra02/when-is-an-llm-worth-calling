"""Saved-evidence native-client audit and descriptive report; no acquisitions."""
import argparse,csv,hashlib,json,math,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/native_nginx/mpl'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache/native_nginx'))

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def verify(stage):
 out=ROOT/f'results/v{stage}_nginx';d=json.loads((out/'summary.json').read_text())
 freeze=json.loads((ROOT/f'reports/protocol_v{stage}.freeze.json').read_text())
 count=freeze.get('requests_per_connection',65536)
 d['requests_per_connection']=count
 for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
 rows=d['cases'];assert len(rows)==6
 cases=['reference','contrast','reference','reference','contrast','reference']
 attempts=[json.loads(s) for s in (out/'attempts.jsonl').read_text().splitlines()]
 assert len(attempts)==d['charged_native_configuration_attempts']<=6
 failed=False
 for i,r in enumerate(rows):
  assert r['index']==i and r['case']==cases[i]
  if r['status']=='unattempted':assert failed;continue
  assert not failed
  assert attempts[i]=={'index':i,'case':r['case'],'charged_native_configuration_attempt':True}
  folder=out/f'{i:02d}_{r["case"]}'
  assert json.loads((folder/'result.json').read_text())==r
  assert sha(folder/'nginx.conf')==r['config_sha256']
  assert sha(folder/'www/payload.bin')==r['payload_sha256']
  if 'measurement' in r:
   m=r['measurement'];assert json.loads((folder/'client.stdout').read_text())==m
   assert m['responses_byte_valid']==sum(m['per_connection_valid'])
   assert m['responses_byte_valid']<=m['requests_sent']<=16*count
   assert math.isclose(m['client_cpu_to_wall'],m['client_cpu_seconds']/m['workload_seconds'],abs_tol=1e-7)
  if r['status']=='valid':
   assert r['client_returncode']==r['server_returncode']==0 and r['owned_process_group_absent']
   assert m['valid'] and m['per_connection_valid']==[count]*16
  else:failed=True
 return d

def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',type=int,default=106);a=p.parse_args();d=verify(a.stage)
 dest=ROOT/f'results/v{a.stage}_analysis';dest.mkdir(exist_ok=True)
 valid=[r for r in d['cases'] if r['status']=='valid'];refs=[r['measurement']['workload_seconds'] for r in valid if r['case']=='reference']
 spread=(max(refs)-min(refs))/statistics.mean(refs) if len(refs)==4 else None
 gates={'all_six_valid':len(valid)==6,'duration_at_least_two_seconds':len(valid)==6 and all(r['measurement']['workload_seconds']>=2 for r in valid),
        'reference_relative_range_at_most_10_percent':spread is not None and spread<=.1,
        'client_cpu_wall_at_most_0_8':len(valid)==6 and all(r['measurement']['client_cpu_to_wall']<=.8 for r in valid)}
 result={'gates':gates,'all_gates_pass':all(gates.values()),'reference_relative_range':spread,'native_configuration_attempts':d['charged_native_configuration_attempts'],
         'validated_responses':sum(r.get('measurement',{}).get('responses_byte_valid',0) for r in d['cases']),
         'requests_sent':sum(r.get('measurement',{}).get('requests_sent',0) for r in d['cases']),'new_model_requests':0,'lifecycle_seconds':d['lifecycle_seconds']}
 (dest/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 with (dest/'timings.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['index','case','status','seconds','client_cpu_wall','responses_byte_valid'])
  for r in d['cases']:
   m=r.get('measurement',{});w.writerow([r['index'],r['case'],r['status'],m.get('workload_seconds'),m.get('client_cpu_to_wall'),m.get('responses_byte_valid')])
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,ax=plt.subplots(1,2,figsize=(9,3.5))
 for name,color in [('reference','#2563eb'),('contrast','#d97706')]:
  selected=[r for r in valid if r['case']==name];x=[r['index']+1 for r in selected]
  for j,key in enumerate(['workload_seconds','client_cpu_to_wall']):ax[j].scatter(x,[r['measurement'][key] for r in selected],label=name,color=color)
 ax[0].axhline(2,color='red',ls='--',label='minimum 2s');ax[1].axhline(.8,color='red',ls='--',label='maximum 0.8')
 for axes in ax:axes.set_xlabel('Fixed attempt order');axes.legend()
 ax[0].set_ylabel('Workload seconds');ax[1].set_ylabel('Client CPU / wall')
 fig.suptitle(f'V{a.stage}: native-client feasibility; gates '+('passed' if result['all_gates_pass'] else 'failed'))
 fig.tight_layout();fig.savefig(dest/'feasibility.png',dpi=160);plt.close(fig)
 table='\n'.join(f"|{r['index']+1}|{r['case']}|{r['status']}|{r.get('measurement',{}).get('workload_seconds',float('nan')):.6f}|{r.get('measurement',{}).get('client_cpu_to_wall',float('nan')):.4f}|" for r in d['cases'])
 report=f'''# V{a.stage}: bounded native-client feasibility

**Frozen gates {'passed' if result['all_gates_pass'] else 'failed'}.** Six intended attempts; {result['native_configuration_attempts']} charged native configuration attempts; {result['validated_responses']:,} byte-valid responses. No LLM request or new recorded-table outcome. These are real local NGINX executions on an exposed development group; no optimization benefit, independent-group generalization or journal-readiness claim.

|Attempt|Bundle|Status|Workload seconds|Client CPU/wall|
|---|---|---|---:|---:|
{table}

Gate outcomes: `{json.dumps(gates)}`. Reference relative range: {spread}. This is a screening statistic, not a confidence interval. Native client elapsed includes connection setup and every response check; CPU includes user and system time. Local client/server share this host; CPU/wall alone does not identify every bottleneck. Two bundled settings are not a validated400-configuration tuning domain. All failures and unattempted conditions remain visible.

![Feasibility](../results/v{a.stage}_analysis/feasibility.png)

Collection lifecycle: {d['lifecycle_seconds']:.3f}s. Intended per-attempt fixed workload:16connections×{d['requests_per_connection']}requests×32768bodybytes. Body bytes flow over loopback, not the internet. Download0; paid/cloud spend0. No deployment-cost estimate. Client source/binary, NGINX binary, harness and protocol were hashed before outcomes. Synthetic protocol fixtures are excluded from this report. Owned processes were checked absent per attempt.

Raw logs: `results/v{a.stage}_nginx/`; verifier/CSV/figure: `results/v{a.stage}_analysis/`; freeze: `reports/protocol_v{a.stage}.freeze.json`. Replay `.venv/bin/python scripts/report_nginx_native_v106.py --stage {a.stage}` performs no workload/model call. Do not rerun the once-only collector into its old output directory. Gates must be met before any optimizer study, using a new prospective protocol for any harness revision.
'''
 (ROOT/f'reports/nginx_v{a.stage}.md').write_text(report);print(json.dumps(result))
if __name__=='__main__':main()
