"""Feature-only reconciliation of the owner's Kanzi samples; no outcome input."""
BOOLS = ['LZP','ROLZX','RANK','TEXT','skip','TPAQ','BWTS','LZ','MTFT','SRT',
         'X86','checksum','FPAQ','RLT','BWT','TPAQX','CM','ZRLT','Range','ROLZ','ANS0','ANS1','Huffman']
FEATURES = BOOLS+['jobs','blocksize']

def released_vector(row):
    if set(row) != set(FEATURES+['config_id']): raise ValueError('Unexpected feature schema; outcomes forbidden')
    if any(row[k] not in ('True','False') for k in BOOLS): raise ValueError('Invalid boolean')
    if row['jobs'] not in ('1','4','8') or row['blocksize'] not in ('1000','1000000','1000000000'):
        raise ValueError('Undeclared numeric level')
    return tuple(row[k] for k in FEATURES)

def original_vector(row):
    jobs = ['jobs_1','jobs_4','jobs_8']; blocks = ['blocksize_1KB','blocksize_1MB','blocksize_1GB']
    if set(row) != set(BOOLS+jobs+blocks+['','entropy']): raise ValueError('Unexpected original schema')
    if any(row[k] not in ('True','False') for k in BOOLS+jobs+blocks+['entropy']): raise ValueError('Invalid boolean')
    js = [n for k,n in zip(jobs,['1','4','8']) if row[k]=='True']
    bs = [n for k,n in zip(blocks,['1000','1000000','1000000000']) if row[k]=='True']
    if len(js)!=1 or len(bs)!=1: raise ValueError('Invalid one-hot feature encoding')
    return tuple(row[k] for k in BOOLS)+(js[0],bs[0])
