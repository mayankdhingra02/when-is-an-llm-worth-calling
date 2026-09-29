"""Bounded owner-only source retrieval. Never import or run downloaded code."""
import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/sources/v68'
REPOS = {'knobs': 'PKU-DAIR/KnobsTuningEA', 'ycsb': 'brianfrankcooper/YCSB',
         'benchbase': 'cmu-db/benchbase'}
CAP = 10 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', choices=REPOS)
    parser.add_argument('--ref')
    parser.add_argument('--files', nargs='*', default=[])
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = OUT / 'manifest.json'
    state = json.loads(manifest.read_text()) if manifest.exists() else {'files': {}, 'failures': []}
    started = time.monotonic()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def fetch(url, name):
        path = OUT / name
        if path.exists():
            assert name in state['files']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == state['files'][name]['sha256']
            return path.read_bytes()
        assert time.monotonic() - started < 600
        remaining = CAP - sum(v['bytes'] for v in state['files'].values())
        assert remaining > 0
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'llm-escalation-source-audit/68'})
            with opener.open(req, timeout=60) as response:
                # A cap violation is saved as a failure, never as usable source.
                body = response.read(remaining + 1)
            if len(body) > remaining:
                raise ValueError('stage source byte cap exceeded')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            state['files'][name] = {'url': url, 'bytes': len(body),
                'sha256': hashlib.sha256(body).hexdigest(),
                'retrieved_at_utc': datetime.now(timezone.utc).isoformat()}
            return body
        except Exception as exc:
            state['failures'].append({'url': url, 'error': repr(exc),
                'at_utc': datetime.now(timezone.utc).isoformat()})
            raise
        finally:
            manifest.write_text(json.dumps(state, indent=2) + '\n')

    repo = REPOS[args.repo]
    api = 'https://api.github.com/repos/' + repo
    if args.ref:
        ref = json.loads(fetch(api + '/git/ref/' + args.ref, args.repo + '/ref.json'))
        obj = ref['object']
        if obj['type'] == 'tag':
            obj = json.loads(fetch(api + '/git/tags/' + obj['sha'], args.repo + '/tag.json'))['object']
        assert obj['type'] == 'commit'
        (OUT / args.repo / 'pin.json').write_text(json.dumps({'repo': repo, 'commit': obj['sha']}, indent=2) + '\n')
    pin = json.loads((OUT / args.repo / 'pin.json').read_text())
    sha = pin['commit']
    tree = json.loads(fetch(api + '/git/trees/' + sha + '?recursive=1', args.repo + '/tree.json'))
    assert not tree['truncated']
    known = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    for name in args.files:
        assert name in known, name
        assert '..' not in Path(name).parts
        fetch('https://raw.githubusercontent.com/' + repo + '/' + sha + '/' + name, args.repo + '/source/' + name)
    print(json.dumps({'repo': repo, 'commit': sha, 'tree_blobs': len(known),
        'all_source_bytes': sum(v['bytes'] for v in state['files'].values()),
        'elapsed_seconds': time.monotonic() - started}, indent=2))


if __name__ == '__main__':
    main()
