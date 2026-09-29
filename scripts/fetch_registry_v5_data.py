"""Fetch owner data/feature-model files only; never execute upstream code."""
import json,hashlib
from pathlib import Path
from download_guard import fetch
root=Path(__file__).resolve().parents[1];records=[]
for m in json.loads((root/'artifacts/registry_v5/metadata.json').read_text()):
    repo=m['repo'];commit=m['commit'];tree=json.loads((root/m['tree_path']).read_text())
    for item in tree['tree']:
        p=item['path'];wanted=False
        if repo=='DeepPerf/DeepPerf':wanted=p.startswith('Data/') and p.endswith('_AllNumeric.csv')
        elif repo=='anonymous12138/multiobj':wanted=p.startswith('Data/') and p.endswith('.csv')
        elif repo=='ChristianKaltenecker/PerformanceEvolution_Website':
            wanted=p.startswith('PerformanceEvolution_Data/') and (p.endswith(('/measurements.csv','/FeatureModel.xml','/README.md','/WorkloadDescriptions.txt')))
        if not wanted:continue
        target=root/'data/registry_raw_v5'/repo.replace('/','__')/p
        url=f'https://raw.githubusercontent.com/{repo}/{commit}/{p}'
        data=target.read_bytes() if target.exists() else fetch(url,target)
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==item['sha'],p
        records.append({'repo':repo,'commit':commit,'upstream_path':p,'path':str(target.relative_to(root)),
                        'url':url,'git_blob_sha1':blob,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
        print(repo,p,len(data),'verified',flush=True)
(root/'artifacts/registry_v5/sources.json').write_text(json.dumps(records,indent=2)+'\n')
