"""Clearly post-hoc concentration/preset diagnostic; no new physical or model calls."""
import json,re,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def main():
    summary=read(ROOT/'results/v78_kanzi_analysis/summary.json');grid=read(ROOT/'data/kanzi_domain_v75.json')['grid']
    owner=(ROOT/'.local-runtime/kanzi-v74/source/java/src/main/java/kanzi/app/BlockCompressor.java').read_text()
    assert re.search(r'case 7\s*:\s*return "LZP\+TEXT\+BWT\+LZP&CM";',owner)
    rows=read(ROOT/'results/v78_kanzi_paired/acquisitions.json');from_model=[c for c in summary['cases'] if c['arms']['llm']['incumbent_from_real_model_proposal']]
    ids=[c['arms']['llm']['config_id'] for c in from_model];assert ids==[439]*4
    observed=[r for r in rows if r['config_id']==439];sizes=sorted({r['compressed_bytes'] for r in observed})
    hashes=sorted({read(ROOT/r['path']/'result.json')['compressed_sha256'] for r in observed})
    result={'diagnostic_timing':'post-hoc after V78 outcomes; no policy fit or prospective baseline result',
        'model_derived_incumbents':len(ids),'distinct_model_derived_incumbent_ids':sorted(set(ids)),
        'configuration':grid[439],'owner_preset_match':{'level':7,'transform_entropy':'LZP+TEXT+BWT+LZP&CM','block_size_is_separate':True},
        'observed_trials_at_configuration':len(observed),'observed_distinct_byte_counts':sizes,'observed_distinct_output_hashes':hashes,
        'seed_without_model_improvement':[c['seed'] for c in summary['cases'] if not c['arms']['llm']['incumbent_from_real_model_proposal']],
        'inference':'The observed gains are compatible with a cheap preset-and-block-size strategy; this is not proof of its counterfactual performance or of the model mechanism',
        'not_run':'A prospectively frozen owner-preset baseline on new workloads; no unseen configuration values were filled in',
        'new_model_requests':0,'new_physical_trials':0}
    out=ROOT/'results/v78_preset_diagnostic';out.mkdir(exist_ok=True);(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
