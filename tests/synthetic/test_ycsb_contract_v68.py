"""Synthetic fault injection only. No database/LLM measurements."""
import pytest
from escalation.ycsb_contract_v68 import (
    deterministic_value, read_only_contract, verify_record, verify_snapshot, verify_read_counters)


def properties():
    return dict(workload='site.ycsb.workloads.CoreWorkload', readproportion='1',
        updateproportion='0', insertproportion='0', scanproportion='0',
        readmodifywriteproportion='0', readallfields='true', dataintegrity='true',
        fieldlengthdistribution='constant', requestdistribution='zipfian',
        insertorder='ordered', fieldnameprefix='field', zeropadding='1',
        fieldcount='10', fieldlength='100', recordcount='2', operationcount='5')


def row(key='user0'):
    return {'key': key, 'fields': {f'field{i}': deterministic_value(key, f'field{i}', 100) for i in range(10)}}


def counters():
    return '\n'.join(f'[{g}], {k}, 5' for g in ['READ', 'VERIFY'] for k in ['Operations', 'Return=OK'])


def test_contract():
    assert read_only_contract(properties())['operationcount'] == 5


@pytest.mark.parametrize('key,value', [('dataintegrity','false'), ('readallfields','false'),
    ('fieldlengthdistribution','uniform'), ('readmodifywriteproportion','0.1'),
    ('scanproportion','0.1'), ('insertorder','hashed'), ('recordcount','0'),
    ('operationcount','NaN'), ('fieldlength','1048577'), ('fieldcount','1001')])
def test_contract_rejects(key, value):
    p = properties(); p[key] = value
    with pytest.raises(ValueError): read_only_contract(p)


def test_missing_property():
    p = properties(); del p['dataintegrity']
    with pytest.raises(ValueError): read_only_contract(p)


def test_completeness():
    r = row(); verify_record(r['key'], r['fields'], 10, 100)
    del r['fields']['field9']
    with pytest.raises(ValueError, match='missing'): verify_record(r['key'], r['fields'], 10, 100)


@pytest.mark.parametrize('mode', ['corrupt', 'extra', 'empty'])
def test_bad_field(mode):
    r = row()
    if mode == 'corrupt': r['fields']['field0'] = 'bad'
    elif mode == 'extra': r['fields']['field10'] = 'unexpected'
    else: r['fields'].clear()
    with pytest.raises(ValueError): verify_record(r['key'], r['fields'], 10, 100)


def test_snapshot():
    assert verify_snapshot([row('user1'), row()], 2, 10, 100)['fields_verified'] == 20


@pytest.mark.parametrize('keys', [['user0'], ['user0','user0'], ['user0','user2'], ['user0','user01']])
def test_bad_snapshot(keys):
    with pytest.raises(ValueError): verify_snapshot([row(k) for k in keys], 2, 10, 100)


def test_counters_ignore_poisoned_objectives():
    s = counters() + '\n[OVERALL], Throughput(ops/sec), NEVER_PARSE_ME\n[READ], AverageLatency(us), NaN'
    assert verify_read_counters(s, 5, returncode=0, timed_out=False)['field_completeness_certified_by_counters'] is False


@pytest.mark.parametrize('suffix', ['\n[READ], Return=ERROR, 1', '\n[VERIFY], Return=UNEXPECTED_STATE, 1',
    '\n[UPDATE], Operations, 1', '\n[READ], Return=OK, 5', '\n[READ], Return=ERROR, NaN',
    '\n[READ], Return=ERROR, -1', '\n[READ] malformed'])
def test_counter_failures(suffix):
    with pytest.raises(ValueError): verify_read_counters(counters()+suffix, 5, returncode=0, timed_out=False)


@pytest.mark.parametrize('rc,timeout', [(1,False),(0,True),(0,None)])
def test_process_failure(rc, timeout):
    with pytest.raises(ValueError): verify_read_counters(counters(), 5, returncode=rc, timed_out=timeout)


def test_missing_denominator():
    with pytest.raises(ValueError): verify_read_counters('[READ], Return=OK, 5', 5, returncode=0, timed_out=False)


def test_ascii_restriction():
    with pytest.raises(ValueError): deterministic_value('ü', 'field0', 100)


def test_hand_computed_java_hash():
    # Java hashCode: 97 -> 3065 -> 95113 -> 2948561 (after each character).
    assert deterministic_value('a', 'b', 11) == 'a:b:2948561'


def test_incremental_hash_matches_simple_reference():
    # Independent deliberately slow Java-hash recipe over complete prefixes.
    for key in ('user0', 'user999999', 'a'):
        for length in (1, 11, 100, 1024):
            value = key + ':field0'
            while len(value) < length:
                value += ':'
                unsigned = sum(ord(c) * 31 ** i for i, c in enumerate(reversed(value))) % 2**32
                value += str(unsigned if unsigned < 2**31 else unsigned - 2**32)
            assert deterministic_value(key, 'field0', length) == value[:length]
