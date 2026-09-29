"""V176 input-discovery tracer, loaded automatically when this directory is on PYTHONPATH and $TRACE_DIR is set.

Records, per process, every file opened, globbed, listed or executed, plus loaded modules, into $TRACE_DIR/<pid>.json.
Used only to decide which files the audit bundle must contain; it never changes what the traced scripts compute.
"""
import atexit, json, os, sys

_D = os.environ.get('TRACE_DIR')
if _D:
    _rec = {'open': set(), 'glob': set(), 'list': set(), 'exec': set(), 'net': set()}
    def _p(x):
        try: return os.path.abspath(os.fsdecode(x))
        except Exception: return None
    def _hook(ev, args):
        try:
            if ev == 'open' and args and not isinstance(args[0], int):
                p = _p(args[0])
                if p: _rec['open'].add((p, str(args[1] if len(args) > 1 and args[1] is not None else 'r')))
            elif ev.startswith('glob.glob'): _rec['glob'].add(_p(args[0]))
            elif ev in ('os.listdir', 'os.scandir'): _rec['list'].add(_p(args[0] if args and args[0] is not None else '.'))
            elif ev == 'subprocess.Popen': _rec['exec'].add(json.dumps([os.fsdecode(a) for a in (args[1] if isinstance(args[1], (list, tuple)) else [args[1]])]))
            elif ev in ('socket.connect', 'socket.getaddrinfo'): _rec['net'].add(repr(args)[:200])
        except Exception:
            pass
    sys.addaudithook(_hook)
    def _dump():
        out = {'argv': sys.argv, 'cwd': os.getcwd(), 'open': sorted(map(list, _rec['open'])), 'glob': sorted(x for x in _rec['glob'] if x),
               'list': sorted(x for x in _rec['list'] if x), 'exec': sorted(_rec['exec']), 'net': sorted(_rec['net']),
               'modules': sorted({getattr(m, '__file__', None) for m in list(sys.modules.values())} - {None})}
        with open(os.path.join(_D, f'{os.getpid()}.json'), 'w') as f: json.dump(out, f)
    atexit.register(_dump)
