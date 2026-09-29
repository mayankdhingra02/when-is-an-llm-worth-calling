"""Synthetic HTTP byte/framing fixtures, excluded from research measurements."""
import subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
CLIENT=ROOT/'.local-runtime/http-client-v107/client'
BODY=bytes(range(256))*128
@pytest.mark.parametrize('header,body,valid',[
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\n\r\n',BODY,True),
 (b'HTTP/1.1 500 Error\r\nContent-Length: 32768\r\n\r\n',BODY,False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32767\r\n\r\n',BODY,False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nContent-Length: 32768\r\n\r\n',BODY,False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nTransfer-Encoding: chunked\r\n\r\n',BODY,False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nContent-Encoding: gzip\r\n\r\n',BODY,False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\n\r\n',b'X'*32768,False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\n\r\n',BODY[:-1],False),
 (b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\n\r\n',BODY+b'X',False),
])
def test_native_parser(tmp_path,header,body,valid):
 p=tmp_path/'response';p.write_bytes(header+body)
 r=subprocess.run([str(CLIENT),'--validate',str(p)],timeout=2)
 assert (r.returncode==0)==valid
@pytest.mark.parametrize('n',['0','65537','-1','bad'])
def test_request_cap(n):
 assert subprocess.run([str(CLIENT),n],timeout=2).returncode==2
