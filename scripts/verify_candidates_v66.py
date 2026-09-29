"""Independent output, frozen input and trial-denominator verification."""
import hashlib,json,re,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def reference_answers():
    n=2**22;answer=[]
    for group in range(256):
        count=(n-1-group)//256+1
        total=sum(((group+256*k)%97)*(((group+256*(k%16))%17)+1) for k in range(count))
        answer.append([group,total,count])
    return answer

def pgm(path):
    data=path.read_bytes()
    # Separate implementation for the retained owner decoder's P5 output.
    match=re.match(rb'P5[ \t\r\n]+(?:#[^\n]*\n[ \t\r\n]*)?(\d+)[ \t\r\n]+(\d+)[ \t\r\n]+255(?:\r\n|[ \t\r\n])',data)
    assert match is not None,'Invalid PGM header'
    w,h=map(int,match.groups());pixels=data[match.end():]
    assert len(pixels)==w*h
    return w,h,pixels

def check_row(row,folder,answers,sort_hash):
    spec=read(folder/'spec.json');assert all(row[k]==v for k,v in spec.items())
    result=read(folder/'result.json');assert all(row[k]==v for k,v in result.items())
    receipt=read(folder/'supervision.json');assert row['supervision']==receipt
    assert row['status']=='valid' and receipt['exit_code']==0 and receipt['termination_reason'] is None
    assert receipt['sampled_maxima']['rss_bytes']<=1024**3
    assert 0<row['objective_ms']/1000<=row['worker_seconds']<=receipt['wall_seconds']<=45
    family=row['family'];c=row['configuration']
    if family=='duckdb':
        assert read(folder/'answer.json')==answers and row['answer_sha256']==sha(folder/'answer.json')
        assert row['version']==[['v1.3.2','0b83e5d2f6','Ossivalis']]
        settings=dict(row['settings']);assert settings['threads']==str(c[0]) and settings['perfect_ht_threshold']==str(c[2])
        displayed=re.fullmatch(r'([0-9.]+) MiB',settings['memory_limit']);assert displayed
        # DuckDB's human-readable display loses precision below one tenth MiB.
        assert abs(float(displayed[1])*2**20-int(c[1][:-2])*10**6)<=.101*2**20
        assert all(settings[k]=='false' for k in ['enable_external_access','autoload_known_extensions','autoinstall_known_extensions','preserve_insertion_order'])
    elif family=='gnu_sort':
        assert sha(folder/'sorted.txt')==row['answer_sha256']==sort_hash
        assert [f'--parallel={c[0]}',f'--buffer-size={c[1]}',f'--batch-size={c[2]}']==row['command'][1:4]
        assert math.isclose(row['objective_ms'],1000*row['execution']['wall_seconds'])
    else:
        assert family=='openjpeg'
        w,h,pixels=pgm(folder/'decoded.pgm')
        expected=bytes(((x*13+y*7)^((x//32+y//32)*11))%256 for y in range(1024) for x in range(1024))
        assert (w,h)==(1024,1024) and pixels==expected
        assert hashlib.sha256(pixels).hexdigest()==row['decoded_pixels_sha256']
        assert (folder/'encoded.j2k').stat().st_size==row['compressed_bytes']
        assert row['command'][-10:]==['-r','1','-b',f'{c[0]},{c[0]}','-n',str(c[1]),'-t',f'{c[2]},{c[2]}','-threads',str(c[3])]
        assert math.isclose(row['objective_ms'],1000*row['execution']['wall_seconds'])
        assert row['validation_execution']['exit_code']==0 and row['program_invocations']==2
    return row['program_invocations']

def main():
    started=time.monotonic()
    for name,digest in read(ROOT/'reports/protocol_v66_admission.freeze.json')['sha256'].items():assert sha(ROOT/name)==digest,name
    out=ROOT/'results/v66_candidate_feasibility';rows=read(out/'all_cases.json');schedule=read(ROOT/'artifacts/study_v66/schedule.json')
    assert len(rows)==len(schedule)==9
    assert rows==[json.loads(x) for x in (out/'trials.jsonl').read_text().splitlines()]
    answers=reference_answers();sort_hash=hashlib.sha256(b''.join(('%08d\n'%i).encode() for i in range(2**20))).hexdigest()
    invocations=0
    for spec,row in zip(schedule,rows):
        assert all(row[k]==v for k,v in spec.items())
        invocations+=check_row(row,out/f"trial_{row['trial']:02d}",answers,sort_hash)
    summary=read(out/'summary.json');assert summary['valid_trials']==summary['attempted_trials']==9 and summary['stage_seconds']<=600
    assert summary['admitted_groups']==['duckdb','gnu_sort','openjpeg']
    print(json.dumps({'verified':True,'configuration_trials':9,'application_invocations_including_decoder_validation':invocations,'model_requests':0,'seconds':time.monotonic()-started},indent=2))
if __name__=='__main__':main()
