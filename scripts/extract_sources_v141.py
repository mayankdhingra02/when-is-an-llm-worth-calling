"""Retain only already acquired source lines for offline review."""
from collect_smollm_v47 import ROOT,read,write,sha
def main():
 a=ROOT/'artifacts/study_v141';out=ROOT/'results/v141_analysis';s=read(out/'summary.json');assert s['complete'];by={}
 for key in s['arms']:
  r=read(out/'arms'/f'{key}.json');g=r['system_group'];c=read(a/'candidates'/f'{g}.json');spec=c['spec'];record=by.setdefault(g,{'spec':spec,'rows':set()});states=[r['state']]+[read(ROOT/v['path'])['state'] for v in r['references'].values()]
  for state in states:record['rows'].update(c['source_ids'][i] for i in state['ids'])
 for g,r in by.items():
  sp=r['spec'];assert sha(ROOT/sp['path'])==sp['sha256'];lines=(ROOT/sp['path']).read_text().splitlines();used=r['rows']|{1};write(a/'source_extracts'/f'{g}.json',{'source_path':sp['path'],'source_sha256':sp['sha256'],'scope':'Only source lines already acquired by preserved model/prefix/control arms','lines':{str(i):lines[i-1] for i in sorted(used)}})
if __name__=='__main__':main()
