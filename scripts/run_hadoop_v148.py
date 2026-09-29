"""Finite sequential orchestrator: a failed classical stage cannot start inference."""
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    for command in [['scripts/hadoop_v148.py','prefixes'],['scripts/hadoop_v148.py','classical'],['scripts/collect_models_v148.py'],['scripts/hadoop_v148.py','evaluate']]:
        subprocess.run([sys.executable,*command],cwd=ROOT,check=True,timeout=1750)
if __name__=='__main__':main()
