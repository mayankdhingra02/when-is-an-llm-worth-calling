"""Build a standard-library version of the saved-evidence verifier."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'scripts/verify_proposal_v127_fixed.py').read_text()
a=source.index('from collect_smollm_v47');b=source.index('\ndef independent_project',a)
header='''from pathlib import Path
from types import SimpleNamespace
from functools import lru_cache
import hashlib,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from proposal_v127 import messages,payload,parse,project
OUT=ROOT/'results/v127_analysis'
def read(p):return json.loads(Path(p if Path(p).is_absolute() else ROOT/p).read_text())
def sha(p):return hashlib.sha256(Path(p if Path(p).is_absolute() else ROOT/p).read_bytes()).hexdigest()
def write(p,v):pass  # Portable replay does not mutate evidence.
def frozen():
 m=read(ROOT/'manifest.json')
 for n,v in m['files'].items():assert sha(ROOT/n)==v['sha256'] and (ROOT/n).stat().st_size==v['bytes'],n
 for n,h in read(ROOT/'reports/protocol_v127.freeze.json')['sha256'].items():
  if (ROOT/n).is_file():assert sha(ROOT/n)==h,n
@lru_cache(maxsize=6)
def candidates(dataset):
 spec=next(s for s in read(ROOT/'data/manifest_v41.json')['datasets'] if s['id']==dataset)
 lines=(ROOT/spec['path']).read_text().splitlines();header=next(csv.reader([lines[0]],delimiter=spec['delimiter']));xs=[]
 for line in spec['subset']['source_lines']:
  row=dict(zip(header,next(csv.reader([lines[line-1]],delimiter=spec['delimiter']))));xs.append(tuple(float(row[n]) for n in spec['feature_names']))
 return spec,SimpleNamespace(x=tuple(xs),names=spec['feature_names'],source_ids=spec['subset']['source_lines'])
def references(j,p,direction):
 refs={};opt=min if direction=='-' else max
 paths={**{m:f"results/v41_transfer/arms/{j['base_key']}_{m}.json" for m in ['batch_3nn','full_sequential_3nn','random_full']},'presentation_first10':f"results/v41_models/0.5/arms/{j['base_key']}.json",'single_portfolio':f"results/v115_portfolio/arms/{j['base_key']}.json"}
 for m,n in paths.items():
  if not (ROOT/n).exists():assert m=='single_portfolio';continue
  s=read(ROOT/n)['state'];assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels'] and len(set(s['ids']))==20
  if m=='presentation_first10':assert s['ids'][10:]==[p['pool']['mapping'][i] for i in '0123456789']
  refs[m]=opt(y[0] for y in s['labels'])
 return refs
'''
source=source[:a]+header+source[b:]
source=source.replace("choices,d=choose();assert d==read(OUT/'diagnostics.json')",'''choices=[read(p) for p in sorted((OUT/'choices').glob('*.json'))];d=read(OUT/'diagnostics.json');assert len(choices)==90
 dm={r['key']:r for r in d['requests']};assert set(dm)==set(jm)
 for j in jobs:
  dd=dm[j['key']];r=rm.get(j['key']);spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix'])['state']
  try:
   if r is None:raise ValueError('No returned response')
   props=parse(r['response'],j['domains']);selected,detail=project(props,c.x,p)
  except ValueError:
   assert dd['status']==('missing' if r is None else 'invalid') and dd['selected_rows'] is None
  else:assert dd['status']=='valid' and dd['selected_rows']==independent_project(c.x,p['order'],p['ids'],props)==selected and dd['projection']==detail
 for r in d['label_rotation_probes']:
  a=dm[r['key']+'_normal']['selected_rows'];b=dm[r['key']+'_rotated_labels']['selected_rows'];valid=a is not None and b is not None;assert r['both_valid']==valid
  if valid:assert r['selection_set_overlap']==len(set(a)&set(b)) and r['same_order']==(a==b)''')
source=source.replace("assert ch['selected_rows']==selected;es=", "assert ch['fallback']==(ch['mode']=='model' and dm[ch['request_key']]['status']!='valid');assert ch['selected_rows']==selected;es=")
source=source.replace("assert v['wins']+v['ties']+v['losses']==len(rs)","assert v['wins']==sum(r['gains'][m]>1e-12 for r in rs);assert v['ties']==sum(abs(r['gains'][m])<=1e-12 for r in rs);assert v['losses']==sum(r['gains'][m]<-1e-12 for r in rs)")
source=source.replace("receipt={'verified':True", "primary=['full_sequential_3nn','random_projection','full_batch_3nn'];joint=sum(all(r['gains'][m]>=.05 for m in primary) for r in result['cases']);assert result['joint_5pct_cases']==joint;assert result['normal_valid']==sum(r['condition']=='normal' and r['status']=='valid' for r in d['requests'])\n receipt={'verified':True")
(ROOT/'scripts/replay_proposal_v127_standalone.py').write_text(source)
print('Prepared independent standard-library projection/ranking replay; no experiment execution')
