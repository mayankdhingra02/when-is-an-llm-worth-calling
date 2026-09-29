"""Finite FLAC task and bounded native oracle; no unacquired outcome table."""
import copy, itertools, json, random, subprocess, time
from fractions import Fraction
from pathlib import Path
from collect_smollm_v47 import ROOT, read, write, sha, now, append
from proposal_v128 import messages, domains, project, random_proposals

A=ROOT/'artifacts/study_v130'
O=ROOT/'results/v130_native'
NAMES=['block_size_samples','maximum_LPC_order','maximum_Rice_partition_order']
XS=list(itertools.product([1024,1536,2048,3072,4096,4608],[4,8,10,12],[0,2,4,6]))
PRESET=XS.index((4096,12,6))
SEEDS=[11,23,37,53,71]
CONTROLS=['sequential_3nn','batch_3nn','random_projection','random_full']

def rank(state):
 assert len(state['ids'])>=3
 seen=set(state['ids']);result=[]
 for row in state['order']:
  if row in seen:continue
  near=sorted(range(len(state['ids'])),key=lambda k:sum(a!=b for a,b in zip(XS[row],XS[state['ids'][k]])))[:3]
  result.append((sum(Fraction(state['labels'][k][0]) for k in near)/3,row))
 return [r for _,r in sorted(result,key=lambda x:x[0])]

def state(seed):
 order=list(range(len(XS)));random.Random(seed).shuffle(order)
 return {'ids':[],'labels':[],'order':order}

def observe(s,row,target):
 if len(s['ids'])>=20:raise ValueError('B20 exceeded')
 if type(row) is not int or row not in range(len(XS)) or row in s['ids']:raise ValueError('Invalid/duplicate acquisition')
 if type(target) is not int or target<=0:raise ValueError('Invalid positive byte target')
 s['ids'].append(row);s['labels'].append([target])

def branch_choices(prefix,mode,seed,proposals=None):
 if len(prefix['ids'])!=10:raise ValueError('Expected B10 prefix')
 if mode=='sequential_3nn':return None,[]
 if mode=='batch_3nn':return rank(prefix)[:10],[]
 if mode=='random_projection':return project(random_proposals(domains(XS),130900+seed),XS,prefix)
 if mode=='random_full':return random.Random(130400+seed).sample([i for i in prefix['order'] if i not in prefix['ids']],10),[]
 if mode=='llm':return project(proposals,XS,prefix)
 raise ValueError('Unknown arm')

def verify_freeze():
 for n,h in read(ROOT/'reports/protocol_v130.freeze.json')['sha256'].items():
  if sha(ROOT/n)!=h:raise ValueError('Frozen input changed: '+n)

class Oracle:
 def __init__(self,phase,cap,seconds):
  self.phase=phase;self.cap=cap;self.seconds=seconds;self.started=time.monotonic();self.count=0
  self.build=read(A/'build_xcode.json');self.workloads=read(A/'workloads.json')['workloads'];self.binary=str(ROOT/self.build['binary'])
  if sha(self.binary)!=self.build['sha256']:raise ValueError('Binary identity mismatch')
  for w in self.workloads:
   if sha(ROOT/w['raw_path'])!=w['raw_sha256']:raise ValueError('Workload identity mismatch')
  self.out=O/phase;self.out.mkdir(parents=True,exist_ok=False)
  self.ledger={'phase':phase,'at':now(),'configuration_attempts':0,'completed_configurations':0,'encode_attempts':0,'decode_attempts':0,'max_configurations':cap,'max_seconds':seconds}
 def command(self,cmd,kind):
  remaining=self.seconds-(time.monotonic()-self.started)
  if remaining<=0:raise TimeoutError('Native stage wall cap')
  self.ledger[kind+'_attempts']+=1;write(self.out/'ledger.json',self.ledger)
  t=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=min(10,remaining))
  rec={'command':cmd,'returncode':p.returncode,'seconds':time.monotonic()-t,'stderr':p.stderr.decode(errors='replace')}
  append(self.out/'commands.jsonl',rec)
  if p.returncode:raise RuntimeError('FLAC command failed: '+rec['stderr'])
  return rec
 def acquire(self,key,row):
  if type(row) is not int or row not in range(len(XS)):raise ValueError('Invalid row')
  if self.count>=self.cap:raise ValueError('Native configuration cap')
  if time.monotonic()-self.started>=self.seconds:raise TimeoutError('Native wall cap')
  dest=self.out/key;dest.mkdir(exist_ok=False);self.count+=1
  self.ledger['configuration_attempts']=self.count;write(self.out/'ledger.json',self.ledger)
  append(self.out/'starts.jsonl',{'at':now(),'key':key,'row':row,'settings':XS[row],'attempt':self.count})
  records=[];block,lpc,rice=XS[row]
  try:
   for j,w in enumerate(self.workloads):
    encoded=dest/f'{j}.flac';decoded=dest/f'{j}.raw'
    cmd=[self.binary,'--silent','-V','-8','-b',str(block),'-l',str(lpc),'-r',f'0,{rice}','--no-padding','--no-seektable','--force-raw-format','--endian=little','--sign=signed','--channels=1','--bps=16','--sample-rate=16000','-o',str(encoded),w['raw_path']]
    enc=self.command(cmd,'encode')
    dec=self.command([self.binary,'--silent','-d','--force-raw-format','--endian=little','--sign=signed','-o',str(decoded),str(encoded)],'decode')
    actual=sha(decoded)
    if actual!=w['raw_sha256'] or decoded.stat().st_size!=w['raw_bytes']:raise ValueError('Decoded sample mismatch')
    records.append({'workload':j,'encoded_path':str(encoded.relative_to(ROOT)),'encoded_sha256':sha(encoded),'bytes':encoded.stat().st_size,'decoded_sha256':actual,'decoded_bytes':decoded.stat().st_size,'encode':enc,'decode':dec})
    decoded.unlink() # Owned transient output; sample hash/size and encoded file retained.
   result={'at':now(),'key':key,'row':row,'settings':XS[row],'target_bytes':sum(r['bytes'] for r in records),'workloads':records,'valid':True}
   write(dest/'result.json',result);self.ledger['completed_configurations']+=1;return result['target_bytes']
  except Exception as e:
   write(dest/'failure.json',{'error':repr(e),'completed_workloads':records});self.ledger['error']=repr(e);raise
  finally:self.save()
 def save(self):
  self.ledger['seconds']=time.monotonic()-self.started;write(self.out/'ledger.json',self.ledger)

