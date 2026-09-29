"""V176: discover which files the audit bundle must contain by running its command suite under a file-access tracer.

The suite runs in an APFS copy-on-write clone of the project (outside the project, never the workspace itself), without
model weights, runtimes or native build trees, so a command that needs them fails here rather than silently passing.
Writes artifacts/study_v176/traced_inputs.json. No network, acquisition, model request or download.

    .venv/bin/python scripts/trace_inputs_v176.py --scratch /path/outside/project
"""
import argparse, importlib.metadata as md, json, os, shutil, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reproduce_bundle_v176 import CORE, HOST

ROOT = Path(__file__).resolve().parents[1]
SKIP_TOP = {'models', 'output', '.git', '.venv', '.venv-solvers156', '.local-runtime', '.native-v150', '.native-v160', '.cache', '.scratch-v71', '.claude', '.pytest_cache', '.DS_Store'}
# The only files from runtime/native trees that the bundle carries. The three executables are never run by any bundle
# command; the verifiers only hash them against their recorded pins. The corpus is text input (PSF licence).
ALLOWED_HIDDEN = ['.local-runtime/llama-b11146/llama-server', '.local-runtime/llama-b11146/LICENSE',
                  '.native-v160/ripgrep-15.2.0-aarch64-apple-darwin/rg', '.native-v160/ripgrep-15.2.0-aarch64-apple-darwin/COPYING',
                  '.native-v160/ripgrep-15.2.0-aarch64-apple-darwin/LICENSE-MIT', '.native-v160/ripgrep-15.2.0-aarch64-apple-darwin/UNLICENSE',
                  '.native-v160/bin/hnsw_worker_v161', '.native-v160/hnswlib-0.8.0/LICENSE', '.native-v160/Python-3.10.13/LICENSE', '.native-v160/search_corpus']

def clone(dst):
    dst.mkdir(parents=True)
    for p in sorted(ROOT.iterdir()):
        if p.name in SKIP_TOP: continue
        subprocess.run(['cp', '-cR', str(p), str(dst/p.name)], check=True)
    for n in ALLOWED_HIDDEN:
        (dst/n).parent.mkdir(parents=True, exist_ok=True); subprocess.run(['cp', '-cR', str(ROOT/n), str(dst/n)], check=True)

def distributions(module_files):
    """Map loaded module files to installed distributions via each distribution's RECORD (works on Python 3.10)."""
    owner = {}
    for d in md.distributions():
        for f in d.files or []:
            try: owner[str(Path(d.locate_file(f)).resolve())] = (d.metadata['Name'], d.version)
            except Exception: pass
    return dict(sorted({owner[str(Path(m).resolve())] for m in module_files if str(Path(m).resolve()) in owner}))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scratch', type=Path, required=True); a = ap.parse_args()
    scratch = a.scratch.resolve(); assert ROOT not in scratch.parents and scratch != ROOT
    box = scratch/f'trace_v176_{int(time.time())}'; clone(box/'root'); R = (box/'root').resolve()
    env0 = dict(os.environ, PYTHONPATH=os.pathsep.join(['src', 'scripts/trace_v176']), MPLCONFIGDIR=str(box/'mpl'), PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    commands = []; reads = {}; writes = set(); globs = set(); net = []; modules = set()
    for name, argv, *rest in [(n, v) for n, v, _ in CORE]+[(n, v) for n, v, *_ in HOST]:
        d = box/'traces'/name; d.mkdir(parents=True)
        t = time.time(); p = subprocess.run([sys.executable, *argv], cwd=R, env=dict(env0, TRACE_DIR=str(d)), capture_output=True, text=True, timeout=1800)
        commands.append({'name': name, 'argv': argv, 'returncode': p.returncode, 'seconds': round(time.time()-t, 1), 'stderr_tail': p.stderr[-500:] if p.returncode else ''})
        for f in sorted(d.glob('*.json')):
            x = json.loads(f.read_text()); net += x['net']; modules |= set(x['modules'])
            for path, mode in x['open']:
                q = Path(os.path.realpath(path))
                if R not in q.parents: continue
                rel = str(q.relative_to(R))
                if any(c in mode for c in 'wax+'): writes.add(rel)
                elif q.is_file(): reads.setdefault(rel, {'bytes': q.stat().st_size, 'commands': []})['commands'].append(name)
            for g in x['glob']:
                if g and Path(g).is_absolute() and str(R) in g: globs.add(os.path.relpath(g, R))
    for v in reads.values(): v['commands'] = sorted(set(v['commands']))
    dists = distributions(modules)
    out = {'status': 'V176 input discovery; clone excluded models, runtimes and native build trees', 'python': sys.version.split()[0], 'commands': commands,
           'reads': dict(sorted(reads.items())), 'writes': sorted(writes), 'globs': sorted(globs), 'network_events': net, 'distributions': dict(sorted(dists.items()))}
    dest = ROOT/'artifacts/study_v176/traced_inputs.json'; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_text(json.dumps(out, indent=1)+'\n')
    print(json.dumps({'commands_failed': [c['name'] for c in commands if c['returncode']], 'files_read': len(reads), 'bytes_read': sum(v['bytes'] for v in reads.values()),
                      'network_events': len(net), 'distributions': dists, 'clone': str(box)}, indent=1))

if __name__ == '__main__': main()
