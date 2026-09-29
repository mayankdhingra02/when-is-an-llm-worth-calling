"""Read only ZIP metadata/explicit source members via bounded HTTP ranges."""
import argparse
import hashlib
import io
import json
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'artifacts/sources/v73'
URL = 'https://zenodo.org/api/records/7658046/files/artifact_excluding_raw_coverage.zip/content'
SIZE = 401331220
CAP = 10*1024**2

class RemoteArchive(io.RawIOBase):
    def __init__(self): self.position = 0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.position
    def seek(self, offset, whence=0):
        self.position = offset if whence==0 else self.position+offset if whence==1 else SIZE+offset
        if self.position<0 or self.position>SIZE: raise ValueError('Seek bounds')
        return self.position
    def read(self, count=-1):
        if count<0: count = SIZE-self.position
        count = min(count, SIZE-self.position)
        if count==0: return b''
        ledgerpath = OUT/'range_manifest.json'
        ledger = json.loads(ledgerpath.read_text()) if ledgerpath.exists() else {'url':URL,'archive_bytes':SIZE,'ranges':[]}
        used = sum(r['bytes'] for r in ledger['ranges'])+sum(e['bytes'] for e in json.loads((OUT/'manifest.json').read_text())['entries'])
        if count > CAP-used: raise ValueError('Combined metadata stage cap')
        start = self.position; end = start+count-1
        # Reuse already stored exact ranges; do not count replay as fresh network.
        for entry in ledger['ranges']:
            if entry['start']==start and entry['end']==end:
                data=(OUT/entry['file']).read_bytes();assert hashlib.sha256(data).hexdigest()==entry['sha256']
                self.position+=len(data);return data
        req=urllib.request.Request(URL,headers={'Range':f'bytes={start}-{end}','User-Agent':'llm-escalation-study-source-audit'})
        with urllib.request.urlopen(req,timeout=40) as response:
            if response.status!=206 or response.headers.get('Content-Range')!=f'bytes {start}-{end}/{SIZE}':
                raise ValueError('Server did not honor exact Range; body not downloaded')
            data=response.read(count+1)
            if len(data)!=count:raise ValueError('Unexpected range size')
            entry={'start':start,'end':end,'bytes':len(data),'etag':response.headers.get('ETag'),'file':f'zip_range_{len(ledger["ranges"]):03d}.bin','sha256':hashlib.sha256(data).hexdigest(),'at':datetime.now(timezone.utc).isoformat()}
        (OUT/entry['file']).write_bytes(data);ledger['ranges'].append(entry);ledgerpath.write_text(json.dumps(ledger,indent=2)+'\n')
        self.position+=len(data);return data


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--member');p.add_argument('--output');args=p.parse_args()
    with zipfile.ZipFile(RemoteArchive()) as archive:
        if args.member is None:
            rows=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size,'crc32':i.CRC} for i in archive.infolist()]
            (OUT/'archive_inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(json.dumps({'archive_members':len(rows),'archive_downloaded_in_full':False,'objective_members_opened':0}))
        else:
            member=archive.getinfo(args.member)
            if member.file_size>5*1024**2:raise ValueError('Individual decompressed member cap')
            if Path(args.member).suffix.lower() not in ['.md','.txt','.py','.sh','.xml','.dimacs','.csv']:
                raise ValueError('Source/configuration metadata members only')
            if any(word in args.member.lower() for word in ['measurement','performance.csv','coverage','result']):
                raise ValueError('Outcome members excluded')
            if not args.output or Path(args.output).name!=args.output:raise ValueError('Output basename required')
            dest=OUT/args.output
            if dest.exists():raise FileExistsError('No overwrite')
            data=archive.read(member)  # stdlib verifies entry CRC; no execution
            dest.write_bytes(data)
            meta={'archive_url':URL,'member':args.member,'bytes':len(data),'crc32':member.CRC,'sha256':hashlib.sha256(data).hexdigest(),'scope':'source/feature metadata only; archive-wide MD5 not verified'}
            (OUT/(args.output+'.provenance.json')).write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
