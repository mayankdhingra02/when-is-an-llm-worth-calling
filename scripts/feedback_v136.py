"""Two-proposal feedback/masked interface; no oracle or objective-file imports."""
import json,hashlib,math
from proposal_v127 import ALPHABET,domains,encode
COUNT=2
MAX_OUTPUT=256

def grammar(ds):
 if not ds or any(not d or len(d)>len(ALPHABET) for d in ds):raise ValueError('Invalid feature domains')
 row=' '.join('['+ALPHABET[:len(d)]+']' for d in ds)
 return 'root ::= "[" row "," row "]"\nrow ::= "\\\"" '+row+' "\\\""\n'

def capacity(ds,tokens,prompt_tokens,cap=MAX_OUTPUT,context=4096):
 grammar(ds)
 if type(prompt_tokens) is not int or prompt_tokens<1 or cap!=MAX_OUTPUT:raise ValueError('Bad accounting')
 needed=set('[],"')|set(ALPHABET[:max(map(len,ds))])
 if not needed<=set(tokens):raise ValueError('Missing ASCII construction')
 upper=COUNT*(len(ds)+3)+2
 if upper>cap or prompt_tokens+cap>context:raise ValueError('Representation/context capacity exceeded')
 return {'constructive_token_upper_bound_including_eos':upper,'maximum_output_ascii_bytes':upper-1,'prompt_tokens':prompt_tokens,'cap':cap,'context':context,'required_singletons':sorted(needed)}

def payload(prompt,seed,ds):
 return {'prompt':prompt,'n_predict':MAX_OUTPUT,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.0,'repeat_penalty':1.0,'seed':seed,'grammar':grammar(ds),'stream':False,'cache_prompt':False,'return_tokens':True}
def check_payload(p):
 required={'n_predict':256,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.0,'repeat_penalty':1.0,'stream':False,'cache_prompt':False,'return_tokens':True}
 if any(p.get(k)!=v for k,v in required.items()) or type(p.get('seed')) is not int or not isinstance(p.get('prompt'),str) or not isinstance(p.get('grammar'),str):raise ValueError('Disallowed generation payload')
def payload_key(p):return hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def parse(response,ds):
 if response.get('truncated') is not False or response.get('stop_type')!='eos' or type(response.get('tokens_predicted')) is not int or not 0<response['tokens_predicted']<=MAX_OUTPUT:raise ValueError('Incomplete/unaccounted response')
 try:rows=json.loads(response['content'])
 except (KeyError,ValueError,TypeError) as e:raise ValueError('Malformed response') from e
 if not isinstance(rows,list) or len(rows)!=2 or any(not isinstance(r,str) or len(r)!=len(ds) or any(c not in ALPHABET[:len(d)] for c,d in zip(r,ds)) for r in rows):raise ValueError('Invalid proposal shape/domain')
 if response['content']!=json.dumps(rows,separators=(',',':')):raise ValueError('Noncanonical output')
 return [tuple(d[ALPHABET.index(c)] for c,d in zip(r,ds)) for r in rows]

def messages(names,xs,prefix,state,meaning,direction,mode):
 if mode not in ['feedback','masked'] or direction not in ['-','+'] or len(prefix['ids'])!=10 or len(state['ids']) not in [10,12,14,16,18]:raise ValueError('Decision stage contract')
 if state['ids'][:10]!=prefix['ids'] or state['labels'][:10]!=prefix['labels'] or len(state['labels'])!=len(state['ids']) or len(set(state['ids']))!=len(state['ids']):raise ValueError('Shared-prefix/isolation contract')
 ds=domains(xs)
 def example(i,y,reveal):
  if reveal and (len(y)!=1 or not math.isfinite(y[0]) or y[0]<=0):raise ValueError('Invalid acquired target')
  return {'settings':encode(xs[i],ds),'performance':f'{y[0]:.6f}' if reveal else None}
 body={'feature_order':list(names),'symbol_to_value':ds,'performance_meaning':meaning,'direction':'minimize' if direction=='-' else 'maximize','initial_observations':[example(i,y,True) for i,y in zip(prefix['ids'],prefix['labels'])],'new_evaluations':[example(i,y,mode=='feedback') for i,y in zip(state['ids'][10:],state['labels'][10:])],'remaining_evaluations':20-len(state['ids'])}
 return [{'role':'system','content':'Optimize software configurations using the acquired measurements shown. Propose two diverse promising configurations. Settings encode each feature by its index in symbol_to_value using 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. A null performance value means the measurement is withheld; do not infer its value. Do not repeat any initial or newly evaluated settings or your own proposals. Feature-distance projection will map proposals to valid unobserved rows. Output only a JSON array of two setting strings.'},{'role':'user','content':json.dumps(body,separators=(',',':'))}]

def project(proposals,xs,state):
 if len(proposals)!=2 or len(state['ids']) not in [10,12,14,16,18] or len(set(state['order']))!=len(xs) or set(state['order'])!=set(range(len(xs))):raise ValueError('Projection contract')
 seen=set(state['ids']);rows=[];diag=[];prior=[]
 for p in proposals:
  if len(p)!=len(xs[0]):raise ValueError('Wrong width')
  row=min([i for i in state['order'] if i not in seen],key=lambda i:sum(a!=b for a,b in zip(p,xs[i])))
  diag.append({'proposal':list(p),'row_id':row,'hamming_distance':sum(a!=b for a,b in zip(p,xs[row])),'repeated_proposal':tuple(p) in prior,'matches_acquired':any(tuple(p)==tuple(xs[i]) for i in state['ids'])});rows.append(row);seen.add(row);prior.append(tuple(p))
 return rows,diag
