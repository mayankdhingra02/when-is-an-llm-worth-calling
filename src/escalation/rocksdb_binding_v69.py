"""Corrected explicit-column-family opening and active-engine-only readback.

Prepared after V69.1; never applied retroactively to its measured trials.
"""
import hashlib
import re
from pathlib import Path
from .rocksdb_v69 import options, validate_config


def open_configured(path, config):
    from rocksdict import Rdict
    opt, cache = options(config)
    # Passing Options alone still lets rocksdict load the DEFAULT column family's
    # options with a fresh hard-coded 8 MiB cache. Supply both explicitly.
    db = Rdict(str(path), options=opt, column_families={'default': opt})
    return db, cache


def active_readback(path, config):
    validate_config(config)
    path = Path(path)
    active_log = (path/'LOG').read_text(errors='strict')
    files = sorted(path.glob('OPTIONS-*'))
    if not files: raise ValueError('missing active options')
    text = files[-1].read_text()
    for name, expected in [('block_size', config['block_size']),
                           ('block_restart_interval', config['restart_interval'])]:
        values = re.findall(r'^\s*'+name+r'\s*=\s*(\d+)\s*$', text, re.M)
        if not values or any(int(v)!=expected for v in values):
            raise ValueError('active setting mismatch: '+name)
    capacities = [int(v) for v in re.findall(r'^\s*capacity\s*:\s*(\d+)\s*$', active_log, re.M)]
    expected = config['cache_mib']*1024**2
    if not capacities or any(v!=expected for v in capacities):
        raise ValueError(f'active cache mismatch: expected {expected}, observed {capacities}')
    if 'RocksDB version: 9.8.4' not in active_log:
        raise ValueError('unexpected runtime engine version')
    return {'cache_capacity_bytes': expected, 'block_size':config['block_size'],
        'restart_interval':config['restart_interval'], 'active_log_sha256':hashlib.sha256(active_log.encode()).hexdigest(),
        'options_sha256':hashlib.sha256(text.encode()).hexdigest()}
