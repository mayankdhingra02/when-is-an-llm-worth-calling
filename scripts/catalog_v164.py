"""Explicit eligible-candidate intervention; receives features and acquired labels only."""
import json
from proposal_v128 import payload as numeric_payload, parse as numeric_parse, capacity,check_payload,payload_key
from native_apps_v163 import messages as numeric_messages

def messages(engine,c,s,condition):
 old=numeric_messages(engine,c,s)
 if condition=='numeric':return old
 if condition!='catalog':raise ValueError('Unknown interface')
 body=json.loads(old[1]['content']);body.pop('projection');body.pop('indexed_values');body['observed_examples']=[{'id':f'{i:02d}','settings':c['raw_features'][i],'loss_seconds':v[0]} for i,v in zip(s['ids'],s['labels'])]
 body['eligible_candidates_columns']=['id',*c['names']];body['eligible_candidates']=[[f'{i:02d}',*c['raw_features'][i]] for i in range(64) if i not in s['ids']]
 body['duplicate_resolution']='A repeated ID is projected to the nearest not-yet-selected setting by normalized ordinal-coordinate L1 distance; seeded order breaks ties.'
 return [{'role':'system','content':f'Optimize {engine} configuration from ten acquired outcomes. Return a JSON array of ten two-digit candidate ID strings ordered most promising first. Choose only from the provided eligible candidates, whose feature values are listed. Avoid duplicate proposals and propose diverse promising settings. Only the first seven unseen settings will be measured; three remaining evaluations are reserved for fresh validation of the best observed setting.'},{'role':'user','content':json.dumps(body,separators=(',',':'))}]

def id_grammar(eligible):
 if len(eligible)!=54 or len(set(eligible))!=54 or any(type(i)is not int or not 0<=i<64 for i in eligible):raise ValueError('Invalid eligible set')
 return 'root ::= "[" row '+ ' '.join('\",\" row' for _ in range(9))+' "]"\nrow ::= "\\\"" id "\\\""\nid ::= '+' | '.join(json.dumps(f'{i:02d}') for i in eligible)+'\n'

def make_payload(prompt,j):
 p=numeric_payload(prompt,j['sampling_seed'],j['domains'])
 if j['condition']=='catalog':p['grammar']=id_grammar(j['eligible'])
 return p

def authorize(rt,p,j,tokens,count):
 check_payload(p)
 expected=make_payload(p['prompt'],j)
 if p!=expected:raise ValueError('Payload not bound to job')
 ds=j['domains'] if j['condition']=='numeric' else [list(range(10)),list(range(10))]
 proof=capacity(ds,tokens,count,p['n_predict']);proof['condition']=j['condition'];proof['eligible_ids']=j['eligible'] if j['condition']=='catalog' else None
 rt.authorized[payload_key(p)]=proof;return proof

def parse(response,j):
 if j['condition']=='numeric':return numeric_parse(response,j['domains'])
 if response.get('truncated') is not False or response.get('stop_type')!='eos' or type(response.get('tokens_predicted'))is not int or not 0<response['tokens_predicted']<=1024:raise ValueError('Incomplete response')
 try:rows=json.loads(response['content'])
 except (KeyError,TypeError,ValueError) as e:raise ValueError('Malformed response') from e
 if not isinstance(rows,list) or len(rows)!=10 or any(not isinstance(x,str) or len(x)!=2 or x not in {f'{i:02d}' for i in j['eligible']} for x in rows):raise ValueError('Invalid candidate IDs')
 if response['content']!=json.dumps(rows,separators=(',',':')):raise ValueError('Noncanonical response')
 return [int(x) for x in rows]
