"""Outcome-blind admission plus comprehensive recursive local-result exposure audit."""
import hashlib, json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
from escalation.io import read, write, digest, now
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import restrict, SEEDS

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    if Path('data/manifest_v41.json').exists(): raise ValueError('Preserve admission')
    registry = read('data/registry_v5.json')
    selection = [
        ('BDBC_AllNumeric', 'berkeleydb', '-', 'I/O time', {}),
        ('Dune_AllNumeric', 'dune_hsmgp', '-', 'Poisson solving time', {'cells': 50.0}),
        ('LLVM_AllNumeric', 'llvm', '-', 'Compiler optimization time', {}),
        ('hipacc_AllNumeric', 'hipacc', '-', 'PDE benchmark execution time', {}),
        ('sac_AllNumeric', 'sac', '-', 'n-body simulation execution time', {}),
        ('OpenVPN', 'openvpn', '+', 'iperf3 TCP throughput in Mbits/s', {}),
    ]
    aliases = {}
    for d in registry['datasets']:
        if d['system_group']:
            for key in (d['dataset_id'], d['dataset_id'].split('/')[-1], d['system_group']): aliases[key.lower()] = d['system_group']
    exposed, scanned, hits, metadata_only = set(), {}, [], {}
    def visit(obj, path):
        if isinstance(obj, dict):
            for key in ('system_group', 'dataset', 'dataset_id', 'system'):
                value = obj.get(key)
                if isinstance(value, str) and value.lower() in aliases:
                    group = aliases[value.lower()]; exposed.add(group)
                    if group in {s[1] for s in selection}: hits.append({'file': str(path), 'key': key, 'value': value})
            for value in obj.values(): visit(value, path)
        elif isinstance(obj, list):
            for value in obj: visit(value, path)
    for path in sorted(Path('results').rglob('*')):
        if path.suffix not in ('.json', '.jsonl') or 'source_snapshot' in path.parts: continue
        scanned[str(path)] = sha(path)
        if str(path) in ('results/v13_admission/summary.json', 'results/v13_1_admission/summary.json'):
            d = read(path)
            if d['scope'] != 'metadata-only task admission, not an optimization experiment' or d['new_model_requests'] != 0 or d['new_objective_acquisitions'] != 0:
                raise ValueError('Previously reviewed metadata-only artifact changed')
            metadata_only[str(path)] = {'sha256': scanned[str(path)], 'reason': 'Reviewed explicit zero-acquisition metadata-only admission; no performance scores'}
            continue
        if path.suffix == '.jsonl':
            for line in path.read_text().splitlines():
                if line.strip(): visit(json.loads(line), path)
        else: visit(read(path), path)
    write('artifacts/study_v41/exposure_audit.json', {'at': now(), 'scanned': scanned, 'exposed_groups': sorted(exposed),
          'candidate_hits': hits, 'metadata_only_exceptions': metadata_only,
          'qualification': 'Local structured outcome/request records, including nested JSON. Public pretraining exposure cannot be excluded.'})
    if hits: raise ValueError('Candidate appears in prior result records; inspect before admission')
    evidence = {s['path']: s['sha256'] for s in read('artifacts/study_v41/sources.json')}
    for name in ('artifacts/sources/registry_v5/papers/hsmgp_study.pdf', 'artifacts/registry_v5/sources.json'):
        evidence[name] = sha(name)
    specs = []
    for name, group, direction, meaning, fixed in selection:
        d = next(d for d in registry['datasets'] if d['dataset_id'].split('/')[-1] == name)
        s = d['schema']
        spec = dict(id=name, system_group=group, path=d['path'], sha256=d['sha256'], url=d['url'],
            delimiter=';' if name == 'OpenVPN' else ',', feature_names=s['feature_names'],
            objective_columns=s['objective_names'], primary_objective=s['objective_names'][0],
            metadata_columns=s['metadata_columns'], filters=s['row_filters'], rows=s['unique_configurations'],
            duplicates=s['duplicates'], direction=direction, meaning=meaning, fixed_features=fixed,
            split='prospective_test', evidence=evidence,
            license='No source code reused. DeepPerf data-specific redistribution grant unresolved; local analysis only. PerformanceEvolution owner GPL-2.0; source payloads remain ignored.',
            limitation='Recorded benchmark target only; equal functional utility/correctness and per-row noise not verified.')
        if name == 'OpenVPN':
            doc = str(Path(d['path']).parent/'README.md'); spec['evidence'] = {**evidence, doc: sha(doc)}
        c, subset = restrict(load_candidates(spec), fixed)
        spec['subset'] = subset; specs.append(spec)
    write('data/manifest_v41.json', dict(version=41, created=now(), datasets=specs, seeds=SEEDS,
        objective_values_parsed_at_admission=0, historical_exposed_groups=sorted(exposed),
        scope='Six new local-study families; single-target recorded-table adaptation. Not live-system tuning.',
        exclusions={'BDBJ': 'same family as BDBC', 'HSMGP': 'same conservative family as Dune',
                    'JavaGC': '612-level feature exceeds existing 62-symbol encoding',
                    'VEER/MOOT additions': 'defer unresolved semantics/lineage; no outcome-based selection'}))
    print(json.dumps([{'id': s['id'], 'group': s['system_group'], 'candidates': s['subset']['selected'], 'direction': s['direction']} for s in specs], indent=2))

if __name__ == '__main__': main()
