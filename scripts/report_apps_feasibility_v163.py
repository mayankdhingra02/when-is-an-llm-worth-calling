"""Independent admission replay and descriptive report for both retained stages."""
import copy,json,statistics,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app_validation_v163 import Reference
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v163'
def read(p):return json.loads(p.read_text())
def main():
 ref=Reference();out={};text=['# V161–V162: native application feasibility','','Both stages remain in the evidence. V161 failed; V162 was frozen before a repaired workload/domain ran. No model outputs were used to select either design. Configuration outcomes and underlying native invocations are distinct counters.','','| Stage | Application / setting | Valid quality / 5 | Minimum observed quality | Median raw seconds | Relative MAD of valid timings | Admitted cell |','|---|---|---:|---:|---:|---:|---|']
 for version in [161,162]:
  base=ROOT/f'results/v{version}_apps';artifact=ROOT/f'artifacts/study_v{version}';jobs=read(artifact/'jobs.json');raw=[read(base/f'{i:03d}.json') for i in range(1,41)];summary=read(base/'summary.json');calls=0
  for n,h in read(artifact/'freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
  for i,(r,j) in enumerate(zip(raw,jobs),1):
   assert r['charge']==i and r['job']==j and r['status']=='completed';v=copy.deepcopy(r['result']);assert v['config']==j['config']
   if version==161 and j['engine']=='ripgrep':
    expected=read(ROOT/'artifacts/study_v160/rg_reference.json');actual={}
    for line in v['stdout'].encode().split(b'\n'):
     if not line:continue
     k,n=line.rsplit(b'\0',1);k=k.decode().removeprefix('./');assert k not in actual;actual[k]=int(n)
    assert actual==expected and v['correct'] and v['quality']==1 and v['value']==v['objective_seconds'];calls+=1
   else:
    if version==161:v['native_invocations']=1
    ref.validate(v);calls+=v['native_invocations']
  cells=[]
  for e in ['ripgrep','hnswlib']:
   for c in summary[e]['cells']:
    rs=[r['result'] for r in raw if r['job']['engine']==e and r['job']['candidate_id']==c['candidate_id']];good=[r['objective_seconds'] for r in rs if r['correct'] and r['quality']>=.95];med=statistics.median(good) if good else None;mad=statistics.median(abs(t-med) for t in good)/med if good else None;passed=len(good)==5 and med>=.01 and mad<=.05
    assert c['valid_quality']==len(good) and c['median_seconds']==med and c['relative_mad']==mad and c['pass']==passed
    x={'stage':version,'engine':e,'candidate_id':c['candidate_id'],'valid_quality':len(good),'minimum_observed_quality':min(r['quality'] for r in rs),'median_raw_seconds':statistics.median(r['objective_seconds'] for r in rs),'relative_mad':mad,'pass':passed};cells.append(x)
    madtext='undefined (no quality-feasible results)' if mad is None else f'{100*mad:.3f}%';text.append(f"| {version} | {e} / {c['candidate_id']} | {len(good)}/5 | {100*x['minimum_observed_quality']:.3f}% | {x['median_raw_seconds']:.6f} | {madtext} | {'pass' if passed else 'fail'} |")
  assert calls==(40 if version==161 else 120);out[str(version)]={'configuration_outcomes':40,'native_invocations':calls,'seconds':read(base/'completion.json')['seconds'],'cells':cells,'admitted':{e:summary[e]['admitted'] for e in summary}}
 text+=['','V161 ripgrep failed the fixed 5% MAD gate in two cells. Its hnswlib smallest graph/search cell returned valid neighbor IDs but only89.416% recall, below95%. These five infeasible outcomes used the declared20s utility penalty; their measured raw execution time is still retained. No missing value or penalty is represented as a successful constrained runtime.','','V162 uses five distinct fixed code-analytics queries, one aggregate timer per setting and five separately counted native invocations. It does not measure individual query timings or repeat the same query to acquire uncharged reliability labels. Hnswlib increases minimum M/construction ef, with the same recall and timing thresholds. All40outcomes passed; two implementations are admitted. This is feasibility-based design exposure, not untouched production evidence.','','Independent checks reconstructed search counts and ANN distances using a separate norm/dot formula. All80configuration outcomes and160native workload invocations are accounted for. Collection caps600s/stage and full intended denominators are preserved. No model request, retry or native warmup occurred. The initial reference timing is unknown because its receipt failed after a linker error; V162 reference preparation has its own receipt.','','Raw artifacts: results/v161_apps and results/v162_apps; plans/code hashes: artifacts/study_v161 and study_v162. Safe report replay: .venv/bin/python scripts/report_apps_feasibility_v163.py.']
 (ROOT/'reports/apps_feasibility_v163.md').write_text('\n'.join(text)+'\n');(A/'feasibility_replay.json').write_text(json.dumps({'verified':True,'stages':out},indent=2)+'\n')
 plt.rcParams['svg.hashsalt']='apps-feas-v163';fig,axs=plt.subplots(1,2,figsize=(11,4));fig.subplots_adjust(left=.075,right=.98,bottom=.3,top=.83,wspace=.27)
 for ax,(version,data) in zip(axs,out.items()):
  cs=data['cells'];ax.bar(range(8),[100*c['minimum_observed_quality'] for c in cs],color=['#176d8c' if c['pass'] else '#b94a3b' for c in cs]);ax.axhline(95,ls=':',color='gray');ax.set_ylim(85,101);ax.set_xticks(range(8),[c['engine']+' '+str(c['candidate_id']) for c in cs],rotation=60,ha='right',fontsize=8);ax.set_ylabel('Minimum quality (%)');ax.set_title('V'+version+(' — admitted' if all(data['admitted'].values()) else ' — failed admission'));ax.grid(axis='y',alpha=.15)
 fig.suptitle('Feasibility: quality and timing gate, all intended cells retained\nRed cells fail quality or timing; dotted line marks the ANN quality threshold',fontsize=11);fig.savefig(A/'feasibility.png',dpi=160,metadata={'Software':'V163'});fig.savefig(A/'feasibility.svg',metadata={'Date':None});plt.close(fig);print(json.dumps({'verified':True,'configuration_outcomes':80,'native_invocations':160,'stages':{v:d['admitted'] for v,d in out.items()}}))
if __name__=='__main__':main()
