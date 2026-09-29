"""Fixed feasibility data and independent bitstream-setting verification.

Header fields/constants follow Apache-2.0 Kanzi1.9 source commit9828b058...
CompressedOutputStream.writeHeader, TransformFactory, EntropyCodecFactory.
No measured labels or optimizer decisions are used by this module.
"""
import hashlib
import struct

REFERENCE={'transform':'LZ+RLT','entropy':'HUFFMAN','block_bytes':1048576,'jobs':1}
CONTRAST={'transform':'BWT+RANK+ZRLT','entropy':'ANS0','block_bytes':65536,'jobs':4}
TRANSFORMS={'BWT':1,'BWTS':2,'LZ':3,'RLT':5,'ZRLT':6,'MTFT':7,'RANK':8,'X86':9,'TEXT':10,'ROLZ':11,'ROLZX':12,'SRT':13,'LZP':14,'FSD':15,'LZX':16}
ENTROPY={'HUFFMAN':1,'FPAQ':2,'RANGE':4,'ANS0':5,'CM':6,'TPAQ':7,'ANS1':8,'TPAQX':9}

def generated_workload():
    """16 MiB, four prescribed equal parts, not a production corpus."""
    n=4*1024**2
    def fill(data):return (data*((n+len(data)-1)//len(data)))[:n]
    records=b''.join(('record=%06d category=%02d value=%08d status=complete\n'%(i,i%17,(i*101)%100000)).encode() for i in range(4096))
    text=b'Configuration experiments require complete records, exact validation, and reproducible inputs.\n'
    binary=b''.join(struct.pack('<4I',i,i%1024,i*i%(2**32),i^0xA5A5A5A5) for i in range(65536))
    entropy=b''.join(hashlib.sha256(b'kanzi-v74-fixed-workload:'+struct.pack('<I',i)).digest() for i in range(n//32))
    return fill(records)+fill(text)+fill(binary)+entropy

def parse_header(data):
    if len(data)<16:raise ValueError('Truncated header')
    number=int.from_bytes(data[:16],'big');left=128
    def get(width):
        nonlocal left
        left-=width;return (number>>left)&((1<<width)-1)
    magic=get(32);version=get(4);checksum=get(1);codec=get(5);transforms=get(48)
    block=get(28)*16;nbblocks=get(6);reserved=get(4)
    if magic!=0x4B414E5A or version!=1 or reserved!=0:raise ValueError('Unexpected stream format')
    return {'version':version,'checksum':bool(checksum),'entropy_type':codec,'transform_type':transforms,'block_bytes':block,'input_blocks_hint':nbblocks}

def verify_settings(header,config,log):
    expected=sum(TRANSFORMS[t]<<(42-6*i) for i,t in enumerate(config['transform'].split('+')))
    if header['checksum'] is not True or header['entropy_type']!=ENTROPY[config['entropy']]:raise ValueError('Checksum/codec mismatch')
    if header['transform_type']!=expected or header['block_bytes']!=config['block_bytes']:raise ValueError('Transform/block mismatch')
    for fragment in [f'Block size set to {config["block_bytes"]} bytes','Checksum set to true',
                     f'Using {config["transform"]} transform (stage 1)',
                     f'Using {config["entropy"]} entropy codec (stage 2)',f'Using {config["jobs"]} job']:
        if fragment not in log:raise ValueError('Missing applied-setting log: '+fragment)
    if 'Ignoring invalid option' in log or 'Warning:' in log:raise ValueError('Ignored/adjusted option')
    return True

def byte_equal(left,right):
    with left.open('rb') as a,right.open('rb') as b:
        while True:
            x=a.read(1024**2);y=b.read(1024**2)
            if x!=y:return False
            if not x:return True
