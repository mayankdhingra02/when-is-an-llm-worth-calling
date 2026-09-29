"""Reconstruct a V172 stage summary from persisted files when the collector crashed before writing one (amendment 2)."""
import argparse, json
from collect_smollm_v47 import ROOT, read, write, now
from common_v172 import A, M, STAGES, config, stage_info

def reconstruct(stage):
    out = M/stage; dest = out/'summary.json'; assert not dest.exists(), 'Stage already has a collector-written summary'
    info = stage_info(stage, config()); jobs = [j for j in read(A/'jobs.json') if j['split'] == info['split']]
    starts = [json.loads(l) for l in (out/'generation_starts.jsonl').read_text().splitlines()]
    scores = [read(p) for p in (out/'scores').glob('*.json')]; attempted = [g['identity'] for g in starts if g['kind'] == 'scientific']
    errors = [json.loads(l) for l in (out/'errors.jsonl').read_text().splitlines()] if (out/'errors.jsonl').exists() else []
    s = {'at': now(), 'reconstructed_after_collector_crash': True, 'reconstruction_basis': ['generation_starts.jsonl', 'responses.jsonl', 'scores/', 'errors.jsonl', 'ledger.json (last persisted before final request)'],
         'stage': stage, 'arm': info['arm'], 'model_key': info['model_key'], 'intended': len(jobs), 'attempted': len(attempted), 'responses': len(scores),
         'valid': sum(x['status'] == 'valid' for x in scores), 'invalid': sum(x['status'] == 'invalid' for x in scores),
         'unattempted': [j['qualified_key'] for j in jobs if j['qualified_key'] not in attempted],
         'attempted_without_response': [k for k in attempted if k not in {x['qualified_key'] for x in scores}],
         'error': '; '.join(e['error'] for e in errors)+'; collector close() then raised PermissionError(1) from os.killpg on the exiting server group, so no summary was written',
         'seconds': None, 'ledger': {**read(out/'ledger.json'), 'resource_stop_reason': 'unrecorded (in-memory only; lost when close() raised)', 'server_exit_code': 'unrecorded', 'stage_seconds': None}}
    write(dest, s); return s

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=list(STAGES)); print(json.dumps(reconstruct(ap.parse_args().stage), indent=1))

if __name__ == '__main__': main()
