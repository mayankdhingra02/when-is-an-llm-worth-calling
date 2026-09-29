"""Finite foreground driver; all children waited and model runtime cleaned up."""
import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v163';start=time.monotonic();error=None;completed=[]
try:
 for argv in [['native_apps_v163.py','prefixes'],['native_apps_v163.py','classical'],['collect_models_v163.py'],['native_apps_v163.py','model_search'],['native_apps_v163.py','validate']]:
  if time.monotonic()-start>1740:raise TimeoutError('1800s driver cap')
  # Each stage has internal caps; driver timeout is a final process guard.
  subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts'/argv[0]),*argv[1:]],cwd=ROOT,check=True,timeout=1800-(time.monotonic()-start));completed.append(argv)
except Exception as e:error=repr(e)
finally:(A/'driver_receipt.json').write_text(json.dumps({'seconds':time.monotonic()-start,'completed':completed,'error':error},indent=2)+'\n')
if error:raise RuntimeError(error)
