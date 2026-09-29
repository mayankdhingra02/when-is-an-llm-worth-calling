"""Independent acquisition, reference-selection, prefix and diagnostic replay."""
import copy,json,random,statistics,hashlib
from pathlib import Path
from app_validation_v163 import Reference
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v165';O=ROOT/'results/v165_headroom'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_reference(observed,selection):
 expected=[min((x for x in selection if x['engine']==e and x['valid']),key=lambda x:(x['median'],x['row_id'])) for e in ['ripgrep','hnswlib']]
 assert observed==expected

def main():
 ref=Reference();freeze=read(A/'freeze.json');cfg=read(ROOT/'configs/study_v165.json');assert cfg['max_new_model_requests']==cfg['new_download_bytes_cap']==0
 for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
 plan=[]
 for phase,base in [('selection',165100),('validation',165200)]:
  for block in range(3):
   rows=[{'phase':phase,'block':block,'engine':e,'row_id':i} for e in ['ripgrep','hnswlib'] for i in range(64)];random.Random(base+block).shuffle(rows);plan+=rows
 assert read(A/'plan.json')==plan
 raw=[read(O/'acquisitions'/f'{i:03d}.json') for i in range(1,769)];cs={e:read(A/'candidates'/f'{e}.json') for e in ['ripgrep','hnswlib']}
 def check(r):
  v=r['measurement'];assert r['returncode']==0 and v['engine']==r['job']['engine'] and v['config']==cs[r['job']['engine']]['configs'][r['job']['row_id']];assert ref.validate(v)==r['value'];assert r['status']==('correct' if v['quality']>=.95 else 'quality_penalty')
 for k,(r,j) in enumerate(zip(raw,plan),1):assert r['charge']==k and r['job']==j and r['at_unix']>freeze['at_unix'];check(r)
 assert sum(r['measurement']['native_invocations'] for r in raw)==2304
 complete=read(O/'completion.json');assert complete['charged_outcomes']==768 and complete['unattempted']==0 and complete['error']is None and complete['new_model_requests']==0 and complete['seconds']<1800
 seal=read(O/'reference.freeze.json');assert len(seal['sha256'])==385 and max(r['at_unix'] for r in raw[:384])<seal['at_unix']<min(r['at_unix'] for r in raw[384:])
 for n,h in seal['sha256'].items():assert sha(ROOT/n)==h,n
 def cells(phase):
  out=[]
  for e in ['ripgrep','hnswlib']:
   for i in range(64):
    rr=[r for r in raw if r['job']['phase']==phase and r['job']['engine']==e and r['job']['row_id']==i];assert len(rr)==3 and {r['job']['block'] for r in rr}=={0,1,2};vals=[r['value'] for r in rr];med=sorted(vals)[1];out.append({'engine':e,'row_id':i,'median':med,'relative_mad':sorted(abs(x-med) for x in vals)[1]/med,'valid':all(r['status']=='correct' for r in rr),'values':vals,'minimum_quality':min(r['measurement']['quality'] for r in rr)})
  return out
 selection=cells('selection');validation=cells('validation');selected=[min((x for x in selection if x['engine']==e and x['valid']),key=lambda x:(x['median'],x['row_id'])) for e in ['ripgrep','hnswlib']];check_reference(read(O/'selected_reference.json'),selection)
 targets=read(A/'targets.json');assert len(targets)==120
 for t in targets:
  assert sha(ROOT/t['source'])==t['source_sha256']
  if t['kind']=='prefix':
   p=read(ROOT/t['source']);assert t['checkpoint'] in [4,7,10];k=min(range(t['checkpoint']),key=lambda i:p['labels'][i][0]);assert t['row_id']==p['ids'][k]
  else:assert t['row_id']==next(x['row_id'] for x in read(ROOT/t['source']) if x['case']==t['case'] and x['arm']==t['arm'])
 comp=read(O/'comparison.json');assert comp['selection_cells']==selection and comp['validation_cells']==validation and len(comp['targets'])==120
 for t,x in zip(targets,comp['targets']):
  assert all(x[k]==v for k,v in t.items());candidate=next(v for v in validation if v['engine']==t['engine'] and v['row_id']==t['row_id']);i=next(r['row_id'] for r in selected if r['engine']==t['engine']);r=next(v for v in validation if v['engine']==t['engine'] and v['row_id']==i);gap=(candidate['median']-r['median'])/candidate['median'];stable=all(v['valid'] and v['relative_mad']<=.05 and v['median']>=.01 for v in [candidate,r]);assert x['headroom']==gap and x['same_reference_setting']==(t['row_id']==i) and x['stable_quality_comparison']==stable and x['robust_practical_headroom']==(gap>.1 and i!=t['row_id'] and stable)
 for s in comp['prefix_summary']:
  rr=[x for x in comp['targets'] if x['kind']=='prefix' and x['engine']==s['engine'] and x['checkpoint']==s['checkpoint']];assert len(rr)==s['cases']==5 and s['mean_headroom']==statistics.mean(x['headroom'] for x in rr) and s['robust_practical_cases']==sum(x['robust_practical_headroom'] for x in rr)
 posthoc=read(O/'posthoc_validation_minimum.json');assert len(posthoc['rows'])==30
 for x in posthoc['rows']:
  t=next(t for t in comp['targets'] if t['kind']=='prefix' and t['case']==x['case'] and t['checkpoint']==x['checkpoint']);best=min((v for v in validation if v['engine']==x['engine'] and v['valid']),key=lambda v:(v['median'],v['row_id']));assert x['validation_minimum_id']==best['row_id'] and x['optimistic_observed_headroom']==(t['validation_median']-best['median'])/t['validation_median']
 # Semantics must reject corruption of observations and selecting a validation winner as primary.
 rejected=[]
 for kind in ['value','quality','configuration']:
  r=copy.deepcopy(raw[0])
  if kind=='value':r['value']*=2
  elif kind=='quality':r['measurement']['quality']=0.
  else:r['job']['row_id']=(r['job']['row_id']+1)%64
  try:check(r)
  except AssertionError:rejected.append(kind)
  else:raise AssertionError('Accepted '+kind)
 altered=copy.deepcopy(selected);altered[0]['row_id']=(altered[0]['row_id']+1)%64
 try:check_reference(altered,selection)
 except AssertionError:rejected.append('reference_id_change')
 else:raise AssertionError('Altered reference accepted')
 receipt={'verified':True,'new_outcomes':768,'native_invocations':2304,'new_model_requests':0,'selection_cells':128,'validation_cells':128,'reference_fixed_before_validation':True,'frozen_prefix_targets':30,'frozen_prior_incumbent_targets':90,'posthoc_targets_checked':30,'mutations_rejected':rejected,'scope':'Independent internal replay; not independently collected host evidence'};(A/'replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
