# Deterministic value recipe adapted from YCSB CoreWorkload (Apache-2.0).
# Copyright (c) 2010 Yahoo! Inc., (c) 2016-2017 YCSB contributors.
# Licensed under the Apache License, Version 2.0; see
# artifacts/sources/v68/ycsb/source/LICENSE.txt and THIRD_PARTY.md.
# Provided AS IS, without warranties or conditions of any kind.
"""Strict validation for a future read-only YCSB-C adaptation; no objectives.

Deterministic values follow YCSB 0.17.0 CoreWorkload.buildDeterministicValue
(Apache-2.0, Yahoo!/YCSB contributors). Restrict identifiers to ASCII so Java
UTF-16 and Python code points agree. This module does not run a database.
"""
import re
from collections.abc import Mapping


def read_only_contract(properties):
    required = {
        'workload': 'site.ycsb.workloads.CoreWorkload',
        'readproportion': '1', 'updateproportion': '0', 'insertproportion': '0',
        'scanproportion': '0', 'readmodifywriteproportion': '0',
        'readallfields': 'true', 'dataintegrity': 'true',
        'fieldlengthdistribution': 'constant', 'requestdistribution': 'zipfian',
        'insertorder': 'ordered', 'fieldnameprefix': 'field', 'zeropadding': '1',
    }
    for key, expected in required.items():
        if properties.get(key) != expected:
            raise ValueError('missing or incompatible property: ' + key)
    counts = {}
    for key in ('fieldcount', 'fieldlength', 'recordcount', 'operationcount'):
        value = properties.get(key, '')
        if not isinstance(value, str) or not re.fullmatch(r'[1-9][0-9]*', value):
            raise ValueError('positive integer required: ' + key)
        counts[key] = int(value)
    if counts['fieldcount'] > 1000 or counts['fieldlength'] > 1048576:
        raise ValueError('validator size cap')
    # Extra properties may be backend knobs. They need a separately frozen
    # application/domain contract; this check alone never admits a task.
    return counts


def deterministic_value(key, field, length):
    if not isinstance(key, str) or not isinstance(field, str) or not key.isascii() or not field.isascii():
        raise ValueError('ASCII key and field required')
    if type(length) is not int or not 1 <= length <= 1048576:
        raise ValueError('invalid value length')
    if len(key) + len(field) > 4096:
        raise ValueError('identifier size cap')
    initial = key + ':' + field
    chunks = [initial]
    size = len(initial)
    h = 0
    for ch in initial:
        h = (31 * h + ord(ch)) & 0xffffffff
    while size < length:
        h = (31 * h + ord(':')) & 0xffffffff
        digits = str(h if h < 0x80000000 else h - 0x100000000)
        chunks.append(':' + digits)
        size += len(digits) + 1
        for ch in digits:
            h = (31 * h + ord(ch)) & 0xffffffff
    return ''.join(chunks)[:length]


def verify_record(key, fields, fieldcount, fieldlength):
    if type(fieldcount) is not int or not 1 <= fieldcount <= 1000:
        raise ValueError('invalid field count')
    expected = {'field' + str(i) for i in range(fieldcount)}
    if not isinstance(fields, Mapping) or set(fields) != expected:
        raise ValueError('missing or unexpected fields')
    for field in expected:
        if fields[field] != deterministic_value(key, field, fieldlength):
            raise ValueError('incorrect field contents')


def verify_snapshot(records, recordcount, fieldcount, fieldlength):
    """Validate every ordered userN key, once; callers must export complete data.

    Any export/validation queries are additional actual collection cost. A full
    snapshot checks final contents, not every timed response or crash durability.
    """
    if type(recordcount) is not int or recordcount <= 0:
        raise ValueError('invalid record count')
    seen = set()
    for record in records:
        if not isinstance(record, Mapping) or set(record) != {'key', 'fields'}:
            raise ValueError('invalid record schema')
        key = record['key']
        if not isinstance(key, str) or not re.fullmatch(r'user(?:0|[1-9][0-9]*)', key):
            raise ValueError('invalid key')
        index = int(key[4:])
        if index >= recordcount or key in seen:
            raise ValueError('out-of-range or duplicate key')
        verify_record(key, record['fields'], fieldcount, fieldlength)
        seen.add(key)
    if len(seen) != recordcount:
        raise ValueError('incomplete snapshot')
    return {'records_verified': len(seen), 'fields_verified': len(seen) * fieldcount}


def verify_read_counters(text, expected_operations, *, returncode, timed_out):
    """Read status counters only; latency/throughput cells remain opaque strings."""
    if type(expected_operations) is not int or expected_operations <= 0:
        raise ValueError('invalid intended operation count')
    if returncode != 0 or timed_out is not False:
        raise ValueError('process failure or missing timeout status')
    counters = {}
    for line in text.splitlines():
        if not line.startswith('['):
            continue  # JVM/banner text is not an exporter record.
        cells = line.split(',', 2)
        if len(cells) != 3:
            raise ValueError('malformed exporter record')
        group, name, raw = (v.strip() for v in cells)
        if not re.fullmatch(r'\[[A-Z][A-Z0-9_-]*\]', group):
            raise ValueError('malformed exporter group')
        if name != 'Operations' and not name.startswith('Return='):
            continue
        if not re.fullmatch(r'0|[1-9][0-9]*', raw):
            raise ValueError('invalid counter')
        identity = (group[1:-1], name)
        if identity in counters:
            raise ValueError('duplicate counter')
        counters[identity] = int(raw)
    for group in ('READ', 'VERIFY'):
        for name in ('Operations', 'Return=OK'):
            if counters.get((group, name)) != expected_operations:
                raise ValueError('missing or inconsistent success denominator')
    for (group, name), value in counters.items():
        if group not in ('READ', 'VERIFY') and value:
            raise ValueError('unexpected operation type')
        if name.startswith('Return=') and name != 'Return=OK' and value:
            raise ValueError('non-OK response')
    return {'read_operations': expected_operations, 'verified_operations': expected_operations,
            'all_reported_statuses_ok': True,
            'field_completeness_certified_by_counters': False}
