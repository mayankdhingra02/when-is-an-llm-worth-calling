"""Minimal bounded RESP2 client and deterministic application workload, not LLM output."""
import hashlib
import socket

KEYS=256
FIELDS=128

def value(field):
    return (f'field-{field:03d}-'.encode()+b'x'*64)[:64]

def key(index): return f'v60:{index:012d}'.encode()
def field(index): return f'f{index:03d}'.encode()

def encode(args):
    parts=[a if isinstance(a,bytes) else str(a).encode() for a in args]
    return b'*'+str(len(parts)).encode()+b'\r\n'+b''.join(b'$'+str(len(p)).encode()+b'\r\n'+p+b'\r\n' for p in parts)

def decode(stream, depth=0):
    if depth>4: raise ValueError('RESP nesting limit')
    line=stream.readline(4096)
    if not line.endswith(b'\r\n'): raise ValueError('Truncated or oversized RESP line')
    kind,body=line[:1],line[1:-2]
    if kind==b'+': return body
    if kind==b'-': raise ValueError('Redis error: '+body.decode(errors='replace'))
    if kind==b':': return int(body)
    if kind in (b'$',b'*'):
        n=int(body)
        if n==-1:return None
        if not 0<=n<=1024*1024:raise ValueError('RESP size limit')
        if kind==b'*':return [decode(stream,depth+1) for _ in range(n)]
        data=stream.read(n+2)
        if len(data)!=n+2 or not data.endswith(b'\r\n'):raise ValueError('Truncated RESP payload')
        return data[:-2]
    raise ValueError('Unknown RESP type')

class Client:
    def __init__(self,path):
        self.socket=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.socket.settimeout(3);self.socket.connect(str(path));self.file=self.socket.makefile('rb')
    def call(self,*args):
        self.socket.sendall(encode(args));return decode(self.file)
    def close(self):self.file.close();self.socket.close()

def populate(client):
    assert client.call('DBSIZE')==0
    for i in range(KEYS):
        args=['HSET',key(i)]
        for j in range(FIELDS):args.extend([field(j),value(j)])
        assert client.call(*args)==FIELDS
    assert client.call('DBSIZE')==KEYS

def validate(client):
    assert client.call('DBSIZE')==KEYS
    expected={field(j):value(j) for j in range(FIELDS)};h=hashlib.sha256()
    for i in range(KEYS):
        pairs=client.call('HGETALL',key(i))
        assert isinstance(pairs,list) and len(pairs)==2*FIELDS
        got=dict(zip(pairs[::2],pairs[1::2]));assert got==expected,'Stored payload changed'
        h.update(key(i))
        for k,v in sorted(got.items()):h.update(k);h.update(v)
    return {'keys':KEYS,'fields_per_key':FIELDS,'total_values':KEYS*FIELDS,'sha256':h.hexdigest()}
