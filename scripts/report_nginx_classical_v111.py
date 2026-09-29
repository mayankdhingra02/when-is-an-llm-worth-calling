"""Descriptive reports/figures from already validated classical receipts."""
import csv,json,os,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/native_nginx'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from verify_classical_nginx_v111 import verify

def main():
 fresh=verify();(ROOT/'artifacts/study_v111/verification.json').write_text(json.dumps(fresh,indent=2)+'\n')
 for stage in [109,111]:
  out=ROOT/f'results/v{stage}_classical';d=json.loads((ROOT/f'artifacts/study_v{stage}/verification.json').read_text());aout=ROOT/f'results/v{stage}_analysis';aout.mkdir(exist_ok=True)
  events=[json.loads(s) for s in (out/'completed.jsonl').read_text().splitlines()]
  rows=[]
  for e in events:
   m=e['result']['measurement'];clients=m.get('clients')
   ratio=max(x['measurement']['client_cpu_to_wall'] for x in clients) if clients else m['client_cpu_to_wall']
   rows.append(dict(id=e['id'],arm=e['arm'],phase=e['phase'],row_id=e['row_id'],status=e['result']['status'],seconds=m['workload_seconds'],aggregate_cpu_seconds=m['client_cpu_seconds'],max_individual_cpu_wall=ratio))
  with (aout/'timings.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  fig,axs=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
  colors={'sequential_3nn':'#0072B2','batch_3nn':'#D55E00','random':'#009E73'}
  for a,col in colors.items():
   vals=[r['seconds'] for r in rows if r['arm']==a and r['phase']=='confirmation'];x=list(colors).index(a)
   axs[0].scatter([x]*len(vals),vals,color=col);axs[0].plot([x-.2,x+.2],[statistics.median(vals) if vals else float('nan')]*2,color=col)
  axs[0].set(xticks=range(3),xticklabels=['Sequential\n3NN','Batch\n3NN','Random'],ylabel='Charged confirmation seconds',title='One seed; three repeats per arm')
  if not d['arms']:
   axs[0].clear();axs[0].axis('off');axs[0].text(.5,.5,'Confirmations not reached\n10 completed prefix attempts\n1 timed-out continuation\n29 unattempted slots',ha='center',va='center',transform=axs[0].transAxes);axs[0].set_title('Stopped stage: no arm comparison')
  good=[(i,r) for i,r in enumerate(rows) if r['status']=='valid'];bad=[(i,r) for i,r in enumerate(rows) if r['status']!='valid']
  axs[1].plot([i for i,r in good],[r['seconds'] for i,r in good],'.',color='#0072B2')
  if bad:axs[1].scatter([i for i,r in bad],[r['seconds'] for i,r in bad],marker='^',color='red',label='Timed out; unfinished workload')
  axs[1].axhline(2,color='red',ls='--',label='2 s screen');axs[1].set(xlabel='Acquisition order',ylabel='Batch seconds',title='All acquired outcomes');axs[1].legend()
  axs[2].plot(range(len(rows)),[r['max_individual_cpu_wall'] for r in rows],'.',color='#D55E00');axs[2].axhline(.8,color='red',ls='--',label='0.8 screen');axs[2].set(xlabel='Acquisition order',ylabel='Max individual client CPU/wall',title='Client headroom');axs[2].legend()
  fig.suptitle(f'V{stage}: NGINX development smoke; no LLM calls',fontsize=12)
  fig.savefig(aout/'classical.png',dpi=160,metadata={'Software':'matplotlib'});plt.close(fig)
  lines=[f'# V{stage} classical NGINX smoke','',f"{d['native_attempts']} real native attempts, {d['validated_responses']:,} byte-validated responses, zero model calls. One seed11 and one exposed system group. Planned40attempts: ten shared prefix plus three arms of7search/3confirmation,20logical evaluations each. A stopped stage does not imply completed arms.",'','|Continuation|Median confirmation seconds|Confirmation relative range|','|---|---|---|']
  for a,v in d['arms'].items():lines.append(f"|{a}|{v['confirmation_median_seconds']:.6f}|{v['confirmation_relative_range']:.2%}|")
  lines+=['',f"Diagnostics: `{json.dumps(d['timing_diagnostics'],sort_keys=True)}`."]
  if stage==111:lines += [f"Stage {d['status']}: {d['valid_attempts']}valid, {d['failed_attempts']}failed, {d['unattempted']}unattempted. No completed primary-arm medians when stopped.",f"Frozen expanded-domain screen: `{json.dumps(d['gates'],sort_keys=True)}`. All pass: **{d['all_gates_passed']}**."]
  else:lines += ['The single-process harness fails duration/client-headroom checks on this expanded domain; batch confirmation variation also exceeds10%. These results do not qualify an LLM comparison.']
  lines+=['','Verification reconstructed all recommendations using only branch-acquired labels, checked raw client/server receipts and hashes, and counted all confirmations. No new acquisition occurs during replay. Figures show each confirmation, not confidence intervals over independent systems.','', 'Timing includes the load driver and server on the same machine. The medians are diagnostic outcomes, not evidence for LLM gain or a deployable controller. One seed cannot quantify seed variability; one exposed group cannot establish generalization. Search minima and confirmation medians must not be conflated. Collection includes all three continuations; hypothetical single-policy deployment would use20native attempts plus controller cost, with no measured deployment saving established.','',f'![Saved measurements](../results/v{stage}_analysis/classical.png)']
  (ROOT/f'reports/nginx_classical_v{stage}.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(fresh))
if __name__=='__main__':main()
