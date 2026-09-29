"""Prospective two-family B10/B20 native experiment with isolated charged trials."""
import copy,itertools,json,random,subprocess,time
from fractions import Fraction
import numpy as np
from collect_smollm_v47 import ROOT,read,write,sha,now,append
from proposal_v128 import messages,domains,project,random_proposals
A=ROOT/'artifacts/study_v131';O=ROOT/'results/v131_native';SEEDS=[11,23,37,53,71]
MODES=['sequential_3nn','batch_3nn','random_projection','random_full']
TASKS={
 'wavpack':{'xs':list(itertools.product([0,1,2,3],[0,2,4,6],[0,2048,8192,32768,65536])), 'names':['mode_0fast_1normal_2high_3veryhigh','extra_processing','block_samples_0automatic'],'expert':(3,6,0),'default':(1,0,0),'meaning':'Sum of lossless WavPack 5.9.0 file bytes on three fixed16kHz mono16-bit speech clips. Smaller is better. All results must reconstruct identical samples; one thread, no lossy/hybrid mode. Mode0fast,1normal,2high,3veryhigh; extra processing0,2,4,6; block0means encoder automatic.'},
 'fftw':{'xs':list(itertools.product([0,1,2],[1,2,4],[0,1],[1,2])), 'names':['planner_0estimate_1measure_2patient','threads','inplace_0no_1yes','complex_element_stride'],'expert':(2,1,0,1),'default':(1,1,0,1),'meaning':'Integer nanoseconds for fixed8192-point forward complex FFTs of three real speech windows;256 executions per window including input restoration, excluding planning. Lower is better. FFTW3.3.11 double/ARM NEON; planner0estimate,1measure,2patient with fixed0.02s planning time limit. One plan reused per trial; no shared wisdom. Output must match independent reference.'}}

def fresh(task,seed):
 order=list(range(len(TASKS[task]['xs'])));random.Random(seed).shuffle(order);return {'ids':[],'labels':[],'order':order}
def rank(task,s):
 xs=TASKS[task]['xs'];out=[]
 if len(s['ids'])<3:raise ValueError('Insufficient acquired targets')
 for row in s['order']:
  if row in s['ids']:continue
  near=sorted(range(len(s['ids'])),key=lambda k:sum(a!=b for a,b in zip(xs[row],xs[s['ids'][k]])))[:3]
  out.append((sum(Fraction(s['labels'][k][0]) for k in near)/3,row))
 return [i for _,i in sorted(out,key=lambda x:x[0])]
def observe(task,s,row,target):
 if len(s['ids'])>=20 or type(row) is not int or row not in range(len(TASKS[task]['xs'])) or row in s['ids']:raise ValueError('Invalid or over-budget acquisition')
 if type(target) is not int or target<=0:raise ValueError('Invalid target')
 s['ids'].append(row);s['labels'].append([target])
def choices(task,prefix,mode,seed,proposals=None):
 if len(prefix['ids'])!=10:raise ValueError('Expected B10')
 xs=TASKS[task]['xs']
 if mode=='sequential_3nn':return None,[]
 if mode=='batch_3nn':return rank(task,prefix)[:10],[]
 if mode=='random_full':return random.Random(131400+seed).sample([i for i in prefix['order'] if i not in prefix['ids']],10),[]
 if mode=='random_projection':return project(random_proposals(domains(xs),131900+seed),xs,prefix)
 if mode=='llm':return project(proposals,xs,prefix)
 raise ValueError('Unknown arm')
def numerical_check(actual,reference):
 if actual.shape!=reference.shape or not np.isfinite(actual).all():raise ValueError('Invalid numerical output')
 error=float(np.max(np.abs(actual-reference)));bound=1e-10*max(1.,float(np.max(np.abs(reference))))
 if error>bound:raise ValueError('FFT failed reference tolerance')
 return {'max_absolute_error':error,'tolerance':bound,'validated_complex_values':actual.size}
