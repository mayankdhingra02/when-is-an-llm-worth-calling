"""Independent validation and deterministic feasibility reporting; never solves."""
import json,hashlib,statistics,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v157';O=ROOT/'results/v157_solvers'
def read(p):return json.loads(p.read_text())
def verified(rows,jobs):
 assert len(rows)==len(jobs)==40
 cells={}
 for k,(r,j) in enumerate(zip(rows,jobs),1):
  assert r['charge']==k and r['job']==j
  v=r['result']
  if v:
   assert v['engine']==j['engine'] and v['n']==j['n'] and v['config']==j['config'] and v['limit']==j['limit']
   qs=v['rows'];ok=len(qs)==j['n'] and all(type(q) is int and 0<=q<j['n'] for q in qs)
   if ok:ok=all(qs[i]!=qs[t] and abs(qs[i]-qs[t])!=abs(i-t) for i in range(j['n']) for t in range(i))
   assert ok==v['correct']
   if ok:assert v['status'] in ['sat','OPTIMAL','FEASIBLE']
   assert math.isfinite(v['solve_seconds']) and v['solve_seconds']>0
   assert v==json.loads(r['stdout'])
  cells.setdefault((j['engine'],j['candidate_id']),[]).append(r)
 out={}
 for (e,c),rs in sorted(cells.items()):
  vals=[r['result']['solve_seconds'] for r in rs if r['result'] and r['result']['correct']]
  median=statistics.median(vals) if vals else None;mad=statistics.median([abs(t-median) for t in vals])/median if vals else None
  out.setdefault(e,{'cells':[]})['cells'].append({'candidate_id':c,'charged':len(rs),'correct':len(vals),'median_solve_seconds':median,'relative_mad':mad,'pass':len(vals)==5 and median>=.01 and mad<=.05})
 for s in out.values():s['admitted']=all(c['pass'] for c in s['cells'])
 return out

def main():
 for n,h in read(A/'freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
 jobs=read(A/'jobs.json');rows=[read(O/f'{i:03d}.json') for i in range(1,41)];summary=verified(rows,jobs);assert summary==read(O/'summary.json')
 intents=[json.loads(x) for x in (O/'intents.jsonl').read_text().splitlines()];assert [x['job'] for x in intents]==jobs and [x['charge'] for x in intents]==list(range(1,41));done=read(O/'completion.json');assert done['charged']==40 and done['unattempted']==0 and done['seconds']<=600
 fig,axes=plt.subplots(1,2,figsize=(9,3.5));fig.subplots_adjust(bottom=.2,wspace=.25,top=.8)
 for ax,(e,s) in zip(axes,summary.items()):
  for idx,c in enumerate(s['cells']):
   rs=[r for r in rows if r['job']['engine']==e and r['job']['candidate_id']==c['candidate_id']]
   for k,r in enumerate(rs):
    v=r['result'];y=v['solve_seconds'] if v else 15;ok=v is not None and v['correct'];ax.scatter(idx+(k-2)*.05,y,marker='o' if ok else 'x',color='#146b8a' if ok else '#b24739',s=28)
  ax.set_xticks(range(4),[str(c['candidate_id']) for c in s['cells']]);ax.set_xlabel('Predeclared configuration index');ax.set_title(e+(' — admitted' if s['admitted'] else ' — not admitted'));ax.set_yscale('log');ax.set_ylim(1,20) if e=='cvc5' else None;ax.grid(axis='y',alpha=.2);ax.set_ylabel('Native solve seconds (log scale)')
 fig.suptitle('N=32 N-queens: 40 actual feasibility probes\nCircles: valid solutions; crosses: failures/timeouts',fontsize=11)
 plt.rcParams['svg.hashsalt']='v157';fig.savefig(O/'feasibility.png',dpi=160,metadata={'Software':'V157'});fig.savefig(O/'feasibility.svg',metadata={'Date':None});plt.close(fig)
 lines=['# V157: two new solver engines, native feasibility result','',f"Executed40/40 charged probes in{done['seconds']:.3f}s, no LLM calls. Fixed N=32, four settings/engine, five repeats. Every returned assignment is independently checked by an O(N²) pairwise validator. No objective value was inferred or mocked.",'','| Engine / candidate | Correct / intended | Median valid solve (s) | Relative MAD | Admission cell |','|---|---:|---:|---:|---|']
 for e,s in summary.items():
  for c in s['cells']:
   med='unknown' if c['median_solve_seconds'] is None else f"{c['median_solve_seconds']:.6f}";mad='unknown' if c['relative_mad'] is None else f"{100*c['relative_mad']:.3f}%";lines.append(f"| {e} / {c['candidate_id']} | {c['correct']}/5 | {med} | {mad} | {'pass' if c['pass'] else 'fail'} |")
 lines+=['','Admission requires all20valid results/engine and every cell median>=10ms/relativeMAD<=5%. This gate and a prospective10%paired practical margin were frozen before measurements. It is distinct from the earlier1%study; no claim about1%effects follows. Timeouts have missing successful-runtime values, not a measured10second solution. All intended probes remain in the denominator.','', 'Admitted engines: '+(', '.join(e for e,s in summary.items() if s['admitted']) or 'none')+'. No paired stage may proceed for an inadmissible engine under this protocol.','',f"Total subprocess collection time{sum(r['collection_seconds'] for r in rows):.3f}s; total observed solve time{sum(r['result']['solve_seconds'] for r in rows if r['result']):.3f}s. Import/model construction and validation are separately logged. This is actual feasibility-collection cost, not estimated B20deployment cost. Per-probe native process exits are saved; no server/background inference used.",'','The two implementations share a mathematical benchmark/domain, and Z3 was historically exposed in the repository. Neither engine is a new industrial application. Configuration variants/repeats cannot be counted as independent systems; feasibility now exposes bothfamilies for subsequent workload selection. Runtime feasibility does not establish useful LLM escalation, router generalization or journal readiness. External-host reproducibility and upstream full regressions remain untested.','','Evidence: results/v157_solvers/{001..040}.json,intents.jsonl,completion.json,summary.json,feasibility.png/svg; artifacts/study_v157/freeze.json,jobs.json. Raw solver text and exact solution vectors retained. Safe regeneration: `.venv/bin/python scripts/solver_feasibility_v157.py summarize`; `MPLCONFIGDIR=/tmp/mpl-v157 .venv/bin/python scripts/report_solvers_v157.py`. Collect is create-once; do not rerun it.']
 (ROOT/'reports/solvers_v157.md').write_text('\n'.join(lines)+'\n');(A/'replay.json').write_text(json.dumps({'verified':True,'charged':40,'assignments_checked':sum(bool(r['result'] and r['result']['correct']) for r in rows),'admitted':{e:s['admitted'] for e,s in summary.items()}},indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main()
