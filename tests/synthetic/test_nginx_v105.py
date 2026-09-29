"""Synthetic protocol validation, not native measurements."""
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('nginx',ROOT/'scripts/native_nginx_v105.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
@pytest.mark.parametrize('header',[
 b'HTTP/1.1 500 Error\r\nContent-Length: 32768\r\n\r\n',
 b'HTTP/1.1 200 OK\r\nContent-Length: 32767\r\n\r\n',
 b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nContent-Length: 32768\r\n\r\n',
 b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nTransfer-Encoding: chunked\r\n\r\n',
 b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nContent-Encoding: gzip\r\n\r\n',
 b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\nConnection: close\r\n\r\n',
])
def test_rejects_invalid_http(header):
    with pytest.raises(ValueError):m.validate_header(header,32768)
def test_equal_length_wrong_body_rejected():
    with pytest.raises(ValueError):m.validate_body(b'X'*len(m.PAYLOAD))
def test_valid_response():
    m.validate_header(b'HTTP/1.1 200 OK\r\nContent-Length: 32768\r\n\r\n',32768)
    m.validate_body(m.PAYLOAD)
def test_service_is_loopback_and_same_payload_contract(tmp_path):
    for case in m.CASES:
        text=m.config_text(case,tmp_path)
        assert 'listen 127.0.0.1:18595;' in text
        assert 'daemon off;' in text
    assert len(m.CASES)==6 and m.CONCURRENCY*m.PER_CLIENT==8192
