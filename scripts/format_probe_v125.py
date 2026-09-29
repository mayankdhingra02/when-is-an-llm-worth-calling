"""Format-only development probe; no new objective reads or ranking changes."""
import copy,json
from surrogate_v124 import messages as base_messages,payload,check_payload,parse

def messages(prefix,candidate,meaning,condition):
    base=base_messages(prefix,candidate,meaning);body=json.loads(base[1]['content'])
    if condition=='marked_json':
        for o in body['observed_examples']:o['performance']='## '+o['performance']+' ##'
        return [base[0],{'role':'user','content':json.dumps(body,separators=(',',':'))}]
    if condition!='reference_text':raise ValueError('Unknown format condition')
    names=body['feature_order']
    def settings(xs):return ', '.join(f'{k} is {int(v) if float(v).is_integer() else v}' for k,v in zip(names,xs))
    text=f'The following are software configurations and the corresponding performance measured in {meaning}. Your response should only contain the predicted {meaning} in the format ## performance ##.'
    for o in body['observed_examples']:text+='\nHyperparameter configuration: '+settings(o['settings'])+'\nPerformance: ## '+o['performance']+' ##'
    text+='\nHyperparameter configuration: '+settings(body['new_configuration'])+'\nPerformance: '
    return [base[0],{'role':'user','content':text}]
