"""Prepare existing development messages without changing their contents."""
import json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    out=ROOT/'artifacts/study_v93';out.mkdir(exist_ok=True)
    assert not (out/'jobs.json').exists()
    old=json.loads((ROOT/'artifacts/study_v48/jobs.json').read_text())
    jobs=[]
    for j in old:
        if j['representation']!='symbols':continue
        for mode in ['native']+(['forced'] if (j['loss_mode'],j['presentation_mode'])==('observed','base') else []):
            jobs.append({**j,'source_key':j['key'],'key':j['key']+'_'+mode,'decoder':mode})
    random.Random(49000).shuffle(jobs)
    assert len(jobs)==63 and sum(j['decoder']=='native' for j in jobs)==54
    assert {j['system_group'] for j in jobs}=={'mysql_family','brotli','lrzip'}
    (out/'jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
    print('Prepared 54 native cases + nine forced controls; unchanged V48 symbol messages.')
if __name__=='__main__':main()
