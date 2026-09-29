"""Read-only receipt replay plus regenerable descriptive tables/figure; no trials."""
import csv,hashlib,json,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.kanzi_v74 import generated_workload,parse_header,verify_settings,byte_equal,REFERENCE,CONTRAST

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def analyze():
    for name,digest in json.loads((ROOT/'reports/protocol_v74.freeze.json').read_text())['sha256'].items():
        assert sha(ROOT/name)==digest,name
    data=ROOT/'data/generated_v74/workload.bin'
    assert data.read_bytes()==generated_workload()
    out=ROOT/'results/v74_kanzi_feasibility';summary=json.loads((out/'summary.json').read_text())
    charges=[json.loads(s) for s in (out/'charges.jsonl').read_text().splitlines()]
    assert summary['intended_trials']==3 and summary['charged_trials']==len(charges)==len(summary['trials'])
    records=[]
    for i,row in enumerate(summary['trials']):
        folder=out/f'trial_{i}';config=[REFERENCE,CONTRAST,REFERENCE][i]
        assert row['trial']==charges[i]['trial']==i and row['config']==charges[i]['config']==config
        assert row==json.loads((folder/'result.json').read_text())
        assert row['status']=='valid' and row['exact_byte_equality']
        for phase in ['compression','decompression']:
            assert row[phase]['exit_code']==0 and row[phase]['termination_reason'] is None
            assert row[phase]['wall_seconds']<=120
            assert row[phase]['sampled_maxima']['rss_bytes']<=2*1024**3
            assert row[phase]['sampled_maxima']['scratch_bytes']<=128*1024**2
        with (folder/'output.knz').open('rb') as f:header=parse_header(f.read(16))
        assert header==row['stream_header'];verify_settings(header,config,(folder/'compression.log').read_text())
        assert byte_equal(data,folder/'decoded.bin')
        assert sha(data)==row['input_sha256']==row['decoded_sha256']==sha(folder/'decoded.bin')
        assert sha(folder/'output.knz')==row['compressed_sha256']
        assert (folder/'output.knz').stat().st_size==row['compressed_bytes']
        records.append({'trial':i,'setting':'contrast' if i==1 else 'reference',
            'compression_seconds':row['compression_process_seconds'],'decompression_seconds':row['decompression_process_seconds'],
            'compressed_bytes':row['compressed_bytes'],'compressed_input_ratio':row['compression_ratio'],
            'peak_sampled_rss_bytes':max(row[p]['sampled_maxima']['rss_bytes'] for p in ['compression','decompression'])})
    assert summary['complete'] and summary['valid_trials']==3 and not summary['stop_reason'] and summary['seconds']<=600
    return records,summary

def main():
    records,summary=analyze();out=ROOT/'results/v74_kanzi_analysis';out.mkdir(exist_ok=True)
    with (out/'trials.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    result={'verified_trials':len(records),'stage_seconds':summary['seconds'],'records':records,
        'reference_compressed_bytes_identical':records[0]['compressed_bytes']==records[2]['compressed_bytes'],
        'interpretation':'correctness/resource feasibility only; artificial input; no optimizer or LLM benefit measured'}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    cache=ROOT/'.cache/kanzi-v74-plot';cache.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR',str(cache));os.environ.setdefault('XDG_CACHE_HOME',str(cache))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(9,3.5),layout='constrained')
    labels=['Reference 1','Contrast','Reference 2'];x=list(range(3))
    axes[0].bar(x,[r['compression_seconds'] for r in records],label='Compression',color='#326b9e')
    axes[0].bar(x,[r['decompression_seconds'] for r in records],bottom=[r['compression_seconds'] for r in records],label='Decompression',color='#dc9145')
    axes[0].set_ylabel('Process wall seconds');axes[0].legend(fontsize=8)
    axes[1].bar(x,[r['compressed_bytes']/1024**2 for r in records],color='#326b9e');axes[1].set_ylabel('Compressed MiB (input: 16 MiB)')
    for ax in axes:ax.set_xticks(x,labels);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Kanzi feasibility: three real trials on generated input\nAll outputs byte-exact; no optimization or LLM inference',fontsize=11)
    fig.savefig(out/'feasibility.png',dpi=160);fig.savefig(out/'feasibility.svg');plt.close(fig)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
