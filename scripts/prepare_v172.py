"""Build the 70 V172 replay jobs from saved V141/V144/V148 jobs; feature-only, no target reads."""
import random
from collect_smollm_v47 import ROOT, read, write, sha
A = ROOT/'artifacts/study_v172'
ORIGINS = [('v141', 'artifacts/study_v141/jobs.json', 'results/v141_models/qwen3_8b/preflight'),
           ('v144', 'artifacts/study_v144/jobs.json', 'results/v145_models/qwen3_8b/preflight'),
           ('v148', 'artifacts/study_v148/jobs.json', 'results/v148_models/qwen3_8b/preflight')]

def build_jobs(cfg):
    jobs = []
    for origin, path, preflight in ORIGINS:
        for j in read(ROOT/path):
            assert sha(ROOT/j['prefix']) == j['prefix_sha256'] and (ROOT/j['messages_path']).exists()
            hist = f"{preflight}/{j['key']}.json"; assert (ROOT/hist).exists()
            job = {'origin': origin, 'key': j['key'], 'qualified_key': j['system_group']+'::'+j['key'], 'system_group': j['system_group'], 'seed': j['seed'],
                   'domains': j['domains'], 'messages_path': j['messages_path'], 'prefix': j['prefix'], 'prefix_sha256': j['prefix_sha256'],
                   'sampling_seed': j['sampling_seed'], 'redraw_seed': j['sampling_seed']+cfg['redraw_seed_offset'], 'historical_qwen3_8b_preflight': hist}
            if origin == 'v141': job.update(dataset=j['dataset'])
            else: job.update(app=j['app'])
            jobs.append(job)
    keys = sorted(j['qualified_key'] for j in jobs); assert len(keys) == len(set(keys)) == 70
    random.Random(cfg['split_permutation_seed']).shuffle(keys); first = set(keys[:cfg['requests_per_stage']])
    for j in jobs: j['split'] = 1 if j['qualified_key'] in first else 2
    order = {k: n for n, k in enumerate(keys)}; jobs.sort(key=lambda j: order[j['qualified_key']])
    return jobs

def main():
    cfg = read(ROOT/'configs/study_v172.json'); dest = A/'jobs.json'; assert not dest.exists()
    jobs = build_jobs(cfg); write(dest, jobs); print(len(jobs), 'jobs;', sum(j['split'] == 1 for j in jobs), 'in split 1')

if __name__ == '__main__': main()
