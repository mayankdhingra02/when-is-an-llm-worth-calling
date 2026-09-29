"""Post-hoc synthetic formatting diagnostic: tokenizer requests only, no generation."""
import json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**k):raise ValueError('No redirect')
def main():
 out=ROOT/'artifacts/study_v127/synthetic_tokenizer_diagnostic.json';assert not out.exists();jobs=json.loads((ROOT/'artifacts/study_v127/jobs.json').read_text());rows=[];opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect());start=time.monotonic()
 for j in jobs:
  if j['condition']!='normal' or j['seed']!=11:continue
  content=json.dumps(['0'*len(j['domains'])]*10,separators=(',',':'));p={'content':content,'add_special':False,'parse_special':False};row={'dataset':j['dataset'],'fixture':'synthetic all-zero domain-index strings,not model output','characters':len(content),'payload':p,'generation_requests':0};t=time.monotonic()
  try:
   req=urllib.request.Request('http://127.0.0.1:18591/tokenize',data=json.dumps(p).encode(),headers={'Content-Type':'application/json'});row['response']=json.load(opener.open(req,timeout=5));row['token_count']=len(row['response']['tokens'])
  except Exception as e:row['error']=repr(e)
  row['seconds']=time.monotonic()-t;rows.append(row)
 out.write_text(json.dumps({'scope':'Post-hoc synthetic-format tokenizer diagnostic,never research model-output aggregates','metadata_attempts':len(rows),'new_generation_requests':0,'new_objective_acquisitions':0,'seconds':time.monotonic()-start,'rows':rows},indent=2)+'\n');print([(r['dataset'],r.get('token_count'),r.get('error')) for r in rows])
if __name__=='__main__':main()
