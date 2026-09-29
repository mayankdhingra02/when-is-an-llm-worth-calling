"""Read-only bounded collection progress; no target selection or analysis."""
import collections,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'results/v59_workload_physical'
rows=[];partial=False
if (p/'trials.jsonl').exists():
    lines=(p/'trials.jsonl').read_text().splitlines()
    for i,line in enumerate(lines):
        try:rows.append(json.loads(line))
        except json.JSONDecodeError:
            if i!=len(lines)-1:raise
            partial=True
summary={'completed':len(rows),'intended':576,'statuses':dict(collections.Counter(r['status'] for r in rows)),
         'completed_by_workload':dict(collections.Counter(r['family']+'/'+r['workload'] for r in rows)),
         'last_completed_trial':rows[-1]['trial'] if rows else None,'partial_tail':partial,
         'terminal_summary_exists':(p/'summary.json').exists(),
         'minutes_since_first_start':round((time.time()-rows[0]['started_at_unix'])/60,2) if rows else None}
print(json.dumps(summary,indent=2))
