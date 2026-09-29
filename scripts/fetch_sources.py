"""Retrieve small primary artifacts from pinned owner repositories; no execution."""
import json, pathlib, hashlib
from download_guard import fetch
root=pathlib.Path(__file__).resolve().parents[1]
for name,paths in {'moot':['README.md','LICENSE.md','CITATION.cff','optimize/config/README.md','optimize/config/Apache_AllMeasurements.csv','optimize/config/SQL_AllMeasurements.csv','optimize/config/X264_AllMeasurements.csv'], 'ezr':['ezr.py','cli.py','LICENSE.md','pyproject.toml']}.items():
 sha={'moot':'90803be51b00f881305db45aa0cf6a3b5340804f','ezr':'bfda80b3b797d142378f7fb8746c3485610fb17e'}[name]
 (root/'artifacts/sources').mkdir(parents=True,exist_ok=True)
 (root/'data/raw').mkdir(parents=True,exist_ok=True)
 for path in paths:
  url=f'https://raw.githubusercontent.com/timm/{name}/{sha}/{path}'
  target=root/('data/raw/'+path.split('/')[-1] if path.endswith('.csv') else f'artifacts/sources/{name}_'+path.replace('/','_'))
  manifest_path=root/'data/manifest.json'
  known=json.loads(manifest_path.read_text())['datasets'] if manifest_path.exists() else []
  expected=next((d['sha256'] for d in known if d['path']==str(target.relative_to(root))),None)
  data=fetch(url,target,expected=expected)
  print(target.relative_to(root),len(data),hashlib.sha256(data).hexdigest())