def continue_arm(oracle,prefix,mode,seed,proposals=None):
 s=copy.deepcopy(prefix);choices,diagnostics=branch_choices(prefix,mode,seed,proposals)
 for k in range(10):
  row=rank(s)[0] if choices is None else choices[k]
  observe(s,row,oracle.acquire(f's{seed}_{mode}_{k:02}',row))
 return {'state':s,'best_bytes':min(y[0] for y in s['labels']),'diagnostics':diagnostics}

def classical():
 verify_freeze();oracle=Oracle('classical',250,900);jobs=[]
 try:
  for seed in SEEDS:
   s=state(seed)
   for k in range(10):
    row=PRESET if k==0 else next(i for i in s['order'] if i not in s['ids']) if k<3 else rank(s)[0]
    observe(s,row,oracle.acquire(f's{seed}_prefix_{k:02}',row))
   write(O/'prefixes'/f'{seed}.json',s)
   prompt=messages(NAMES,XS,s,'Sum of native FLAC file bytes over three fixed 16 kHz mono speech clips, with exact lossless reconstruction. All configurations start from FLAC 1.5.0 preset -8 and override block size, maximum LPC order and maximum Rice partition order (minimum zero); padding/seektable disabled. Smaller is better.','-')
   path=A/'prompts'/f'{seed}.json';write(path,prompt)
   jobs.append({'key':f'flac_{seed}','seed':seed,'sampling_seed':130000+seed,'system_group':'flac','split':'new_family_descriptive_pilot','messages_path':str(path.relative_to(ROOT)),'domains':domains(XS),'prefix_path':str((O/'prefixes'/f'{seed}.json').relative_to(ROOT)),'prefix_sha256':sha(O/'prefixes'/f'{seed}.json')})
   for mode in CONTROLS:write(O/'arms'/f'{seed}_{mode}.json',continue_arm(oracle,s,mode,seed))
  write(A/'jobs.json',jobs)
  files=[A/'jobs.json']+list((A/'prompts').glob('*.json'))+list((O/'prefixes').glob('*.json'))
  write(A/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in files}})
 finally:oracle.save()

def final():
 verify_freeze()
 for n,h in read(A/'inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 oracle=Oracle('continuations',53,300)
 try:
  for seed in SEEDS:
   prefix=read(O/'prefixes'/f'{seed}.json');p=ROOT/f'results/v130_proposals/scores/flac_{seed}.json'
   score=read(p) if p.exists() else {'status':'unattempted'}
   proposals=score['score'] if score['status']=='valid' else None
   if proposals is None:
    result=continue_arm(oracle,prefix,'sequential_3nn',seed);result['model_status']=score['status'];result['fallback']=True
   else:
    result=continue_arm(oracle,prefix,'llm',seed,proposals);result['model_status']='valid';result['fallback']=False
   write(O/'arms'/f'{seed}_llm.json',result)
  repeats=[oracle.acquire(f'preset_repeat_{k}',PRESET) for k in range(3)]
  write(O/'determinism.json',{'kind':'Three separately charged post-selection correctness/size repeat probes, not arm acquisitions or optimization input','row':PRESET,'targets':repeats})
 finally:oracle.save()

if __name__=='__main__':
 import sys
 if sys.argv[1:] == ['classical']:classical()
 elif sys.argv[1:]==['continuations']:final()
 else:raise SystemExit('Select classical or continuations; create once')
