"""Freeze V172 inputs, code and pins before any model start. Create-once."""
import json
from collect_smollm_v47 import ROOT, read, write, sha, now
import audit_v171
A = ROOT/'artifacts/study_v172'
CODE = ['scripts/'+n for n in ['common_v172.py', 'runtime_v172.py', 'collect_models_v172.py', 'evaluate_v172.py', 'analyze_v172.py', 'verify_v172.py', 'prepare_v172.py', 'fetch_qwen_v172.py',
        'freeze_v172.py', 'audit_v171.py', 'runtime_models_v148.py', 'proposal_v128.py', 'proposal_v127.py', 'spark_v144.py', 'spark_v145.py', 'hadoop_v148.py', 'analyze_pointwise_v123.py',
        'audit_output_capacity_v127.py', 'process_rss_v129.py', 'collect_smollm_v47.py', 'router_v132.py', 'router_v147.py']]+\
       ['src/escalation/'+n for n in ['core.py', 'transfer_v41.py', 'receipts_v70.py']]+['tests/synthetic/test_v172.py', 'tests/synthetic/test_audit_v171.py']
DOCS = ['reports/protocol_v172.md', 'reports/proposal_v172.md', 'configs/proposal_v172.json', 'configs/study_v172.json', 'artifacts/study_v171/freeze.json',
        'artifacts/study_v172/authorization.json', 'artifacts/study_v172/model_manifest.json', 'artifacts/study_v172/downloads.json', 'artifacts/study_v172/models.json',
        'artifacts/study_v172/jobs.json', 'artifacts/sources/v172/LICENSE', 'artifacts/sources/v172/README.md', 'artifacts/sources/v172/model.pointer', 'data/manifest_v41.json']

def main():
    dest = A/'freeze.json'; assert not dest.exists()
    manifest = read(A/'model_manifest.json'); old = read(ROOT/'artifacts/study_v148/models.json')['qwen3_8b']
    assert sha(ROOT/manifest['path']) == manifest['sha256'] and (ROOT/manifest['path']).stat().st_size == manifest['bytes']
    write(A/'models.json', {'qwen3_14b': {'path': manifest['path'], 'sha256': manifest['sha256'], 'repo': manifest['model_repo'], 'revision': manifest['revision'], 'license': 'Apache-2.0',
                                          'provenance': 'artifacts/study_v172/model_manifest.json', 'bytes': manifest['bytes']}, 'qwen3_8b': old})
    jobs = read(A/'jobs.json'); files = set(CODE+DOCS)
    for j in jobs:
        files.update([j['messages_path'], j['prefix'], j['historical_qwen3_8b_preflight']])
        if j['origin'] == 'v141': files.add(next(s['path'] for s in read(ROOT/'data/manifest_v41.json')['datasets'] if s['id'] == j['dataset']))
        else: files.add(('artifacts/study_v144' if j['origin'] == 'v144' else 'artifacts/study_v148')+f"/candidates/{j['app']}.json")
    files.update(audit_v171.INPUTS.values())
    files.update(str(p.relative_to(ROOT)) for p in (ROOT/'.local-runtime/llama-b11146').rglob('*') if p.is_file())
    write(dest, {'at': now(), 'purpose': 'V172 inputs, code, pins and protocol frozen before any model start or recorded acquisition',
                 'model_weights_verified_at_each_start_via': 'artifacts/study_v172/models.json', 'sha256': {n: sha(ROOT/n) for n in sorted(files)}})
    print(len(files), 'files frozen')

if __name__ == '__main__': main()
