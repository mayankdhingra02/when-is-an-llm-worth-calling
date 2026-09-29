"""Sequential bounded phases, check=True prevents inference after failed classical search."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for script,args in [('native_study_v153.py',['prefixes']),('native_study_v153.py',['classical']),('collect_models_v153.py',[]),('native_study_v153.py',['model_search']),('native_study_v153.py',['validate'])]:
 subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)
