"""Lossless byte metadata for JSON receipts; never reinterpret measured values."""
def bytes_default(value):
    if isinstance(value, bytes):
        return {'bytes_hex': value.hex()}
    raise TypeError('unsupported result metadata: '+type(value).__name__)