def verify_freeze():
 for n,h in read(ROOT/'reports/protocol_v131.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

class Oracle:
 def __init__(self,phase,cap,seconds):
  self.out=O/phase;self.out.mkdir(parents=True,exist_ok=False);self.start=time.monotonic();self.seconds=seconds;self.cap=cap;self.count=0;self.work=read(A/'workloads.json');self.reference=np.fromfile(ROOT/self.work['fftw_reference']['path'],dtype='<c16')
  for n,h in read(A/'binaries.json').items():assert sha(ROOT/n)==h,n
  self.ledger={'at':now(),'phase':phase,'configuration_attempts':0,'completed_configurations':0,'wavpack_encodes':0,'wavpack_decodes':0,'fftw_worker_calls':0,'cap':cap,'seconds_cap':seconds,'by_task':{'wavpack':0,'fftw':0}}
 def command(self,cmd,kind):
  remain=self.seconds-(time.monotonic()-self.start)
  if remain<=0:raise TimeoutError('Native stage exhausted')
  self.ledger[kind]+=1;self.save();t=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=min(10,remain))
  r={'command':cmd,'returncode':p.returncode,'seconds':time.monotonic()-t,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')};append(self.out/'commands.jsonl',r)
  if p.returncode:raise RuntimeError('Native failed: '+r['stderr'])
  return r
 def acquire(self,task,key,row):
  if self.count>=self.cap:raise ValueError('Stage configuration cap')
  if time.monotonic()-self.start>=self.seconds:raise TimeoutError('Stage time cap')
  xs=TASKS[task]['xs'];assert type(row) is int and row in range(len(xs))
  dest=self.out/key;dest.mkdir(exist_ok=False);self.count+=1;self.ledger['configuration_attempts']=self.count;self.ledger['by_task'][task]+=1;self.save();append(self.out/'starts.jsonl',{'at':now(),'key':key,'task':task,'row':row,'settings':xs[row],'attempt':self.count})
  result={'key':key,'task':task,'row':row,'settings':xs[row],'records':[]}
  try:
   if task=='wavpack':
    mode,extra,block=xs[row];bin=ROOT/'.local-runtime/native-v131/wavpack';settings=([['-f'],[],['-h'],['-hh']][mode])+[f'-x{extra}']+([f'--blocksize={block}'] if block else [])
    for j,w in enumerate(self.work['workloads']):
     encoded=dest/f'{j}.wv';decoded=dest/f'{j}.raw'
     enc=self.command([str(bin/'wavpack'),'-q','--no-threads','--raw-pcm=16000,16,1,le',*settings,'-o',str(encoded),w['raw_path']],'wavpack_encodes')
     dec=self.command([str(bin/'wvunpack'),'-q','-r','-o',str(decoded),str(encoded)],'wavpack_decodes')
     assert decoded.stat().st_size==w['raw_bytes'] and sha(decoded)==w['raw_sha256'],'Lossless sample mismatch'
     result['records'].append({'workload':j,'encoded_path':str(encoded.relative_to(ROOT)),'encoded_sha256':sha(encoded),'bytes':encoded.stat().st_size,'decoded_bytes':decoded.stat().st_size,'decoded_sha256':sha(decoded),'encode':enc,'decode':dec});decoded.unlink()
    result['target']=sum(r['bytes'] for r in result['records'])
   else:
    output=dest/'output.c128';cmd=[str(ROOT/'.local-runtime/native-v131/fftw_worker'),*map(str,xs[row]),str(ROOT/self.work['fftw_input']['path']),str(output)];record=self.command(cmd,'fftw_worker_calls');metrics=json.loads(record['stdout']);check=numerical_check(np.fromfile(output,dtype='<c16'),self.reference)
    assert metrics['n']==8192 and metrics['clips']==3 and metrics['iterations_per_clip']==256 and metrics['warmup_per_clip']==8 and metrics['target_ns']==sum(metrics['workload_ns']) and metrics['target_ns']>0
    result.update(target=metrics['target_ns'],metrics=metrics,validation=check,output_path=str(output.relative_to(ROOT)),output_sha256=sha(output),records=[record])
   result['at']=now();result['valid']=True;write(dest/'result.json',result);self.ledger['completed_configurations']+=1;return result['target']
  except Exception as e:result['error']=repr(e);write(dest/'failure.json',result);self.ledger['error']=repr(e);raise
  finally:self.save()
 def save(self):self.ledger['seconds']=time.monotonic()-self.start;write(self.out/'ledger.json',self.ledger)

def arm(oracle,task,prefix,mode,seed,proposals=None):
 s=copy.deepcopy(prefix);batch,diag=choices(task,prefix,mode,seed,proposals)
 for k in range(10):
  row=rank(task,s)[0] if batch is None else batch[k];observe(task,s,row,oracle.acquire(task,f'{task}_{seed}_{mode}_{k:02}',row))
 incumbent=min(range(20),key=lambda k:s['labels'][k][0]);return {'state':s,'best':s['labels'][incumbent][0],'incumbent':s['ids'][incumbent],'diagnostics':diag}
def classical():
 verify_freeze();oracle=Oracle('classical',500,900);jobs=[]
 try:
  for task in TASKS:
   spec=TASKS[task];xs=spec['xs']
   for seed in SEEDS:
    s=fresh(task,seed)
    for k in range(10):
     row=xs.index(spec['expert']) if k==0 else xs.index(spec['default']) if k==1 else next(i for i in s['order'] if i not in s['ids']) if k==2 else rank(task,s)[0]
     observe(task,s,row,oracle.acquire(task,f'{task}_{seed}_prefix_{k:02}',row))
    prefix=O/'prefixes'/f'{task}_{seed}.json';write(prefix,s);path=A/'prompts'/f'{task}_{seed}.json';write(path,messages(spec['names'],xs,s,spec['meaning'],'-'))
    jobs.append({'key':f'{task}_{seed}','task':task,'seed':seed,'sampling_seed':131000+seed,'domains':domains(xs),'system_group':task,'split':'prospectively_fixed_two_family_extension','messages_path':str(path.relative_to(ROOT)),'prefix_path':str(prefix.relative_to(ROOT)),'prefix_sha256':sha(prefix)})
    modes=MODES[:];random.Random(131600+seed).shuffle(modes)
    for mode in modes:write(O/'arms'/f'{task}_{seed}_{mode}.json',arm(oracle,task,s,mode,seed))
  write(A/'jobs.json',jobs);paths=[A/'jobs.json']+list((A/'prompts').glob('*.json'))+list((O/'prefixes').glob('*.json'));write(A/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
 finally:oracle.save()
def continuations():
 verify_freeze()
 for n,h in read(A/'inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h
 oracle=Oracle('continuations',148,300)
 try:
  for task in TASKS:
   for seed in SEEDS:
    prefix=read(O/'prefixes'/f'{task}_{seed}.json');scorepath=ROOT/f'results/v131_proposals/scores/{task}_{seed}.json';score=read(scorepath) if scorepath.exists() else {'status':'unattempted'};proposals=score.get('score') if score['status']=='valid' else None
    result=arm(oracle,task,prefix,'llm' if proposals is not None else 'sequential_3nn',seed,proposals);result.update(model_status=score['status'],fallback=proposals is None);write(O/'arms'/f'{task}_{seed}_llm.json',result)
  for k in range(3):oracle.acquire('wavpack',f'wavpack_expert_repeat_{k}',TASKS['wavpack']['xs'].index(TASKS['wavpack']['expert']))
  validation=[]
  # Fresh, separately charged validation; never fed back into B20 search.
  for seed in SEEDS:
   configs={m:read(O/'arms'/f'fftw_{seed}_{m}.json')['incumbent'] for m in ['sequential_3nn','llm']};configs['expert']=TASKS['fftw']['xs'].index(TASKS['fftw']['expert'])
   for block in range(3):
    modes=list(configs);random.Random(131800+seed*10+block).shuffle(modes)
    for mode in modes:
     key=f'fftw_validation_{seed}_{block}_{mode}';value=oracle.acquire('fftw',key,configs[mode]);validation.append({'seed':seed,'block':block,'mode':mode,'row':configs[mode],'key':key,'target':value})
  write(O/'fresh_validation.json',{'scope':'45 separately charged trials after incumbent selection; no optimizer/controller input','records':validation})
 finally:oracle.save()
if __name__=='__main__':
 import sys
 if sys.argv[1:]==['classical']:classical()
 elif sys.argv[1:]==['continuations']:continuations()
 else:raise SystemExit('classical or continuations required; create once')
