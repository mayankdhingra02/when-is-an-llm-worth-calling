"""Post-hoc output-capacity proof from pinned GGUF vocabulary, not inference."""
import json,struct,re,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def vocab(path):
 f=path.open('rb')
 def integer(fmt):return struct.unpack('<'+fmt,f.read(struct.calcsize('<'+fmt)))[0]
 def string():
  n=integer('Q');assert n<10000000;return f.read(n).decode('utf8')
 def value(t,keep=False):
  if t==8:return string()
  if t==9:
   subtype,n=integer('I'),integer('Q');assert n<2000000
   if keep:return [value(subtype) for _ in range(n)]
   for _ in range(n):value(subtype)
   return None
  formats={0:'B',1:'b',2:'H',3:'h',4:'I',5:'i',6:'f',7:'?',10:'Q',11:'q',12:'d'}
  return integer(formats[t])
 with f:
  assert f.read(4)==b'GGUF';assert integer('I') in [2,3];integer('Q');n=integer('Q')
  for _ in range(n):
   key=string();typ=integer('I')
   if key=='tokenizer.ggml.tokens':assert typ==9;return value(typ,True)
   value(typ)
 raise ValueError('No vocabulary')
def capacity_bound(tokens,ds):
 alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
 allowed=set('[]", \t\r\nĠĊĉč')|set(alphabet[:max(map(len,ds))])
 possible=[t for t in tokens if t and set(t)<=allowed]
 capacity=max(sum(c in '01' for c in t) for t in possible)
 if capacity<1:raise ValueError('No binary-digit vocabulary token')
 binary_positions=sum(len(d)<=2 for d in ds);required=10*binary_positions;lower=(required+capacity-1)//capacity
 return {'features':len(ds),'binary_or_constant_positions':binary_positions,'required_binary_digits':required,'max_binary_digits_in_any_charset_compatible_vocabulary_token':capacity,'conservative_token_lower_bound':lower,'fixed_cap':512,'provably_exceeds_cap':lower>512}

def main():
 start=time.monotonic();m=json.loads((ROOT/'artifacts/study_v91/model_manifest.json').read_text());tokens=vocab(ROOT/m['path']);jobs=json.loads((ROOT/'artifacts/study_v127/jobs.json').read_text());rows=[]
 for j in jobs:
  if j['condition']!='normal' or j['seed']!=11:continue
  rows.append({'dataset':j['dataset'],**capacity_bound(tokens,j['domains'])})
 result={'scope':'Post-hoc formal lower bound for fixed JSON-symbol output;vocabulary analysis only,not model completion','model_sha256_from_preverified_manifest':m['sha256'],'vocabulary_size':len(tokens),'rows':rows,'new_generation_requests':0,'new_objective_acquisitions':0,'seconds':time.monotonic()-start};dest=ROOT/'artifacts/study_v127/output_capacity.json'
 if '--verify-only' in __import__('sys').argv:
  import hashlib
  h=hashlib.sha256()
  with (ROOT/m['path']).open('rb') as f:
   for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
  assert h.hexdigest()==m['sha256']
  old=json.loads(dest.read_text());assert {k:v for k,v in result.items() if k!='seconds'}=={k:v for k,v in old.items() if k!='seconds'};print('Verified capacity proof against pinned model;no new inference or acquisitions')
 else:dest.write_text(json.dumps(result,indent=2)+'\n');print(rows)
if __name__=='__main__':main()
