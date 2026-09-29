"""V17 features; reuse unchanged V16 charged oracle and acquired-only search."""
from types import SimpleNamespace
from .offline_live_v16 import FEATURES, REFERENCES, RecordedOracle, make_prefix, continuation
from .live_compression_v17 import settings

def candidates(entry):
    family=entry['system_group'];rows=entry['configurations'];names=FEATURES[family]
    expected=[r for r in settings() if r['family']==family]
    if rows!=expected:raise ValueError('Candidate grid differs from frozen V17 settings')
    xs=tuple(tuple(float(r[n]) for n in names) for r in rows)
    if len(set(xs))!=len(xs):raise ValueError('Duplicate feature configuration')
    reference=next(i for i,r in enumerate(rows) if all(r[k]==v for k,v in REFERENCES[family].items()))
    return SimpleNamespace(x=xs),[r['config_id'] for r in rows],reference
