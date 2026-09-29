"""Bounded, byte-validated native XZ task; no stored hidden outcome table."""
import copy,hashlib,importlib.util,itertools,os,random,subprocess,time
from collect_smollm_v47 import ROOT,read,write,sha,now,append
from proposal_v128 import messages,domains,project
from router_v132 import features,predict,decide
from incumbent_v138 import choose
_spec=importlib.util.spec_from_file_location('_xz_search_v140',ROOT/'scripts/native_v131.py')
search=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(search)
A=ROOT/'artifacts/study_v140';O=ROOT/'results/v140_native';TASK='xz';SEEDS=[11,23,37,53,71]
XS=list(itertools.product([0,1,3],[0,1],[0,2],[0,1],[16,64,128],[0,16,64]))
SPEC={'xs':XS,'names':['literal_context_bits_lc','literal_position_bits_lp','position_bits_pb','algorithm_0fast_hc4_1normal_bt4','nice_match_length','search_depth_0automatic'],'expert':(3,0,2,1,128,0),'default':(3,0,2,1,64,0),'meaning':'Minimize total XZ file bytes for three fixed complete RGB PPM photographs. XZ5.8.4/LZMA2, fixed8MiB dictionary, one thread, CRC64, no preprocessing or lossy changes. Every output must decompress to identical source bytes. lc literal context bits; lp literal position bits; lc+lp<=4. pb position bits. Algorithm0 fast mode with hc4 match finder, algorithm1 normal mode with bt4. nice match length16/64/128; depth0automatic,16/64fixed search depth. No runtime/energy objective; original full images remain unchanged.'}
search.TASKS[TASK]=SPEC
MODES=['sequential_3nn','random_full','fixed_prefix_neighbor','adaptive_incumbent_neighbor','context_sweep']
def verify_freeze():
 for n,h in read(ROOT/'reports/protocol_v140.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
def arguments(row):
 if type(row) is not int or row not in range(len(XS)):raise ValueError('Invalid row')
 lc,lp,pb,algorithm,nice,depth=XS[row];mode,mf=[('fast','hc4'),('normal','bt4')][algorithm]
 return ['--format=xz','--threads=1','--check=crc64','--memlimit-compress=256MiB','--no-adjust',f'--lzma2=dict=8MiB,lc={lc},lp={lp},pb={pb},mode={mode},mf={mf},nice={nice},depth={depth}']
def validated_bytes(path,w):
 n=path.stat().st_size;h=sha(path)
 if n!=w['bytes'] or h!=w['sha256']:raise ValueError('Decoded source bytes mismatch')
 return {'decoded_bytes':n,'decoded_sha256':h}
def selection(prefix,mode,seed,proposals=None):
 if mode in ['fixed_prefix_neighbor','adaptive_incumbent_neighbor']:return None,[]
 if mode=='context_sweep':
  ids=[XS.index((lc,lp,pb,1,128,0)) for lc in [0,1,3] for lp in [0,1] for pb in [0,2]];ids=[i for i in ids if i not in prefix['ids']];ids.extend(i for i in search.rank(TASK,prefix) if i not in ids);return ids[:10],[]
 return search.choices(TASK,prefix,mode,seed,proposals)
class Oracle:
 def __init__(self,phase,cap,seconds):
  self.out=O/phase;self.out.mkdir(parents=True,exist_ok=False);self.start=time.monotonic();self.cap=cap;self.seconds=seconds;self.work=read(A/'workloads.json')['workloads'];self.bin=ROOT/'.local-runtime/xz-v140/xz'
  assert sha(self.bin)==read(A/'build.json')['binaries']['.local-runtime/xz-v140/xz']
  for w in self.work:assert sha(ROOT/w['path'])==w['sha256']
  self.env={k:v for k,v in os.environ.items() if k not in ['XZ_DEFAULTS','XZ_OPT','LZMA_API_STATIC']};self.ledger={'at':now(),'phase':phase,'configuration_attempts':0,'completed_configurations':0,'encodes':0,'decodes':0,'cap':cap,'seconds_cap':seconds};self.save()
 def save(self):self.ledger['seconds']=time.monotonic()-self.start;write(self.out/'ledger.json',self.ledger)
 def command(self,cmd,kind,dest):
  remain=self.seconds-(time.monotonic()-self.start)
  if remain<=0:raise TimeoutError('Native stage time limit')
  self.ledger[kind]+=1;self.save();start=time.monotonic()
  try:
   with dest.open('xb') as f:p=subprocess.run(cmd,cwd=ROOT,env=self.env,stdout=f,stderr=subprocess.PIPE,timeout=min(10,remain))
   r={'command':cmd,'returncode':p.returncode,'seconds':time.monotonic()-start,'stderr':p.stderr.decode(errors='replace')};append(self.out/'commands.jsonl',r)
   if p.returncode:raise RuntimeError('Native failed: '+r['stderr'])
   return r
  except subprocess.TimeoutExpired:append(self.out/'commands.jsonl',{'command':cmd,'seconds':time.monotonic()-start,'error':'timeout'});raise
 def acquire(self,key,row):
  args=arguments(row)
  if self.ledger['configuration_attempts']>=self.cap or time.monotonic()-self.start>=self.seconds:raise RuntimeError('Native acquisition limit')
  dest=self.out/key;dest.mkdir(exist_ok=False);self.ledger['configuration_attempts']+=1;self.save();append(self.out/'starts.jsonl',{'at':now(),'at_unix':time.time(),'key':key,'row':row,'settings':XS[row],'attempt':self.ledger['configuration_attempts']});r={'key':key,'row':row,'settings':XS[row],'records':[]}
  try:
   for w in self.work:
    enc=dest/(w['name']+'.xz');dec=dest/(w['name']+'.ppm')
    ce=self.command([str(self.bin),*args,'--stdout','--',str(ROOT/w['path'])],'encodes',enc)
    de=self.command([str(self.bin),'--decompress','--stdout','--threads=1','--memlimit-decompress=256MiB','--',str(enc)],'decodes',dec);v=validated_bytes(dec,w)
    r['records'].append({'name':w['name'],'encoded_path':str(enc.relative_to(ROOT)),'encoded_sha256':sha(enc),'encoded_bytes':enc.stat().st_size,'validation':v,'encode':ce,'decode':de});dec.unlink()
   r.update(target=sum(x['encoded_bytes'] for x in r['records']),valid=True,at=now(),at_unix=time.time());write(dest/'result.json',r);self.ledger['completed_configurations']+=1;return r['target']
  except Exception as e:r['error']=repr(e);write(dest/'failure.json',r);self.ledger['error']=repr(e);raise
  finally:self.save()
def acquire_step(oracle,s,prefix,key,mode,step,row):
 write(O/'selections'/f'{key}.json',{'key':key,'mode':mode,'step':step,'before':copy.deepcopy(s),'row':row,'at_unix':time.time()});search.observe(TASK,s,row,oracle.acquire(key,row))
def arm(oracle,prefix,mode,seed,proposals=None,arm_name=None):
 s=copy.deepcopy(prefix);batch,diag=selection(prefix,mode,seed,proposals)
 for k in range(10):
  row=choose(XS,prefix,s,'-',mode)['row_id'] if mode in ['fixed_prefix_neighbor','adaptive_incumbent_neighbor'] else search.rank(TASK,s)[0] if batch is None else batch[k]
  acquire_step(oracle,s,prefix,f'{seed}_{arm_name or mode}_{k:02}',mode,k,row)
 i=min(range(20),key=lambda k:s['labels'][k][0]);return {'state':s,'best':s['labels'][i][0],'incumbent':s['ids'][i],'diagnostics':diag}
def classical():
 verify_freeze();oracle=Oracle('classical',300,900);jobs=[];decisions=[];frozen=read(ROOT/'artifacts/study_v132/model.json')
 try:
  for seed in SEEDS:
   s=search.fresh(TASK,seed)
   for k in range(10):
    row=XS.index(SPEC['expert']) if k==0 else XS.index(SPEC['default']) if k==1 else next(i for i in s['order'] if i not in s['ids']) if k==2 else search.rank(TASK,s)[0]
    acquire_step(oracle,s,None,f'{seed}_prefix_{k:02}','prefix',k,row)
   prefix=O/'prefixes'/f'{seed}.json';write(prefix,s);msg=A/'prompts'/f'{seed}.json';write(msg,messages(SPEC['names'],XS,s,SPEC['meaning'],'-'))
   jobs.append({'key':f'xz_{seed}','seed':seed,'sampling_seed':140000+seed,'domains':domains(XS),'system_group':'xz','messages_path':str(msg.relative_to(ROOT)),'prefix_path':str(prefix.relative_to(ROOT)),'prefix_sha256':sha(prefix)})
   t=time.monotonic();f=features(s,domains(XS),'minimize');score=predict(frozen['model'],f);d={'benefit':decide(score,frozen['benefit_calibration']['selected']['threshold']),'uncertainty':decide(f[-1],frozen['uncertainty_calibration']['selected']['threshold'])}
   decisions.append({'seed':seed,'at':now(),'at_unix':time.time(),'features':f,'predicted_gain':score,'decisions':d,'decision_seconds':time.monotonic()-t});write(A/'decisions.json',{'source_model':'artifacts/study_v132/model.json','rows':decisions})
   modes=MODES[:];random.Random(140600+seed).shuffle(modes)
   for mode in modes:write(O/'arms'/f'{seed}_{mode}.json',arm(oracle,s,mode,seed))
  write(A/'jobs.json',jobs);paths=[A/'jobs.json',A/'decisions.json']+list((A/'prompts').glob('*.json'))+list((O/'prefixes').glob('*.json'));write(A/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
 finally:oracle.save()
def continuations():
 verify_freeze()
 for n,h in read(A/'inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 oracle=Oracle('continuations',53,300)
 try:
  for seed in SEEDS:
   p=ROOT/f'results/v140_proposals/scores/xz_{seed}.json';score=read(p) if p.exists() else {'status':'unattempted'};prop=score.get('score') if score['status']=='valid' else None
   r=arm(oracle,read(O/'prefixes'/f'{seed}.json'),'llm' if prop is not None else 'sequential_3nn',seed,prop,arm_name='llm');r.update(model_status=score['status'],fallback=prop is None);write(O/'arms'/f'{seed}_llm.json',r)
  for k in range(3):oracle.acquire(f'reference_repeat_{k}',XS.index(SPEC['expert']))
 finally:oracle.save()
if __name__=='__main__':
 import sys
 if sys.argv[1:]==['classical']:classical()
 elif sys.argv[1:]==['continuations']:continuations()
 else:raise SystemExit('classical or continuations; create once')
