"""Feature-only eligibility and narrow compressed-frame inspection."""
def eligible(setting):
    family=setting['family']
    if family=='zstd':return setting['checksum'] is True
    if family=='lz4':return setting['dependent'] is False
    if family=='zlib':return True
    raise ValueError('Unknown codec')

def frame_fields(family,payload):
    if family=='zstd':
        if payload[:4]!=bytes.fromhex('28b52ffd') or len(payload)<6:raise ValueError('Not a Zstandard frame')
        return {'content_checksum':bool(payload[4]&4)}
    if family=='lz4':
        if payload[:4]!=bytes.fromhex('04224d18') or len(payload)<7 or payload[4]>>6!=1:raise ValueError('Not an LZ4 v1 frame')
        return {'content_checksum':bool(payload[4]&4),'independent_blocks':bool(payload[4]&32),'block_size_id':(payload[5]>>4)&7}
    if family=='zlib':
        if len(payload)<6 or (payload[0]&15)!=8 or payload[0]>>4>7 or int.from_bytes(payload[:2],'big')%31:raise ValueError('Not a zlib wrapper')
        return {'wrapped':True,'preset_dictionary':bool(payload[1]&32),'window_log':(payload[0]>>4)+8}
    raise ValueError('Unknown codec')
