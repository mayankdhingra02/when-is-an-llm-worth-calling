"""YCSB-C inspired, fixed-trace read-only RocksDB feasibility adaptation.

Zipfian/FNV formula adapted from YCSB 0.17.0 (Apache-2.0), Copyright
2010-2016 Yahoo! Inc. and 2017 YCSB contributors. Python RNG intentionally
differs from Java ThreadLocalRandom; this is not numerical YCSB replication.
"""
import hashlib
import itertools
import random
import re
import struct
from pathlib import Path
from .ycsb_contract_v68 import deterministic_value

RECORDS = 65536
READS = 100000
WARMUP = 10000
FIELD_COUNT = 10
FIELD_LENGTH = 100
VALUE_LENGTH = FIELD_COUNT * FIELD_LENGTH
DOMAINS = {'cache_mib': [1, 2, 4, 8, 16, 32, 64, 128],
           'block_size': [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536],
           'restart_interval': [1, 2, 4, 8, 16, 32, 64, 128]}


def grid():
    return [dict(zip(DOMAINS, values)) for values in itertools.product(*DOMAINS.values())]


def validate_config(c):
    if set(c) != set(DOMAINS) or any(type(c[k]) is not int or c[k] not in DOMAINS[k] for k in DOMAINS):
        raise ValueError('configuration outside declared domain')


def payload(index):
    key = 'user' + str(index)
    return ''.join(deterministic_value(key, 'field'+str(i), FIELD_LENGTH) for i in range(FIELD_COUNT)).encode('ascii')


def fnv64(value):
    h = 0xCBF29CE484222325
    for _ in range(8):
        h = ((h ^ (value & 255)) * 1099511628211) & ((1 << 64) - 1)
        value >>= 8
    signed = h if h < (1 << 63) else h - (1 << 64)
    if signed == -(1 << 63):
        raise ValueError('Java abs(long.MIN_VALUE) is negative')
    return abs(signed)


def trace(seed=69001, count=READS+WARMUP, records=RECORDS):
    if records <= 0 or count < 0: raise ValueError('invalid trace size')
    # Upstream constructor uses max=10^10 inclusive => 10^10+1 items,
    # and its supplied precomputed ZETAN. Preserve that formula explicitly.
    n = 10000000001
    theta, zetan = .99, 26.46902820178302
    eta = (1 - (2/n)**(1-theta)) / (1 - (1+(.5**theta))/zetan)
    rng = random.Random(seed)
    result = []
    for _ in range(count+1):  # upstream generator constructor consumes one draw
        u = rng.random(); uz = u * zetan
        rank = 0 if uz < 1 else 1 if uz < 1+.5**theta else int(n*(eta*u-eta+1)**(1/(1-theta)))
        result.append(fnv64(rank) % records)
    return result[1:]


def options(config):
    validate_config(config)
    from rocksdict import Options, BlockBasedOptions, Cache, DBCompressionType
    cache = Cache(config['cache_mib'] * 1024**2)
    block = BlockBasedOptions()
    block.set_block_cache(cache)
    block.set_block_size(config['block_size'])
    block.set_block_restart_interval(config['restart_interval'])
    block.set_cache_index_and_filter_blocks(False)
    opt = Options(raw_mode=True)
    opt.create_if_missing(True)
    opt.set_block_based_table_factory(block)
    opt.set_compression_type(DBCompressionType.none())
    opt.set_write_buffer_size(8*1024**2)
    opt.set_max_background_jobs(2)
    return opt, cache


def verify_value(value, expected):
    if type(value) is not bytes or len(value) != VALUE_LENGTH or value != expected:
        raise ValueError('missing, truncated, extra or corrupted field payload')


def readback(dbpath, config):
    """Read engine-generated options/log, not merely our requested settings."""
    option_files = sorted(Path(dbpath).glob('OPTIONS-*'))
    if not option_files: raise ValueError('no engine OPTIONS file')
    text = option_files[-1].read_text()
    def field(name, expected):
        matches = re.findall(r'^\s*' + name + r'\s*=\s*(\d+)\s*$', text, re.M)
        if not matches or any(int(v) != expected for v in matches):
            raise ValueError('applied option mismatch: '+name)
    field('block_size', config['block_size'])
    field('block_restart_interval', config['restart_interval'])
    # Cache capacity is reported in engine LOG rather than the OPTIONS file.
    logs = '\n'.join(p.read_text(errors='replace') for p in Path(dbpath).glob('LOG*') if p.is_file())
    capacity = config['cache_mib'] * 1024**2
    capacities = [int(v) for v in re.findall(r'(?:capacity\s*[=:]\s*)(\d+)', logs)]
    if capacity not in capacities:
        raise ValueError('cache capacity not independently visible in engine log')
    return {'block_size': config['block_size'], 'restart_interval': config['restart_interval'],
            'cache_capacity_bytes': capacity, 'options_sha256': hashlib.sha256(text.encode()).hexdigest()}
