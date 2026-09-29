"""V176 offline guard, loaded automatically when this directory is on PYTHONPATH.

Any attempt to open a network connection or resolve a host name raises immediately, so a reproduction run
cannot make API calls. Unix-domain sockets (used by some local libraries) are not affected.
"""
import socket, sys

def _guard(event, args):
    if event == 'socket.connect':
        addr = args[1] if len(args) > 1 else None
        if isinstance(addr, tuple):
            raise RuntimeError(f'offline guard: network connection blocked ({addr!r})')
    elif event in ('socket.getaddrinfo', 'socket.gethostbyname', 'socket.gethostbyaddr'):
        raise RuntimeError(f'offline guard: host lookup blocked ({args[0]!r})')

sys.addaudithook(_guard)
