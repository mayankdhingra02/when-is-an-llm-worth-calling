"""Pin a bounded set of primary-owner artifact inventories; execute no upstream code."""
import hashlib
import json
from pathlib import Path
from download_guard import fetch

ROOT = Path(__file__).resolve().parents[1]
REPOS = ['nk2242696/compression-codec-benchmark', 'nschorgh/PDS-Throughput', 'inikep/lzbench']
OUT = ROOT / 'artifacts/sources/admission_v14'
MANIFEST = ROOT / 'artifacts/study_v14/source_inventory.json'


def get(url, path):
    return path.read_bytes() if path.exists() else fetch(url, path)


def main():
    records = []
    for repo in REPOS:
        folder = OUT / repo.replace('/', '__')
        folder.mkdir(parents=True, exist_ok=True)
        head = json.loads(get(f'https://api.github.com/repos/{repo}/commits/HEAD', folder/'head.json'))
        commit = head['sha']
        tree_path = folder/'tree.json'
        tree = json.loads(get(f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1', tree_path))
        if tree.get('truncated'):
            raise ValueError('Incomplete owner inventory')
        files = []
        for item in tree['tree']:
            p = item['path']
            if item['type'] != 'blob' or '/' in p or not p.lower().startswith(('readme', 'license')):
                continue
            if item.get('size', 0) > 200000:
                raise ValueError('Unexpected metadata size')
            target = folder/p
            url = f'https://raw.githubusercontent.com/{repo}/{commit}/{p}'
            data = get(url, target)
            blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert blob == item['sha'], p
            files.append({'upstream_path': p, 'path': str(target.relative_to(ROOT)), 'url': url,
                          'git_blob_sha1': blob, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
        records.append({'repo': repo, 'commit': commit, 'tree_path': str(tree_path.relative_to(ROOT)),
                        'tree_sha256': hashlib.sha256(tree_path.read_bytes()).hexdigest(), 'files': files})
        MANIFEST.write_text(json.dumps(records, indent=2)+'\n')
        print(repo, commit, 'inventory entries', len(tree['tree']), flush=True)


if __name__ == '__main__':
    main()
