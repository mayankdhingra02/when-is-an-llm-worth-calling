"""Bounded partial ZIP directory audit; explicit source members only, no code run."""
import argparse
import json
import struct
import zlib
import hashlib
from inspect_zip_v73 import OUT, RemoteArchive, SIZE

CD_START=354778498
CD_SIZE=46552624

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--offset',type=int);p.add_argument('--count',type=int,default=524288)
    p.add_argument('--member');p.add_argument('--output');a=p.parse_args()
    index=OUT/'partial_inventory.json';rows=json.loads(index.read_text()) if index.exists() else []
    remote=RemoteArchive()
    if a.offset is not None:
        if a.offset<0 or a.offset+a.count>CD_SIZE:raise ValueError('Central-directory bounds')
        remote.seek(CD_START+a.offset);data=remote.read(a.count);pos=0;found=[]
        while True:
            pos=data.find(b'PK\x01\x02',pos)
            if pos<0 or pos+46>len(data):break
            v=struct.unpack('<4s6H3L5H2L',data[pos:pos+46]);n,e,c=v[10:13];end=pos+46+n+e+c
            if end>len(data):break
            name=data[pos+46:pos+46+n].decode('utf-8' if v[3]&0x800 else 'cp437')
            found.append({'name':name,'bytes':v[9],'compressed_bytes':v[8],'crc32':v[7],'compression_method':v[4],'flags':v[3],'local_header_offset':v[16]})
            pos=end
        existing={r['name']:r for r in rows};existing.update({r['name']:r for r in found});rows=list(existing.values())
        index.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps({'segment_entries':len(found),'known_entries':len(rows),'complete_inventory':False,'first':found[0]['name'] if found else None,'last':found[-1]['name'] if found else None}))
    elif a.member:
        row=next(r for r in rows if r['name']==a.member)
        if any(w in a.member.lower() for w in ['measurement','result','coverage']):raise ValueError('Outcome member excluded')
        if not a.output or '/' in a.output or row['bytes']>1024**2:raise ValueError('Output/name/size limits')
        dest=OUT/a.output
        if dest.exists():raise FileExistsError(dest)
        remote.seek(row['local_header_offset']);header=remote.read(30);v=struct.unpack('<4s5H3L2H',header)
        assert v[0]==b'PK\x03\x04' and not (v[2]&1)
        name=remote.read(v[-2]);assert name.decode('utf-8' if v[2]&0x800 else 'cp437')==a.member
        remote.seek(v[-1],1);data=remote.read(row['compressed_bytes'])
        if row['compression_method']==8:
            dec=zlib.decompressobj(-15);data=dec.decompress(data,row['bytes']+1);assert dec.eof
        else:assert row['compression_method']==0
        assert len(data)==row['bytes'] and zlib.crc32(data)==row['crc32']
        dest.write_bytes(data);(OUT/(a.output+'.provenance.json')).write_text(json.dumps({**row,'sha256':hashlib.sha256(data).hexdigest(),'partial_archive_only':True},indent=2)+'\n')
        print(json.dumps({'member':a.member,'bytes':len(data)}))
    else:raise ValueError('Choose directory segment or explicit source member')
