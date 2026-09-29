"""Corrupt isolated temporary copies; never modify measured originals."""
import json,shutil,tempfile
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,sha
from verify_feedback_v136 import verify
def main():
 bundle=ROOT/'output/v136_replay';checks=[]
 with tempfile.TemporaryDirectory(prefix='v136_synthetic_mutations_') as tmp:
  root=Path(tmp)/'replay';shutil.copytree(bundle,root);verify(root,compact=True)
  def trial(name,path,mutate):
   p=root/path;original=p.read_bytes();mutate(p)
   # Deliberately refresh the transport hash, so rejection must be semantic.
   manifest=read(root/'manifest.json');manifest['files'][path]={'sha256':sha(p),'bytes':p.stat().st_size};write(root/'manifest.json',manifest)
   caught=False
   try:verify(root,compact=True)
   except (AssertionError,ValueError,KeyError):caught=True
   finally:p.write_bytes(original)
   assert caught,name;checks.append({'mutation':name,'rejected_after_transport_hash_refresh':caught})
  def change_mean(p):
   d=read(p);d['groups']['sac']['feedback_vs_masked']['mean']+=.123;write(p,d)
  trial('invented aggregate benefit','results/v136_feedback/comparison.json',change_mean)
  def change_budget(p):
   d=read(p);d['new_acquisitions']=199;write(p,d)
  trial('underreported evaluation budget','results/v136_feedback/summary.json',change_budget)
  def change_order(p):
   rows=[json.loads(x) for x in p.read_text().splitlines()];rows[0]['at_unix']=0;p.write_text(''.join(json.dumps(x)+'\n' for x in rows))
  trial('acquisition before selection','results/v136_feedback/acquisitions.jsonl',change_order)
  j=read(root/'artifacts/study_v136/jobs.json')[0];identity=f"{j['key']}_masked_1"
  def leak(p):
   d=read(p);body=json.loads(d['messages'][1]['content']);body['new_evaluations'][0]['performance']='123.000000';d['messages'][1]['content']=json.dumps(body,separators=(',',':'));write(p,d)
  trial('withheld measurement leaked into masked prompt',f'results/v136_feedback/decisions/{identity}.json',leak)
 write(ROOT/'artifacts/study_v136/mutation_checks.json',{'namespace':'synthetic temporary corruption, excluded from research aggregates','checks':checks})
 print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
