"""Owner-only bounded source/build-doc retrieval; no installer execution."""
import argparse,json
import fetch_admission_v104 as base
base.OUT=base.ROOT/'artifacts/sources/v105';base.LIMIT=5*1024**2
URLS={'source':'https://nginx.org/download/nginx-1.28.3.tar.gz',
      'configure':'https://nginx.org/en/docs/configure.html'}
NAMES={'source':'nginx-1.28.3.tar.gz','configure':'configure.html'}
def check(url):
    if url not in URLS.values():raise ValueError('Exact official source/docs only')
base.check_url=check
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('kind',choices=URLS);a=p.parse_args()
    print(json.dumps(base.fetch(NAMES[a.kind],URLS[a.kind])))
