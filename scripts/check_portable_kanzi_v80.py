"""Validate an isolated ZIP extraction and targeted synthetic corruptions."""
import hashlib,json,shutil,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def main():
    art=ROOT/'artifacts/reproduction_v80';art.mkdir(exist_ok=False)
    extracted=art/'extracted';extracted.mkdir()
    with zipfile.ZipFile(ROOT/'output/kanzi_v80_outcome_reconstruction.zip') as z:
        for name in z.namelist():
            p=Path(name);assert not p.is_absolute() and '..' not in p.parts
        z.extractall(extracted)
    script=extracted/'scripts/replay_kanzi_v80_portable.py'
    def run(p):return subprocess.run([sys.executable,'-I','-S',str(p)],capture_output=True,text=True,timeout=60,cwd=art)
    result=run(script);(art/'clean_stdout.json').write_text(result.stdout);(art/'clean_stderr.txt').write_text(result.stderr)
    assert result.returncode==0 and json.loads(result.stdout)['verified']
    cases=[('reported_mean','results/v80_kanzi_analysis/summary.json'),('arm_budget','results/v80_kanzi_paired/case_dickens_11.json'),('request_denominator','results/v80_kanzi_paired/ledger.json')];checks=[]
    # Corrupt a copied fixture AND update its checksum so semantic checks, not only hashes, must reject it.
    for label,name in cases:
        fixture=art/'synthetic_corruptions'/label;shutil.copytree(extracted,fixture)
        p=fixture/name;value=read(p)
        if label=='reported_mean':value['mean_seed_median_bytes_by_workload']['dickens']['llm']+=1
        elif label=='arm_budget':value['confirmation']['llm'].pop()
        else:value['generation_requests']+=1
        p.write_text(json.dumps(value,indent=2)+'\n');manifest=read(fixture/'portable_manifest.json');manifest['files'][name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size};(fixture/'portable_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        test=run(fixture/'scripts/replay_kanzi_v80_portable.py');assert test.returncode!=0 and 'AssertionError' in test.stderr
        (art/(label+'_rejection.txt')).write_text(test.stderr);checks.append({'fixture':label,'exit_code':test.returncode,'rejected':True,'label':'synthetic_corruption_not_research_data'})
    receipt={'verified':True,'python':sys.version.split()[0],'clean_isolated_replay_exit_code':result.returncode,'new_model_calls':0,'new_physical_trials':0,'checks':checks,'scope':'Local isolated extraction and standard-library outcome reconstruction, not clean-machine native/model rerun'}
    (art/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
