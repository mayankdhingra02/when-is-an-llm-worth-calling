"""Create a deterministic local review ZIP; no downloads, inference or publication."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ['src', 'scripts', 'tests', 'reports', 'configs', 'results', 'artifacts']
SUFFIXES = {'.py', '.md', '.txt', '.json', '.jsonl', '.csv', '.yaml', '.sha256', '.log', '.png', '.svg', '.pdf'}
ROOT_FILES = ['AGENTS.md', 'RESEARCH_BRIEF.md', 'SOURCES.md', 'README.md', 'REPRODUCE.md',
              'STATUS.md', 'THIRD_PARTY.md', 'requirements.lock.txt', 'pyproject.toml', '.gitignore', 'BUNDLE_README.md']
LICENSES = ['artifacts/sources/moot_LICENSE.md', 'artifacts/sources/ezr_LICENSE.md',
            'artifacts/sources/registry_v5/anonymous12138__multiobj/LICENSE',
            'artifacts/sources/registry_v5/se-sic__SPLConqueror/LICENSE.md',
            'artifacts/sources/registry_v5/ChristianKaltenecker__PerformanceEvolution_Website/LICENSE',
            'artifacts/sources/live_v15/cpython/LICENSE']


def selected():
    paths = set(ROOT_FILES + LICENSES + ['output/pdf/llm_escalation_review.pdf'])
    paths.update(str(p.relative_to(ROOT)) for p in (ROOT / 'data').glob('*.json'))
    for directory in DIRECTORIES:
        for path in (ROOT / directory).rglob('*'):
            name = path.relative_to(ROOT).as_posix()
            if (not path.is_file() or path.is_symlink() or '__pycache__' in path.parts
                or path.suffix not in SUFFIXES or name.startswith('artifacts/sources/')
                or name.startswith('artifacts/review_delivery/')
                or name == 'artifacts/registry_v4/promisetune_README.md'):
                continue
            paths.add(name)
    return sorted(paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'output/llm_escalation_review_bundle.zip')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Preserve archive; choose a new output path')
    files = {name: (ROOT / name).read_bytes() for name in selected()}
    files['licenses/Qwen2.5-0.5B-Instruct_LICENSE'] = (ROOT / 'models/Qwen2.5-0.5B-Instruct/LICENSE').read_bytes()
    omitted = {}
    for path in sorted((ROOT / 'reports').glob('*.freeze.json')):
        for name, expected in json.loads(path.read_text())['sha256'].items():
            if name not in files:
                entry = omitted.setdefault(name, {'sha256': expected, 'referenced_by': []})
                if entry['sha256'] != expected:
                    raise ValueError(f'Conflicting frozen input digest: {name}')
                entry['referenced_by'].append(path.relative_to(ROOT).as_posix())
    files['OMITTED_FROZEN_INPUTS.json'] = (json.dumps({'scope': 'Inputs needed by scientific freezes but omitted from this review bundle',
        'restoration': 'Use source/data/model manifests and REPRODUCE.md; do not execute experiments without a new bounded allowance',
        'files': omitted}, indent=2) + '\n').encode()
    manifest = {'scope': 'Local review subset, not a self-contained experiment reproduction or authenticity signature',
                'excluded_categories': ['virtual environment and dependency binaries', 'model weights/tokenizer files (license retained)',
                                        'downloaded source datasets/papers (selected license texts retained)',
                                        'physical compressed payloads and source workload', 'Git metadata, caches, lockfiles',
                                        'review-delivery QA receipts and archive files'],
                'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in sorted(files.items())}}
    files['BUNDLE_MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output, 'x', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo('llm-escalation-review/' + name, date_time=(2026, 9, 24, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    print(json.dumps({'archive': str(args.output), 'archive_bytes': args.output.stat().st_size,
                      'archive_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'included_files': len(manifest['files']), 'omitted_frozen_paths': len(omitted)}, indent=2))


if __name__ == '__main__':
    main()
