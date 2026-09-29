"""Finite sequential collector; reuse provenance-bound prefixes, all new costs charged."""
import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v164';O=ROOT/'results/v164_native'
def main():
 from collect_smollm_v47 import read,write
 from native_apps_v164 import guard
 guard();O.mkdir(exist_ok=False);start=time.monotonic();write(O/'ledger.json',{'acquisitions':0,'start_unix':time.time(),'intended':900,'reused_historical_prefix_outcomes':100});completed=[];error=None
 try:
  for argv in [['native_apps_v164.py','classical'],['collect_models_v164.py'],['native_apps_v164.py','model_search'],['native_apps_v164.py','validate']]:
   if time.monotonic()-start>1740:raise TimeoutError('1800s driver cap')
   subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts'/argv[0]),*argv[1:]],cwd=ROOT,check=True,timeout=1800-(time.monotonic()-start));completed.append(argv)
 except Exception as e:error=repr(e)
 finally:write(A/'driver_receipt.json',{'seconds':time.monotonic()-start,'completed':completed,'error':error})
 if error:raise RuntimeError(error)
if __name__=='__main__':main()
