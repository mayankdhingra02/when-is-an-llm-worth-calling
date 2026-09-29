"""V178 offline bootstrap: install the network guard in this process, prove it works, then run the command.

    python scripts/guarded_run_v178.py scripts/some_script.py [args...]
    python scripts/guarded_run_v178.py -m pytest [args...]
    python scripts/guarded_run_v178.py --selftest

V176/V177 relied on Python importing scripts/guard_v176/sitecustomize.py automatically. A host whose own
sitecustomize is found first silently skips that guard, and an independent audit hit exactly that. This bootstrap does
not depend on start-up module search order. It installs an audit hook directly, then attempts a loopback connection
and a host lookup. Both must raise the guard's own error before the target runs; otherwise it exits with status 3.

The guard covers this Python process. Child processes the target starts are not guarded; each launch is appended to
the file named by $GUARD_CHILD_LOG so the runner can report them.
"""
import json, os, runpy, socket, sys

GUARD_ERROR = 'offline guard'

def _hook(event, args):
    if event == 'socket.connect':
        addr = args[1] if len(args) > 1 else None
        if isinstance(addr, tuple):
            raise RuntimeError(f'{GUARD_ERROR}: network connection blocked ({addr!r})')
    elif event in ('socket.getaddrinfo', 'socket.gethostbyname', 'socket.gethostbyaddr'):
        raise RuntimeError(f'{GUARD_ERROR}: host lookup blocked ({args[0]!r})')
    elif event == 'subprocess.Popen' and os.environ.get('GUARD_CHILD_LOG'):
        try:
            argv = args[1] if isinstance(args[1], (list, tuple)) else [args[1]]
            with open(os.environ['GUARD_CHILD_LOG'], 'a') as f: f.write(json.dumps([os.fsdecode(a) for a in argv])+'\n')
        except Exception:
            pass

def install():
    sys.addaudithook(_hook)

def verify():
    """Return None if both probes are blocked by this guard, else a description of what got through."""
    probes = {'connect': lambda: socket.create_connection(('127.0.0.1', 9), timeout=1), 'lookup': lambda: socket.getaddrinfo('example.invalid', 443)}
    for name, probe in probes.items():
        try:
            s = probe()
        except RuntimeError as e:
            if GUARD_ERROR in str(e): continue
            return f'{name}: unexpected {e!r}'
        except Exception as e:
            return f'{name}: reached the network stack ({type(e).__name__}: {e})'
        try: s.close()
        except Exception: pass
        return f'{name}: succeeded'
    return None

def main(argv):
    install(); problem = verify()
    if problem:
        sys.stderr.write(f'offline guard NOT active, refusing to run: {problem}\n'); sys.exit(3)
    if argv[:1] == ['--selftest']:
        print(json.dumps({'guard_active': True, 'python': sys.version.split()[0]})); return
    if not argv: sys.exit('usage: guarded_run_v178.py SCRIPT [args] | -m MODULE [args] | --selftest')
    if argv[0] == '-m':
        sys.argv = [argv[1], *argv[2:]]; sys.path.insert(0, os.getcwd())
        runpy.run_module(argv[1], run_name='__main__', alter_sys=True)
    else:
        path = os.path.abspath(argv[0]); sys.argv = [argv[0], *argv[1:]]; sys.path.insert(0, os.path.dirname(path))
        runpy.run_path(path, run_name='__main__')

if __name__ == '__main__': main(sys.argv[1:])
