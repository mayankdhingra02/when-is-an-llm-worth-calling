"""Build matched diagnostic prompts using ONLY previously saved acquired messages."""
import copy,hashlib,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/study_v48'
ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
IDS=ALPHABET[:20]
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def decode(x,domains):
    if len(x)!=len(domains):raise ValueError('Feature width')
    return [d[ALPHABET.index(c)] for c,d in zip(x,domains)]
def transform(messages,pool,representation,loss_mode,presentation):
    body=json.loads(messages[1]['content'].split('\n',1)[1]);body=copy.deepcopy(body)
    mapping=dict(pool['mapping'])
    if presentation=='reverse':body['candidates'].reverse()
    elif presentation=='relabel':
        renaming={c:IDS[(i+10)%20] for i,c in enumerate(IDS)}
        mapping={renaming[k]:v for k,v in mapping.items()}
        for row in body['candidates']:row['id']=renaming[row['id']]
    elif presentation!='base':raise ValueError('Presentation')
    original_losses=[r['loss'] for r in body['observations']]
    if loss_mode=='withheld':
        for row in body['observations']:del row['loss']
    elif loss_mode!='observed':raise ValueError('Loss mode')
    header=messages[1]['content'].split('\n',1)[0]
    if loss_mode=='withheld':header='Observed configurations are shown, but their losses are withheld. '+header.replace('Observed losses are normalized using only acquired labels. ','')
    if representation=='symbols':content=header+'\n'+json.dumps(body,separators=(',',':'))
    elif representation=='values':
        header=('Observed losses are normalized using only acquired labels.' if loss_mode=='observed' else 'Observed configurations are shown, but their losses are withheld.')
        header+=' The table shows actual numeric configuration settings under feature names. Select ten distinct promising candidate IDs, one per line. Smaller observed loss is better. Candidate IDs are arbitrary.\n'
        content=header+'feature_order='+json.dumps(body['feature_order'],separators=(',',':'))+'\nOBSERVATIONS\n'
        for r in body['observations']:
            content+='settings='+json.dumps(decode(r['x'],body['symbol_to_value']),separators=(',',':'))
            if loss_mode=='observed':content+=' loss='+json.dumps(r['loss'])
            content+='\n'
        content+='CANDIDATES\n'
        for r in body['candidates']:
            content+=r['id']+' settings='+json.dumps(decode(r['x'],body['symbol_to_value']),separators=(',',':'))+'\n'
    else:raise ValueError('Representation')
    return [{'role':'system','content':messages[0]['content']},{'role':'user','content':content}],mapping,[r['id'] for r in body['candidates']],original_losses
def main():
    cfg=read(ROOT/'configs/study_v48.json')
    if (OUT/'jobs.json').exists():raise ValueError('Preserve prepared prompts')
    manifest=read(ROOT/'data/manifest_v8.json')
    training=set(read(ROOT/'results/v6/router_seal.json')['benefit']['training_groups'])
    if set(cfg['development_groups'])!=training:raise ValueError('Nondevelopment group')
    historical=[json.loads(s) for s in (ROOT/'results/v8/requests.jsonl').read_text().splitlines()]
    jobs=[];inputs=['data/manifest_v8.json','results/v6/router_seal.json','results/v8/requests.jsonl','configs/study_v48.json','reports/protocol_v48_sensitivity.md']
    for spec in manifest['datasets']:
        for seed in cfg['seeds']:
            case=next(c for c in manifest['cases'] if c['dataset']==spec['id'] and c['seed']==seed)
            request=next(r for r in historical if r['dataset']==spec['id'] and r['seed']==seed)
            base=f"{spec['id']}_{seed}";prefix=read(ROOT/f'results/v6/prefixes/{base}.json')
            assert request['prefix_hash']==case['prefix_hash']==prefix['prefix_hash']
            assert len(prefix['state']['ids'])==10
            inputs.append(f'results/v6/prefixes/{base}.json')
            for rep in ('symbols','values'):
                for labels in ('observed','withheld'):
                    for order in ('base','reverse','relabel'):
                        messages,mapping,presentation,losses=transform(request['messages'],case['pool'],rep,labels,order)
                        key=f'{base}_{rep}_{labels}_{order}';path=OUT/'prompts'/f'{key}.json'
                        record={'messages':messages,'prefix_hash':case['prefix_hash'],'mapping':mapping,'presentation':presentation,
                            'base_case':base,'representation':rep,'loss_mode':labels,'presentation_mode':order,'namespace':'real_model_development_diagnostic_v48',
                            'source_prefix':f'results/v6/prefixes/{base}.json','source_pool':case['pool'],'original_acquired_losses':losses}
                        write(path,record);inputs.append(str(path.relative_to(ROOT)))
                        jobs.append({'key':key,'base_case':base,'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,
                            'representation':rep,'loss_mode':labels,'presentation_mode':order,'prefix':str(path.relative_to(ROOT))})
    random.Random(48000).shuffle(jobs)
    assert len(jobs)==cfg['cases']==108
    write(OUT/'jobs.json',jobs);inputs.append('artifacts/study_v48/jobs.json')
    write(OUT/'input_paths.json',inputs)
    print('Prepared',len(jobs),'conditions from nine development prefixes; no target-table reads')
if __name__=='__main__':main()
