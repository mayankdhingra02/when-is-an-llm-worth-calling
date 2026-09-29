"""Offline verification of the incomplete V75 denominator and observed failure."""
import hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v75 import grid,features,choose
from escalation.kanzi_v74 import parse_header,verify_settings
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def audit():
    for n,d in read(ROOT/'reports/protocol_v75.freeze.json')['sha256'].items():assert sha(ROOT/n)==d,n
    out=ROOT/'results/v75_kanzi_classical';summary=read(out/'summary.json');rows=read(out/'acquisitions.json')
    charges=[json.loads(s) for s in (out/'charges.jsonl').read_text().splitlines()]
    assert summary['intended_physical_evaluations']==200 and summary['charged_evaluations']==len(rows)==len(charges)==9
    assert summary['successful_evaluations']==8 and summary['unattempted']==191 and summary['complete'] is False
    assert not summary['cases'] and not list(out.glob('prefix_*.json'))
    configs=grid();x=features(configs);initial=random.Random(11).sample(range(448),4);obs=[]
    for i,row in enumerate(rows):
        assert row['event_id']==i and row['seed']==11 and row['arm']=='prefix' and row['ordinal']==i+1 and row['purpose']=='search'
        assert all(row[k]==v for k,v in charges[i].items() if k!='status')
        cid=initial[i] if i<4 else choose(x,obs,'nn',11);assert row['config_id']==cid and row['config']==configs[cid]
        folder=ROOT/row['path'];assert row==read(folder/'result.json')
        if i<8:
            assert row['status']=='valid' and row['exact_byte_equality']
            assert row['input_sha256']==row['decoded_sha256']==sha(ROOT/'data/generated_v74/workload.bin')
            assert row['decoded_bytes']==16777216
            for phase in ['compression','decompression']:assert row[phase]['exit_code']==0 and row[phase]['termination_reason'] is None
            header=parse_header(bytes.fromhex(row['header_hex']));verify_settings(header,row['config'],(folder/'compression.log').read_text())
            assert header==row['stream_header'];assert not (folder/'output.knz').exists() and not (folder/'decoded.bin').exists()
            obs.append({'config_id':cid,'compressed_bytes':row['compressed_bytes'],'event_id':i})
        else:
            assert row['status']=='failed' and row['compression']['exit_code']==13 and row['compression']['termination_reason'] is None
            assert 'decompression' not in row and not (folder/'decompression.log').exists()
            assert 'Invalid length: 2479880 (must be in [1..2163456])' in (folder/'compression.log').read_text()
            assert (folder/'output.knz').exists()
    return {'intended_trials':200,'charged_trials':9,'valid_trials':8,'failed_trials':1,'unattempted_trials':191,
        'completed_prefixes':0,'completed_continuation_arms':0,'model_requests':0,'application_processes':17,
        'stage_seconds':summary['seconds'],'failing_config':rows[-1]['config'],'exit_code':13,
        'error_block_1_based':49,'requested_bits':2479880,'available_bits':2163456,
        'requested_bytes':309985,'available_bytes':270432,
        'source_diagnosis':'Inferred stale buffer reference: CustomByteArrayOutputStream may grow inherited buf while final emission reads this.data.array; no stack trace or controlled fix experiment yet',
        'source_diagnosis_confirmed_experimentally':False,
        'partial_output_sha256':sha(ROOT/rows[-1]['path']/'output.knz'),
        'valid_observations':[{'event_id':r['event_id'],'config_id':r['config_id'],'compressed_bytes':r['compressed_bytes']} for r in rows[:-1]],
        'interpretation':'Incomplete acquisition/validity result only; no policy comparison, router, or certified domain'}
if __name__=='__main__':
    result=audit();p=ROOT/'results/v75_failure_audit';p.mkdir(exist_ok=True)
    (p/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
