"""Feature-only fixed-service NGINX domain, with platform-inactive options fixed."""
from itertools import product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=bytes(range(256))*128
PORT=18596

def domain():
 modes=[]
 for size in [2048,4096,8192,16384,32768]:
  for n in [1,2,4,8]:
   if n*size<=len(PAYLOAD):modes.append(dict(sendfile=0,buffer_count=n,buffer_size=size,sendfile_chunk=0))
 for chunk in [16384,32768]:modes.append(dict(sendfile=1,buffer_count=0,buffer_size=0,sendfile_chunk=chunk))
 rows=[]
 for mode,(workers,cache,nodelay,postpone,sndbuf) in product(modes,product([1,2,4],[0,1],[0,1],[0,1460],[32768,131072])):
  rows.append(dict(**mode,workers=workers,cache=cache,tcp_nodelay=nodelay,postpone_output=postpone,sndbuf=sndbuf))
 assert len(rows)==768 and len({json.dumps(r,sort_keys=True) for r in rows})==768
 return rows

def config(row,folder):
 assert row in domain()
 flag=lambda x:'on' if x else 'off'
 cache='max=1 inactive=60s' if row['cache'] else 'off'
 output=f"sendfile_max_chunk {row['sendfile_chunk']};" if row['sendfile'] else f"output_buffers {row['buffer_count']} {row['buffer_size']};"
 return f'''daemon off;
master_process on;
worker_processes {row['workers']};
pid "{folder}/nginx.pid";
error_log "{folder}/error.log" notice;
events {{ use kqueue; worker_connections 256; multi_accept off; accept_mutex off; }}
http {{
 access_log off; default_type application/octet-stream;
 sendfile {flag(row['sendfile'])}; {output}
 tcp_nopush off; tcp_nodelay {flag(row['tcp_nodelay'])};
 postpone_output {row['postpone_output']};
 open_file_cache {cache}; open_file_cache_valid 60s;
 keepalive_timeout 10s; keepalive_requests 2000000;
 server {{ listen 127.0.0.1:{PORT} sndbuf={row['sndbuf']}; server_name localhost;
 root "{folder}/www"; location = /payload.bin {{ }} }}
}}
'''

if __name__=='__main__':
 p=ROOT/'configs/nginx_domain_v108.json';assert not p.exists()
 p.write_text(json.dumps({'system_group':'nginx','scope':'prospective development; distinct legal settings, not768independent systems or proven-distinct runtime distributions','rows':domain(),'known_inactive_fixed':['multi_accept on kqueue','tcp_nopush on Darwin sendfile path','disabled-branch knobs'],'service':'one fixed immutable public identity-encoded response on loopback; all responses validated'},indent=2)+'\n')
 print(len(domain()))
