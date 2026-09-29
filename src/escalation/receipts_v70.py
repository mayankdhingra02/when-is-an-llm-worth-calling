"""Atomic JSON phase receipts. Serialize before touching an existing receipt."""
import json
import os
from .record_json_v69 import bytes_default

def atomic_json(path, value):
    data = json.dumps(value, indent=2, default=bytes_default) + '\n'
    pending = path.with_name(path.name + '.pending')
    try:
        with pending.open('w') as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(pending, path)
    finally:
        if pending.exists():pending.unlink()
