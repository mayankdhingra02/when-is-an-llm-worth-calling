"""Prospective policies: features and acquired observations only."""
import json
import math
import numpy as np

SEEDS = [11, 23, 37, 53, 71]
METHODS = ['rf_lcb', 'domain_prior', 'llm']


def vectors(configs):
    return [[c['cache_mib'], c['block_size'], c['restart_interval']] for c in configs]


def features(configs):
    return np.array([[math.log2(a)/7, (math.log2(b)-9)/7, math.log2(c)/7]
                     for a, b, c in vectors(configs)])


def prior_choice(configs, observations):
    """Large cache, small block, small restart interval; no outcome dependence."""
    used = {o['config_id'] for o in observations}
    return min((i for i in range(len(configs)) if i not in used),
               key=lambda i: (-configs[i]['cache_mib'], configs[i]['block_size'],
                              configs[i]['restart_interval'], i))


def messages(configs, observations):
    # Explicit allowlist: receipt paths and any unrelated metadata are excluded.
    rows = [{'configuration': vectors(configs)[o['config_id']],
             'measured_ms': o['value_ms']} for o in observations]
    levels = {k: sorted({c[k] for c in configs}) for k in configs[0]}
    return [
        {'role': 'system', 'content': 'Choose one unmeasured software configuration to minimize elapsed milliseconds. Return only one compact JSON array [cache_mib,block_size,restart_interval]. Do not repeat an observed configuration.'},
        {'role': 'user', 'content': 'RocksDB 9.8.4, read-only fixed scrambled-Zipfian point lookups. 65536 records of 1000 bytes, uncompressed, 10000 warmup reads then 100000 timed verified reads. The block cache capacity is in MiB, block size in bytes, restart interval in keys. Each measurement uses a freshly loaded DB and application cache; OS cache is not cleared. Lower measured_ms is better. Allowed levels: ' + json.dumps(levels, separators=(',', ':')) + '. Observations in acquisition order: ' + json.dumps(rows, separators=(',', ':')) + '. Choose the next configuration.'}
    ]


def validate_acquisition(cid, observations, purpose, physical_count):
    if purpose not in ('search', 'confirmation'): raise ValueError('Invalid purpose')
    if type(cid) is not int or not 0 <= cid < 512: raise ValueError('Invalid ID')
    if len(observations) >= 20 or physical_count >= 150: raise ValueError('Budget exhausted')
    if purpose == 'search' and cid in {o['config_id'] for o in observations}:
        raise ValueError('Duplicate search')

