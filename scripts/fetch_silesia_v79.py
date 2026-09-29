"""Bounded owner-only corpus retrieval; never execute downloaded content."""
import bz2,hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/study_v79';OUT=ROOT/'data/raw/silesia_v79'
FILES=[('dickens',10192446,'88334708559f6db57d79096bc0aca07e','plain text'),('sao',7251944,'79e95a22e18cd82b7e42bf91b380d30b','binary records'),('xml',5345280,'9b09c0c80104adb8aae910b7d7db003e','structured markup')]
LIMIT=12*1024**2

def main():
    assert not (ART/'workloads.json').exists()
    prior=json.loads((ROOT/'artifacts/study_v78_execution/resource_ledger.json').read_text())
    assert prior['remaining_download_bytes']>=LIMIT
    total=0;receipts=[]
    for name,size,md5,kind in FILES:
        url='https://sun.aei.polsl.pl/~sdeor/corpus/'+name+'.bz2';archive=OUT/(name+'.bz2')
        assert not archive.exists()
        receipt={'name':name,'url':url,'retrieved_at_unix':time.time(),'download_bytes':0};receipts.append(receipt)
        try:
            with urllib.request.urlopen(url,timeout=60) as response, archive.open('xb') as f:
                assert response.url==url
                while True:
                    block=response.read(min(65536,LIMIT-total+1))
                    if not block:break
                    total+=len(block);receipt['download_bytes']+=len(block)
                    assert total<=LIMIT,'download cap'
                    f.write(block)
            dec=bz2.BZ2Decompressor();raw=dec.decompress(archive.read_bytes(),max_length=size+1)
            assert dec.eof and not dec.unused_data and len(raw)==size,'unexpected payload size/container'
            assert hashlib.md5(raw).hexdigest()==md5,'owner MD5 mismatch'
            target=OUT/name
            with target.open('xb') as f:f.write(raw)
            receipt.update(status='verified',bytes=size,md5=md5,sha256=hashlib.sha256(raw).hexdigest(),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),path=str(target.relative_to(ROOT)),kind=kind,system_group='kanzi',split='development')
        finally:
            (ART/'download_ledger.json').write_text(json.dumps({'new_download_bytes':total,'prior_download_bytes':prior['cumulative_download_bytes'],'cumulative_download_bytes':prior['cumulative_download_bytes']+total,'remaining_download_bytes':prior['remaining_download_bytes']-total,'receipts':receipts},indent=2)+'\n')
    (ART/'workloads.json').write_text(json.dumps({'selection':'Three owner-listed categories: plain text, binary records and structured markup, each 5–11 MiB; fixed before any Kanzi outcome. No trimming, synthesis or outcome-based replacement.','owner_page':'https://sun.aei.polsl.pl/~sdeor/index.php?page=silesia','license':'No blanket corpus redistribution license established; local research use of owner-provided downloads only, raw payloads excluded from Git/bundles. Original-source rights remain distinct.','files':receipts},indent=2)+'\n')
    print(json.dumps({'download_bytes':total,'workloads_verified':len(receipts)}))
if __name__=='__main__':main()
