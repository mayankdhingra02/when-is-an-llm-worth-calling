import io
import pytest
from escalation.redis_v60 import decode,encode,field,key,value,validate,FIELDS,KEYS

def test_resp_roundtrip_bulk_and_array():
    assert decode(io.BytesIO(encode([b'HGET',b'x\r\ny',b'z'])))==[b'HGET',b'x\r\ny',b'z']
    assert decode(io.BytesIO(b':12\r\n'))==12
    assert decode(io.BytesIO(b'$-1\r\n')) is None

@pytest.mark.parametrize('payload',[b'$4\r\nabc\r\n',b'*1048577\r\n',b'-ERR bad\r\n',b'+unfinished',b'?x\r\n'])
def test_resp_invalid_rejected(payload):
    with pytest.raises(ValueError):decode(io.BytesIO(payload))

def test_fixture_corruption_is_not_accepted_as_valid_measurement():
    class Fixture:
        def call(self,*args):
            if args[0]=='DBSIZE':return KEYS
            answer=[]
            for i in range(FIELDS):answer.extend([field(i),value(i)])
            answer[-1]=b'corrupt';return answer
    with pytest.raises(AssertionError):validate(Fixture())

def test_workload_boundaries_and_distinct_fields():
    assert key(255)==b'v60:000000000255'
    assert value(0)!=value(127) and all(len(value(i))==64 for i in range(FIELDS))
