import pytest
from escalation.kanzi_v74 import parse_header,verify_settings,REFERENCE,byte_equal

def header(checksum=1,codec=1):
    parts=[(0x4B414E5A,32),(1,4),(checksum,1),(codec,5),((3<<42)|(5<<36),48),(65536,28),(16,6),(0,4)]
    n=0
    for v,b in parts:n=(n<<b)|v
    return n.to_bytes(16,'big')

def log():
    return 'Block size set to 1048576 bytes\nChecksum set to true\nUsing LZ+RLT transform (stage 1)\nUsing HUFFMAN entropy codec (stage 2)\nUsing 1 job'

def test_independent_header_layout():
    h=parse_header(header());assert h['block_bytes']==1048576 and h['input_blocks_hint']==16
    assert verify_settings(h,REFERENCE,log())

@pytest.mark.parametrize('data',[b'',b'X'*16,header()[:15]])
def test_corrupt_header(data):
    with pytest.raises(ValueError):parse_header(data)

@pytest.mark.parametrize('checksum,codec',[(0,1),(1,5)])
def test_ignored_settings(checksum,codec):
    with pytest.raises(ValueError):verify_settings(parse_header(header(checksum,codec)),REFERENCE,log())

def test_missing_job_receipt():
    with pytest.raises(ValueError):verify_settings(parse_header(header()),REFERENCE,log().replace('Using 1 job','Using 4 jobs'))

def test_exact_comparison_detects_trailing_and_changed_bytes(tmp_path):
    a=tmp_path/'a';b=tmp_path/'b';a.write_bytes(b'abcdef');b.write_bytes(b'abcdef');assert byte_equal(a,b)
    b.write_bytes(b'abcdef\x00');assert not byte_equal(a,b)
    b.write_bytes(b'abcdeg');assert not byte_equal(a,b)
