import json,math
from .core import losses,project,recommend
from .io import write,append

PROMPT_VERSION='v1'

def messages(c,s,collisions,error=None,previous=None):
    scores=losses(s.labels,c.directions)
    history=[{'x':list(c.x[s.ids[j]]),'loss':round(float(scores[j]),6)} for j in sorted(range(len(s.ids)),key=lambda j:-scores[j])]
    body={'feature_order':list(c.names),'allowed_values_in_order':c.domains,'objective_names':list(c.objective_names),'objective_directions':list(c.directions),'observed_trajectory_worst_to_best':history,'avoid_already_observed':collisions,'required_output':{'candidates':['one feature array','one feature array']}}
    instruction='Propose exactly two new configurations to minimize loss. Each must be a full array in feature_order, containing ONLY its allowed values. These are binary symbolic settings; do not invent objectives. Return ONLY {"candidates": [[...], [...]]}, no explanation. Use observed patterns and avoid observed configurations. Loss is based only on acquired labels; lower is better.'
    result=[{'role':'system','content':'You optimize software configurations using only supplied observations and legal values.'},{'role':'user','content':instruction+'\n'+json.dumps(body,separators=(',',':'))}]
    if error:result.extend([{'role':'assistant','content':previous or ''},{'role':'user','content':f'Invalid response: {error}. Repair to exactly two full arrays of valid feature values. JSON only.'}])
    return result

def parse(raw,c):
    text=raw.strip()
    if text.startswith('```json\n') and text.endswith('```'):text=text[8:-3].strip()
    elif text.startswith('```\n') and text.endswith('```'):text=text[4:-3].strip()
    obj=json.loads(text)
    if not isinstance(obj,dict) or set(obj)!={'candidates'}:raise ValueError('expected candidates object')
    rows=obj['candidates']
    if not isinstance(rows,list) or len(rows)!=2:raise ValueError('expected exactly two arrays')
    for row in rows:
        if not isinstance(row,list) or len(row)!=len(c.names):raise ValueError(f'each array needs {len(c.names)} values')
        for value,domain in zip(row,c.domains):
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value not in domain:raise ValueError('value outside allowed domain')
    return rows

def continue_llm(c,s,oracle,provider,context,checkpoint):
    events=[];collisions=[];batch=0
    while len(s.ids)<20:
        provider.resources.check();batch+=1;proposals=None;error=None;previous=None;attempts=[]
        for retry in range(provider.cfg['inference']['max_retries_per_request']+1):
            request=provider.request(messages(c,s,collisions,error,previous),{**context,'batch':batch,'retry':retry,'prompt_version':PROMPT_VERSION})
            event={'request_id':request['request_id'],'retry':retry,'valid':False,'error':None}
            try:
                if request['status']!='response':raise ValueError(request.get('error','provider failure'))
                proposals=parse(request['raw_output'],c);event['valid']=True
            except (ValueError,TypeError) as e:error=str(e);previous=request['raw_output'];event['error']=error
            attempts.append(event);append(provider.log.parent/'validation.jsonl',{**context,'batch':batch,**event})
            if proposals is not None:break
        next_collisions=[]
        for j in range(2):
            if proposals is None:
                i=recommend(c,s);ev={'fallback':True,'projected':False,'duplicate':False,'collision':False,'distance':None}
            else:
                i,ev=project(c,s,proposals[j]);ev['fallback']=False
                if ev['collision']:next_collisions.append(list(c.x[ev['nearest_seen']]))
            y=oracle.acquire(i);s.observe(i,y,c.directions)
            ev.update({'row_id':i,'batch':batch,'attempts':attempts if j==0 else []});events.append(ev)
            write(checkpoint,{'context':context,'state':s.record(),'events':events})
        collisions=next_collisions
    return events
