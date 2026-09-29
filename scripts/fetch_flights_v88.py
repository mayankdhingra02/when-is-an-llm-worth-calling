"""Fetch registry data archive and inspect it as data, never install its code."""
import json,tarfile
from pathlib import Path
import fetch_duckdb_v87 as bounded
ROOT=Path(__file__).resolve().parents[1];bounded.OUT=ROOT/'artifacts/sources/v88';bounded.CAP=16*1024**2

def main():
    meta=json.loads(bounded.fetch('https://pypi.org/pypi/nycflights13/0.0.3/json','pypi.json').read_text());assert meta['info']['version']=='0.0.3' and meta['info']['license']=='CC0'
    items=[i for i in meta['urls'] if i['filename']=='nycflights13-0.0.3.tar.gz'];assert len(items)==1;i=items[0]
    path=bounded.fetch(i['url'],i['filename'],12*1024**2);assert bounded.sha(path)==i['digests']['sha256']=='d9ef2f5cf1bebca7e30b4daf69dcd7a8fd71f25b7196f5dc489879ad7e3e8a37'
    with tarfile.open(path,'r:gz') as t:
        members=[{'name':m.name,'size':m.size,'regular':m.isfile()} for m in t.getmembers()]
    (ROOT/'artifacts/study_v88/archive_inventory.json').write_text(json.dumps(members,indent=2)+'\n');print(json.dumps(members,indent=2))
if __name__=='__main__':main()
