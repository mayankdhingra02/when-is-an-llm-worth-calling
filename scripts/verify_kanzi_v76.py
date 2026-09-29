"""Offline replay of controlled diagnosis with retained binary products."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v74 import byte_equal,parse_header,verify_settings,REFERENCE
from run_kanzi_v76 import FAIL

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
    for n,d in json.loads((ROOT/'reports/protocol_v76.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==d,n
    out=ROOT/'results/v76_kanzi_diagnosis';s=json.loads((out/'summary.json').read_text());assert s['complete_diagnosis'] and s['charged_trials']==s['intended_trials']==3 and s['seconds']<400
    charges=[json.loads(x) for x in (out/'charges.jsonl').read_text().splitlines()];assert len(charges)==3
    lock=json.loads((ROOT/'configs/runtime_v76.lock.json').read_text())
    for i,row in enumerate(s['trials']):
        folder=out/f'trial_{i}';assert row==json.loads((folder/'result.json').read_text())
        assert charges[i]['trial']==i and charges[i]['config']==row['config']==(FAIL if i<2 else REFERENCE)
        command=json.loads((folder/'commands.json').read_text())
        assert str(ROOT/lock['original_jar']) in command['decompression']
        assert str(ROOT/lock['original_jar'] if i==0 else ROOT/lock['jar']) in command['compression']
        if i==0:
            assert row['status']=='application_failure' and row['expected_failure_reproduced'] and row['compression']['exit_code']==13
            assert 'Invalid length: 2479880 (must be in [1..2163456])' in (folder/'compression.log').read_text()
            assert not (folder/'decoded.bin').exists()
        else:
            assert row['status']=='valid' and row['exact_byte_equality']
            assert byte_equal(ROOT/'data/generated_v74/workload.bin',folder/'decoded.bin')
            assert sha(folder/'decoded.bin')==row['decoded_sha256'] and sha(folder/'output.knz')==row['compressed_sha256']
            assert (folder/'output.knz').stat().st_size==row['compressed_bytes']
            with (folder/'output.knz').open('rb') as f:header=parse_header(f.read(16))
            assert header==row['stream_header'];verify_settings(header,row['config'],(folder/'compression.log').read_text())
            for phase in ['compression','decompression']:
                assert row[phase]['exit_code']==0 and row[phase]['termination_reason'] is None and row[phase]['wall_seconds']<=40
    assert s['trials'][2]['compressed_sha256']=='290dc8a9522ffed814f88d9fc8bc5edc2a8e3d21c9904b185821464500861dd6'
    return {'verified':True,'physical_trials':3,'application_failures':1,'valid_trials':2,'expected_failure_reproduced':True,'original_decoder_recovered_patched_stream':True,'reference_hash_unchanged':True,'stage_seconds':s['seconds'],'application_processes':5,'claim':'Narrow controlled evidence for buffer repair, not universal correctness or LLM benefit'}
if __name__=='__main__':
    result=verify();p=ROOT/'artifacts/study_v76/verification.json';p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
