"""Feature-only full-domain proposals. No hidden objective oracle is imported."""
import json,math,random
ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
N_PROPOSALS=10
MAX_OUTPUT=512

def domains(xs):
    if not xs or not xs[0]:raise ValueError('Empty features')
    if len({len(x) for x in xs})!=1:raise ValueError('Ragged features')
    ds=[sorted({x[k] for x in xs}) for k in range(len(xs[0]))]
    if any(len(v)>len(ALPHABET) for v in ds):raise ValueError('Domain alphabet exhausted')
    return ds

def encode(x,ds):return ''.join(ALPHABET[d.index(v)] for v,d in zip(x,ds))

def messages(names,xs,prefix,meaning,direction,condition='normal'):
    if direction not in ['-','+'] or condition not in ['normal','rotated_labels'] or len(prefix['ids'])!=10 or len(prefix['labels'])!=10:raise ValueError('Prefix contract')
    ds=domains(xs);labels=[y[0] for y in prefix['labels']]
    if not all(math.isfinite(y) and y>0 for y in labels):raise ValueError('Bad acquired target')
    if condition=='rotated_labels':labels=labels[1:]+labels[:1]
    body={'feature_order':list(names),'symbol_to_value':ds,'observed_examples':[{'settings':encode(xs[i],ds),'performance':f'{y:.6f}'} for i,y in zip(prefix['ids'],labels)],'performance_meaning':meaning,'direction':'minimize' if direction=='-' else 'maximize'}
    return [{'role':'system','content':'You optimize software configurations from ten acquired measurements. Infer useful settings from their relationship to performance. Propose ten diverse, promising configurations. Each setting string encodes each feature by its index in symbol_to_value using 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. Proposals will be projected by feature distance to valid unobserved configurations. Output only a JSON array of ten setting strings. Do not repeat observed settings or your own proposals.'},{'role':'user','content':json.dumps(body,separators=(',',':'))}]

def grammar(ds):
    row=' '.join('['+ALPHABET[:len(d)]+']' for d in ds)
    # GBNF literal quote surrounds each fixed-width symbol string.
    return 'root ::= "[" ws row '+ ' '.join('"," ws row' for _ in range(9))+' ws "]"\nrow ::= "\\\"" '+row+' "\\\""\nws ::= [ \\t\\n\\r]*\n'

def payload(prompt,seed,ds):
    return {'prompt':prompt,'n_predict':MAX_OUTPUT,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.0,'repeat_penalty':1.0,'seed':seed,'grammar':grammar(ds),'stream':False,'cache_prompt':False,'return_tokens':True}

def check_payload(p):
    if p.get('n_predict')!=MAX_OUTPUT or p.get('temperature')!=.7 or p.get('top_p')!=.95 or p.get('top_k')!=0 or p.get('min_p')!=0 or p.get('repeat_penalty')!=1 or p.get('stream') is not False or p.get('cache_prompt') is not False or type(p.get('seed')) is not int or not isinstance(p.get('prompt'),str) or not isinstance(p.get('grammar'),str) or not p['grammar'].startswith('root ::= '):raise ValueError('Disallowed generation payload')

def parse(response,ds):
    if response.get('truncated') is not False or response.get('stop_type')!='eos' or type(response.get('tokens_predicted')) is not int or not 0<response['tokens_predicted']<=MAX_OUTPUT:raise ValueError('Incomplete or unaccounted completion')
    try:rows=json.loads(response['content'])
    except (ValueError,TypeError,KeyError) as e:raise ValueError('Malformed JSON') from e
    if not isinstance(rows,list) or len(rows)!=N_PROPOSALS:raise ValueError('Ten proposals required')
    if any(not isinstance(r,str) or len(r)!=len(ds) or any(c not in ALPHABET[:len(d)] for c,d in zip(r,ds)) for r in rows):raise ValueError('Bad domain symbol')
    return [tuple(d[ALPHABET.index(c)] for c,d in zip(r,ds)) for r in rows]

def project(proposals,xs,prefix):
    """Hamming nearest eligible row; ties follow frozen feature-only order."""
    order=prefix['order'];seen=set(prefix['ids']);selected=[];diagnostics=[];prior=[]
    if len(set(order))!=len(order) or set(order)!=set(range(len(xs))) or not seen<=set(order):raise ValueError('Bad candidate order')
    if len(proposals)!=10 or len(xs)-len(seen)<10:raise ValueError('Projection budget')
    for x in proposals:
        if len(x)!=len(xs[0]):raise ValueError('Proposal width')
        available=[i for i in order if i not in seen]
        row=min(available,key=lambda i:sum(a!=b for a,b in zip(x,xs[i])))
        distance=sum(a!=b for a,b in zip(x,xs[row]));diagnostics.append({'proposal':list(x),'row_id':row,'hamming_distance':distance,'repeated_proposal':tuple(x) in prior,'matches_initial_observation':any(tuple(x)==tuple(xs[i]) for i in prefix['ids'])})
        selected.append(row);seen.add(row);prior.append(tuple(x))
    return selected,diagnostics

def random_proposals(ds,seed):
    rng=random.Random(seed)
    return [tuple(rng.choice(d) for d in ds) for _ in range(10)]
