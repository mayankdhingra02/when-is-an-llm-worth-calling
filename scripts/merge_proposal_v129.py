"""Provenance-linked response view; preserves the interrupted charged attempt."""
import json,shutil
from collect_smollm_v47 import ROOT,read,write,sha,append,now
from proposal_v128 import parse
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def main():
    out=ROOT/'results/v129_merged';out.mkdir(exist_ok=False)
    jobs=read(ROOT/'artifacts/study_v128/jobs.json');jm={j['key']:j for j in jobs};responses=[];links=[];starts=[];ledgers=[]
    for stage in [128,129]:
        folder=ROOT/f'results/v{stage}_proposals';rs=lines(folder/'responses.jsonl');ls=read(folder/'ledger.json');ledgers.append(ls)
        if stage==128:
            assert len(rs)==1 and rs[0]['key']=='mongodb_twins_11_normal';parse(rs[0]['response'],jm[rs[0]['key']]['domains'])
        for r in rs:
            responses.append(r);links.append({'key':r['key'],'stage':stage,'source':str((folder/'responses.jsonl').relative_to(ROOT)),'source_sha256':sha(folder/'responses.jsonl')})
        for start in lines(folder/'generation_starts.jsonl'):starts.append({**start,'source_stage':stage})
        for j in jobs:
            p=folder/'preflight'/f"{j['key']}.json"
            if not p.exists():continue
            # The recovery stage's repeated checked template supersedes only the
            # view, never any original raw preflight file.
            dst=out/'preflight'/p.name;dst.parent.mkdir(exist_ok=True);shutil.copyfile(p,dst)
    assert len({r['key'] for r in responses})==len(responses)
    for r in responses:append(out/'responses.jsonl',r)
    for r in starts:append(out/'generation_starts.jsonl',r)
    repeated=sum(r['identity']=='mongodb_twins_23_normal' and r['source_stage']==129 for r in starts)
    combined={k:sum(d[k] for d in ledgers) for k in ['generation_requests','allocated_output_tokens','stage_seconds','startup_seconds','external_spend_usd','http_requests']}
    combined.update(peak_server_rss_bytes=max(d['peak_server_rss_bytes'] for d in ledgers),retries=repeated,
      explicit_recovery_repeats=repeated,automatic_retries=sum(d['retries'] for d in ledgers),server_exit_code=ledgers[-1]['server_exit_code'],
      original_server_exit_code=ledgers[0]['server_exit_code'],original_resource_stop_reason=ledgers[0]['resource_stop_reason'],
      recovery_resource_stop_reason=ledgers[1]['resource_stop_reason'],scope='Two actual model lifecycles; one interrupted request retains unknown usage')
    write(out/'ledger.json',combined);write(out/'cache_links.json',{'at':now(),'links':links,'stage_ledgers':ledgers})
    write(out/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((out/'preflight').glob('*.json'))}})
    print({'responses':len(responses),'charged_attempts':combined['generation_requests'],'explicit_recovery_repeats':repeated})
if __name__=='__main__':main()
