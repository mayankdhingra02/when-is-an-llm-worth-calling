"""Descriptive cost and timing-noise audit; no changes to primary outcomes."""
from collections import defaultdict,Counter
import json,statistics
from collect_smollm_v47 import ROOT,read,write

def main():
    native=ROOT/'results/v97_native'
    records=[json.loads(s) for s in (native/'acquisitions.jsonl').read_text().splitlines()]
    assert len(records)==250 and (native/'completed.json').exists()
    failures={json.loads(s)['key'] for s in ((native/'failures.jsonl').read_text().splitlines() if (native/'failures.jsonl').exists() else [])}
    families={}
    for family in ['superlu']:
        rs=[r for r in records if r['family']==family]
        spreads=[];groups=defaultdict(list);known_solve_seconds=0.;failed_by_panel=Counter();attempted_by_panel=Counter()
        failure_counts=Counter()
        for r in rs:
            request=read(native/'requests'/f"{r['key']}.json")
            if family=='superlu':
                attempted_by_panel[request['configuration'][3]]+=1
                if r['key'] in failures:failed_by_panel[request['configuration'][3]]+=1
            if r['key'] in failures:failure_counts[r['arm']]+=1
            path=native/'evaluations'/f"{r['key']}.json"
            if not path.exists():continue
            result=read(path)
            times=[m['seconds'] for m in result['measurements']];known_solve_seconds+=sum(times)
            if r['key'] not in failures and result['valid']:
                spreads.append((max(times)-min(times))/statistics.median(times));groups[r['row']].append(r['label'][0])
        repeat_spreads=[(max(v)-min(v))/statistics.median(v) for v in groups.values() if len(v)>=2]
        families[family]={'acquisitions':len(rs),'failure_counts_by_arm':dict(failure_counts),
            'summed_returned_timed_solver_seconds':known_solve_seconds,
            'worker_wall_seconds_sum':sum(r['worker_wall_seconds'] for r in rs),
            'median_within_acquisition_relative_range':statistics.median(spreads),
            'repeated_configurations_across_collection':len(repeat_spreads),
            'median_repeated_configuration_relative_range':statistics.median(repeat_spreads) if repeat_spreads else None,
            'crashes_by_panel_posthoc':dict(failed_by_panel),'attempts_by_panel':dict(attempted_by_panel)}
    write(ROOT/'results/v97_analysis/cost_noise.json',{'scope':'posthoc descriptive noise/cost audit; does not change primary 5% threshold or discard any arm',
        'families':families,'warning':'Ranges are descriptive, sensitive to repeat counts and block order; they are not confidence intervals. Crashes by panel show association, not a causal diagnosis. Returned timing sums omit unreturned solver durations, which remain unknown.'})
    print(json.dumps(families,indent=2))
if __name__=='__main__':main()
