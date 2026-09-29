"""Charged lossless JPEG native trials. Generic search from frozen V131."""
import copy,hashlib,itertools,random,subprocess,time
from PIL import Image
from collect_smollm_v47 import ROOT,read,write,sha,now,append
import importlib.util
_spec=importlib.util.spec_from_file_location('_jpeg_search_v133',ROOT/'scripts/native_v131.py')
search=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(search)
from proposal_v128 import messages,domains,project,random_proposals
from router_v132 import features,predict,decide
A=ROOT/'artifacts/study_v133';O=ROOT/'results/v133_native';TASK='jpeg_lossless';SEEDS=[11,23,37,53,71]
XS=list(itertools.product(range(1,8),[0,1,4,16,64],[0,1]))
SPEC={'xs':XS,'names':['predictor_1through7','restart_rows_0none','layout_0interleaved_1separate_RGB'],'expert':(7,0,0),'default':(1,0,0),'meaning':'Total lossless JPEG bytes for three fixed RGB photographs. Smaller is better; all decoded RGB pixels must be exact. libjpeg-turbo3.1.2, 8-bit precision, point transform0, automatic optimized Huffman tables. Predictors1left,2above,3upperleft,4left+above-upperleft,5left+(above-upperleft)/2,6above+(left-upperleft)/2,7(left+above)/2. Restart interval is image rows,0none. Layout0single interleavedRGBscan,1three separate component scans. No color conversion, downsampling, smoothing or lossy quantization.'}
search.TASKS[TASK]=SPEC
MODES=search.MODES+['predictor_sweep']
def verify_freeze():
 for n,h in read(ROOT/'reports/protocol_v133.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def validated_pixels(path,w):
 im=Image.open(path);im.load();b=im.tobytes()
 if im.mode!='RGB' or im.size!=(w['width'],w['height']) or len(b)!=w['pixel_bytes'] or hashlib.sha256(b).hexdigest()!=w['pixel_sha256']:raise ValueError('Decoded RGB pixel mismatch')
 return {'mode':im.mode,'size':list(im.size),'pixel_bytes':len(b),'pixel_sha256':hashlib.sha256(b).hexdigest()}

def selection(prefix,mode,seed,proposals=None):
 if mode!='predictor_sweep':return search.choices(TASK,prefix,mode,seed,proposals)
 # Fixed domain-knowledge portfolio: all seven predictors at no restart,
 # interleaved first then separate RGB, skipping acquired rows.
 priority=[XS.index((p,0,layout)) for layout in [0,1] for p in range(1,8)]
 ids=[r for r in priority if r not in prefix['ids']]
 ids.extend(r for r in search.rank(TASK,prefix) if r not in ids)
 return ids[:10],[]

class Oracle:
 def __init__(self,phase,cap,seconds):
  self.out=O/phase;self.out.mkdir(parents=True,exist_ok=False);self.start=time.monotonic();self.cap=cap;self.seconds=seconds;self.work=read(A/'workloads.json')['workloads']
  self.ledger={'at':now(),'phase':phase,'configuration_attempts':0,'completed_configurations':0,'encodes':0,'decodes':0,'cap':cap,'seconds_cap':seconds};self.save()
 def save(self):self.ledger['seconds']=time.monotonic()-self.start;write(self.out/'ledger.json',self.ledger)
 def command(self,cmd,kind):
  remaining=self.seconds-(time.monotonic()-self.start)
  if remaining<=0:raise TimeoutError('Stage wall cap')
  self.ledger[kind]+=1;self.save();start=time.monotonic()
  try:
   p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=min(10,remaining));r={'command':cmd,'returncode':p.returncode,'seconds':time.monotonic()-start,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')};append(self.out/'commands.jsonl',r)
   if p.returncode:raise RuntimeError('Native process failed: '+r['stderr'])
   return r
  except subprocess.TimeoutExpired as e:append(self.out/'commands.jsonl',{'command':cmd,'seconds':time.monotonic()-start,'error':'timeout'});raise
 def acquire(self,key,row):
  if type(row) is not int or row not in range(len(XS)):raise ValueError('Invalid row')
  if self.ledger['configuration_attempts']>=self.cap or time.monotonic()-self.start>=self.seconds:raise ValueError('Native budget exhausted')
  out=self.out/key;out.mkdir(exist_ok=False);self.ledger['configuration_attempts']+=1;self.save();p,restart,layout=XS[row];append(self.out/'starts.jsonl',{'at':now(),'key':key,'row':row,'settings':XS[row],'attempt':self.ledger['configuration_attempts']});r={'key':key,'row':row,'settings':XS[row],'records':[]}
  try:
   for w in self.work:
    enc=out/(w['name']+'.jpg');dec=out/(w['name']+'.ppm');scan=ROOT/f'data/native_v133/scans_{p}_{layout}.txt';bin=ROOT/'.local-runtime/jpeg-v133'
    ce=self.command([str(bin/'cjpeg-static'),'-strict','-precision','8','-lossless',f'{p},0','-scans',str(scan),'-restart',str(restart),'-outfile',str(enc),str(ROOT/w['ppm'])],'encodes')
    de=self.command([str(bin/'djpeg-static'),'-strict','-pnm','-outfile',str(dec),str(enc)],'decodes');validation=validated_pixels(dec,w)
    r['records'].append({'name':w['name'],'encoded_path':str(enc.relative_to(ROOT)),'encoded_sha256':sha(enc),'encoded_bytes':enc.stat().st_size,'validation':validation,'encode':ce,'decode':de});dec.unlink()
   r.update(target=sum(v['encoded_bytes'] for v in r['records']),valid=True,at=now());write(out/'result.json',r);self.ledger['completed_configurations']+=1;return r['target']
  except Exception as e:r['error']=repr(e);write(out/'failure.json',r);self.ledger['error']=repr(e);raise
  finally:self.save()

def arm(oracle,prefix,mode,seed,proposals=None):
 s=copy.deepcopy(prefix);batch,diag=selection(prefix,mode,seed,proposals)
 for k in range(10):
  row=search.rank(TASK,s)[0] if batch is None else batch[k];search.observe(TASK,s,row,oracle.acquire(f'{seed}_{mode}_{k:02}',row))
 i=min(range(20),key=lambda k:s['labels'][k][0]);return {'state':s,'best':s['labels'][i][0],'incumbent':s['ids'][i],'diagnostics':diag}

def classical():
 verify_freeze();oracle=Oracle('classical',300,900);jobs=[];decisions=[];frozen=read(ROOT/'artifacts/study_v132/model.json');rt=time.monotonic()
 try:
  for seed in SEEDS:
   s=search.fresh(TASK,seed)
   for k in range(10):
    row=XS.index(SPEC['expert']) if k==0 else XS.index(SPEC['default']) if k==1 else next(i for i in s['order'] if i not in s['ids']) if k==2 else search.rank(TASK,s)[0]
    search.observe(TASK,s,row,oracle.acquire(f'{seed}_prefix_{k:02}',row))
   prefix=O/'prefixes'/f'{seed}.json';write(prefix,s);msg=A/'prompts'/f'{seed}.json';write(msg,messages(SPEC['names'],XS,s,SPEC['meaning'],'-'))
   jobs.append({'key':f'jpeg_{seed}','seed':seed,'sampling_seed':133000+seed,'domains':domains(XS),'system_group':'libjpeg','messages_path':str(msg.relative_to(ROOT)),'prefix_path':str(prefix.relative_to(ROOT)),'prefix_sha256':sha(prefix)})
   start=time.monotonic();f=features(s,domains(XS),'minimize');score=predict(frozen['model'],f);decision={'benefit':decide(score,frozen['benefit_calibration']['selected']['threshold']),'uncertainty':decide(f[-1],frozen['uncertainty_calibration']['selected']['threshold'])}
   decisions.append({'seed':seed,'at':now(),'features':f,'predicted_gain':score,'decisions':decision,'decision_seconds':time.monotonic()-start})
   # Save before even classical post-prefix labels for this new seed.
   write(A/'decisions.json',{'at':now(),'source_model':'artifacts/study_v132/model.json','rows':decisions})
   modes=MODES[:];random.Random(133600+seed).shuffle(modes)
   for mode in modes:write(O/'arms'/f'{seed}_{mode}.json',arm(oracle,s,mode,seed))
  write(A/'jobs.json',jobs);paths=[A/'jobs.json',A/'decisions.json']+list((A/'prompts').glob('*.json'))+list((O/'prefixes').glob('*.json'));write(A/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
 finally:oracle.save()

def continuations():
 verify_freeze()
 for n,h in read(A/'inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 oracle=Oracle('continuations',53,300)
 try:
  for seed in SEEDS:
   path=ROOT/f'results/v133_proposals/scores/jpeg_{seed}.json';score=read(path) if path.exists() else {'status':'unattempted'};p=score.get('score') if score['status']=='valid' else None
   r=arm(oracle,read(O/'prefixes'/f'{seed}.json'),'llm' if p is not None else 'sequential_3nn',seed,p);r.update(model_status=score['status'],fallback=p is None);write(O/'arms'/f'{seed}_llm.json',r)
  for k in range(3):oracle.acquire(f'reference_repeat_{k}',XS.index(SPEC['expert']))
 finally:oracle.save()
if __name__=='__main__':
 import sys
 if sys.argv[1:]==['classical']:classical()
 elif sys.argv[1:]==['continuations']:continuations()
 else:raise SystemExit('Expected classical or continuations (create once)')
