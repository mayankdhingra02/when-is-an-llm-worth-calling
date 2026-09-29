"""Declared application inputs and independent correctness contracts for V66."""
import hashlib,itertools,json

SORT_N = 2**20
DUCK_N = 2**22
IMAGE_SIDE = 1024


def grids():
    return {
        'duckdb': list(itertools.product([1,2,4,8], ['64MB','128MB','256MB','512MB'], [0,8,12])),
        'gnu_sort': list(itertools.product([1,2,4,8], ['1M','4M','16M','64M'], [2,16,64])),
        'openjpeg': list(itertools.product([16,32,64], [3,5], [128,256,512,1024], [1,2])),
    }


def expected_query(n=DUCK_N):
    sums=[0]*256;counts=[0]*256
    for i in range(n):
        g=i%256;sums[g]+=(i%97)*((i%4096)%17+1);counts[g]+=1
    return [[g,sums[g],counts[g]] for g in range(256) if counts[g]]


def sort_line(i):return f'{i:08d}\n'.encode('ascii')


def sorted_digest(n=SORT_N):
    h=hashlib.sha256()
    for i in range(n):h.update(sort_line(i))
    return h.hexdigest()


def image_pixels(side=IMAGE_SIDE):
    return bytes(((x*13+y*7)^((x//32+y//32)*11))&255 for y in range(side) for x in range(side))


def read_pgm(data):
    pos=0;tokens=[]
    while len(tokens)<4:
        while pos<len(data) and data[pos] in b' \t\r\n':pos+=1
        if pos<len(data) and data[pos]==35:
            end=data.find(b'\n',pos)
            if end<0:raise ValueError('Unterminated PGM comment')
            pos=end+1;continue
        start=pos
        while pos<len(data) and data[pos] not in b' \t\r\n':pos+=1
        if pos==start:raise ValueError('Incomplete PGM header')
        tokens.append(data[start:pos])
    if tokens[0]!=b'P5' or tokens[3]!=b'255':raise ValueError('Expected 8-bit binary PGM')
    w,h=map(int,tokens[1:3])
    if w<1 or h<1 or pos>=len(data) or data[pos] not in b' \t\r\n':raise ValueError('Invalid PGM shape')
    pos+=2 if data[pos:pos+2]==b'\r\n' else 1
    pixels=data[pos:]
    if len(pixels)!=w*h:raise ValueError('PGM pixel count mismatch')
    return w,h,pixels
