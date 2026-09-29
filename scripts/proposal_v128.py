"""Capacity-checked bounded representation; no objective oracle imports."""
import hashlib,json
from proposal_v127 import ALPHABET,domains,encode,messages,project,random_proposals
MAX_OUTPUT=1024
COUNT=10

def grammar(ds):
    if not ds or any(not d or len(d)>len(ALPHABET) for d in ds):
        raise ValueError('Invalid feature domains')
    row=' '.join('['+ALPHABET[:len(d)]+']' for d in ds)
    return 'root ::= "[" row '+ ' '.join('\",\" row' for _ in range(COUNT-1))+' "]"\nrow ::= "\\\"" '+row+' "\\\""\n'

def capacity(ds,tokens,prompt_tokens,cap=MAX_OUTPUT,context=4096):
    grammar(ds)
    if type(prompt_tokens) is not int or prompt_tokens<1 or type(cap) is not int or cap<1:
        raise ValueError('Missing token accounting')
    needed=set('[],"')|set(ALPHABET[:max(map(len,ds))])
    if not needed<=set(tokens):raise ValueError('Pinned vocabulary lacks ASCII singleton construction')
    # Ten width-w quoted strings, nine commas, two brackets. No whitespace loops.
    # Singleton ASCII vocabulary pieces construct every legal output in at most
    # this many tokens. One further token is reserved for EOS. This is a format
    # capacity certificate, not a promise of correct/useful model behavior.
    maximum_bytes=COUNT*(len(ds)+3)+1
    upper=maximum_bytes+1
    if upper>cap:raise ValueError('Output representation exceeds conservative capacity')
    if prompt_tokens+cap>context:raise ValueError('Input plus reserved output exceeds context')
    return {'maximum_output_ascii_bytes':maximum_bytes,'constructive_token_upper_bound_including_eos':upper,
            'cap':cap,'prompt_tokens':prompt_tokens,'context':context,'required_singletons':sorted(needed),
            'scope':'Structural format capacity only; not a validity or quality guarantee'}

def payload(prompt,seed,ds):
    return {'prompt':prompt,'n_predict':MAX_OUTPUT,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.0,
            'repeat_penalty':1.0,'seed':seed,'grammar':grammar(ds),'stream':False,'cache_prompt':False,'return_tokens':True}

def check_payload(p):
    if p.get('n_predict')!=MAX_OUTPUT or p.get('temperature')!=.7 or p.get('top_p')!=.95 or p.get('top_k')!=0 or p.get('min_p')!=0 or p.get('repeat_penalty')!=1 or p.get('stream') is not False or p.get('cache_prompt') is not False or p.get('return_tokens') is not True or type(p.get('seed')) is not int or not isinstance(p.get('prompt'),str) or not isinstance(p.get('grammar'),str):
        raise ValueError('Disallowed generation payload')

def payload_key(p):return hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def parse(response,ds):
    if response.get('truncated') is not False or response.get('stop_type')!='eos' or type(response.get('tokens_predicted')) is not int or not 0<response['tokens_predicted']<=MAX_OUTPUT:
        raise ValueError('Incomplete or unaccounted completion')
    try:rows=json.loads(response['content'])
    except (ValueError,TypeError,KeyError) as e:raise ValueError('Malformed JSON') from e
    if not isinstance(rows,list) or len(rows)!=COUNT or any(not isinstance(r,str) or len(r)!=len(ds) or any(c not in ALPHABET[:len(d)] for c,d in zip(r,ds)) for r in rows):
        raise ValueError('Bad proposal format')
    if response['content']!=json.dumps(rows,separators=(',',':')):raise ValueError('Noncanonical grammar output')
    return [tuple(d[ALPHABET.index(c)] for c,d in zip(r,ds)) for r in rows]
