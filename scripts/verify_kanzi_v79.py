"""Read-only full replay plus independently check exact input/setting commands."""
import json
from analyze_kanzi_v79 import ROOT,read,verify

def main():
    result=verify();assert result==read(ROOT/'results/v79_kanzi_analysis/summary.json')
    workloads={w['name']:w for w in read(ROOT/'artifacts/study_v79/workloads.json')['files']}
    lock=read(ROOT/'configs/runtime_v76.lock.json')
    base=[str(ROOT/lock['java']),'-Xmx768m','-XX:ActiveProcessorCount=4','-jar',str(ROOT/lock['jar'])]
    events=read(ROOT/'results/v79_kanzi_classical/acquisitions.json')
    for event in events:
        folder=ROOT/event['path'];c=event['config'];source=ROOT/workloads[event['workload']]['path']
        commands=read(folder/'commands.json')
        assert commands=={'compression':base+['-c','-i',str(source),'-o',str(folder/'output.knz'),'-x','-t',c['transform'],'-e',c['entropy'],'-b',str(c['block_bytes']),'-j','1','-v','3'],
            'decompression':base+['-d','-i',str(folder/'output.knz'),'-o',str(folder/'decoded.bin'),'-j','1','-v','3']},event['event_id']
    print(json.dumps({'verified':True,'physical_trials':len(events),'exact_commands_checked':len(events)*2,'replayed_policy_cases':len(result['cases']),'logical_arm_charges':result['logical_arm_charges'],'new_model_requests':0}))
if __name__=='__main__':main()
