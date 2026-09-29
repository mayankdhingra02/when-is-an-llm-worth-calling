"""Independent posterior/EI, charged source and aggregate replay; no acquisitions."""
import copy,csv,hashlib,json,math,statistics,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v155';O=ROOT/'results/v155_gp'
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(s) for s in p.read_text().splitlines()]
def close(a,b):assert math.isclose(a,b,rel_tol=1e-7,abs_tol=1e-8),(a,b)
def encode(raw):
 columns=[];nominal=[]
 for col in zip(*raw):
  if len(set(col))<2:continue
  if any(isinstance(x,str) for x in col):nominal.append([sorted(set(col)).index(x) for x in col])
  else:
   lo,hi=min(col),max(col);columns.append([(x-lo)/(hi-lo) for x in col])
 return np.array(columns).T if columns else np.zeros((len(raw),0)),np.array(nominal).T if nominal else np.zeros((len(raw),0))
def covariance(x,c,a,b,length):
 squared=np.zeros((len(a),len(b)))
 for j in range(x.shape[1]):squared+=(x[a,j,None]-x[b,j][None,:])**2
 r=np.sqrt(squared/max(1,x.shape[1]))/length;t=np.sqrt(5)*r;out=(1+t+t*t/3)*np.exp(-t);h=np.zeros_like(out)
 for j in range(c.shape[1]):h+=(c[a,j,None]!=c[b,j][None,:])
 return out*np.exp(-h/max(1,c.shape[1]))
def expected(raw,ids,y,order,direction,length):
 x,c=encode(raw);available=[i for i in order if i not in ids];y=np.asarray(y);v=(y-y.mean())/(y.std() if y.std()>1e-12 else 1);k=covariance(x,c,ids,ids,length)+np.eye(len(ids))*1e-6;cross=covariance(x,c,ids,available,length);mean=cross.T@np.linalg.lstsq(k,v,rcond=None)[0];variance=1-np.sum(cross*np.linalg.lstsq(k,cross,rcond=None)[0],axis=0);sd=np.sqrt(np.maximum(0,variance));delta=(min(v)-mean) if direction=='minimize' else (mean-max(v));ei=[]
 for d,s in zip(delta,sd):
  if s<=1e-12:ei.append(max(d,0));continue
  z=d/s;ei.append(d*(1+math.erf(z/math.sqrt(2)))/2+s*math.exp(-z*z/2)/math.sqrt(2*math.pi))
 return available,mean,sd,np.array(ei)

def source(c,i):
 if 'spec' in c:
  sp=c['spec'];txt=(ROOT/sp['path']).read_text().splitlines();header=next(csv.reader([txt[0]],delimiter=sp['delimiter']));line=c['source_ids'][i];row=dict(zip(header,next(csv.reader([txt[line-1]],delimiter=sp['delimiter']))));raw=row[sp['primary_objective']];assert [float(row[k]) for k in c['names']]==c['x'][i];value=float(raw);status='completed';meta={'source':sp['path'],'source_line':line,'raw_target':raw}
 elif 'source_lines' in c:
  line=c['source_lines'][i];row=next(csv.reader([(ROOT/c['source_path']).read_text().splitlines()[line-1]]));raw=row[30]
  if raw=='':return None,'invalid_source',{}
  value=float(raw);status='completed';meta={'source':c['source_path'],'source_line':line,'raw_target':raw}
 else:
  n=c['sources'][i];r=read(ROOT/n);assert (r['framework'],r['workload'],r['datasize'])==('hadoop',c['app'],'bigdata') and type(r['completed']) is bool
  if r['completed']:value=min(float(r['elapsed_time']),7200.);status='completed_capped' if float(r['elapsed_time'])>7200 else 'completed'
  else:value=7200.;status='incomplete_failure_penalty'
  meta={'source':n,'source_sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest(),'raw_record':r}
 assert math.isfinite(value) and value>0;return value,status,meta

def verify_collection(jobs,cases,arms,choices,events,completion):
 cursor=0;complete=failed=0;near_ties=[]
 for j in jobs:
  key=j['key'];case=cases[j['case']];c=read(ROOT/j['candidate_path']);p=read(ROOT/j['prefix']);p=p.get('state',p);ids=list(case['ids']);y=list(case['labels']);arm=arms[key];seen=set(ids)
  for step in range(10):
   ch=choices[cursor];e=events[cursor];cursor+=1;assert ch['key']==e['key']==key and ch['step']==step and e['ordinal']==cursor and e['at_unix']>=ch['at_unix'];i=ch['row_id'];assert e['row_id']==i and i not in seen;seen.add(i)
   avail,mean,sd,ei=expected(case['raw_features'],ids,y,p['order'],case['direction'],j['lengthscale']);k=avail.index(i);assert ei[k]>=max(ei)-1e-8,(key,step,i,ei[k],max(ei));
   if k!=int(np.argmax(ei)):near_ties.append({'key':key,'step':step,'selected_row':i,'alternative_argmax_row':avail[int(np.argmax(ei))],'EI_gap':float(max(ei)-ei[k])})
   close(ch['mean'],mean[k]);close(ch['sd'],sd[k]);close(ch['ei'],ei[k]);assert ch['acquired_count']==len(ids)
   value,status,meta=source(c,i);assert e['status']==status and e['value']==value
   for n,v in meta.items():assert e[n]==v
   if status=='invalid_source':assert arm['status']=='unscorable' and arm['target'] is None;failed+=1;break
   ids.append(i);y.append(value)
  else:assert arm['status']=='complete' and len(ids)==20;complete+=1
  assert arm['ids']==ids and arm['labels']==y and arm['remaining_unattempted']==20-len(seen)
  incumbent=(min if case['direction']=='minimize' else max)(y);close(arm['observed_incumbent'],incumbent)
  if arm['status']=='complete':close(arm['target'],incumbent)
 assert cursor==len(events)==len(choices)==completion['acquisition_attempts']<=1400 and complete==completion['complete_arms'] and failed==completion['unscorable_arms'] and complete+failed==140 and completion['wall_seconds']<600
 return near_ties

def verify_report(rows,arms,result):
 for grouping in ['ecosystem','engine']:
  for length,models in result['summary'][grouping].items():
   for model,s in models.items():
    rr=[r for r in rows if r['model']==model];groups={}
    for r in rr:
     g='spark_hadoop_ecosystem' if grouping=='ecosystem' and r['group'] in ['spark','hadoop_mapreduce'] else r['group'];groups.setdefault(g,[]).append(r)
    expected_groups=[]
    for g,data in sorted(groups.items()):
     values=[];gpseq=[];gpad=[];useful=harmful=joint=0
     for r in data:
      t=arms[r['key']+'::gp_'+length]['target']
      if t is None:continue
      sign=1 if r['direction']=='minimize' else -1;gain=sign*(t-r['target'])/t;values.append(gain);gpseq.append(sign*(r['sequential']-t)/r['sequential']);gpad.append(sign*(r['adaptive']-t)/r['adaptive']);useful+=gain>.01;harmful+=gain<-.01;joint+=gain>.01 and r['adaptive_gain']>.01
     full=len(values)==len(data);eg={'group':g,'intended':len(data),'scorable':len(values),'mean_gain':statistics.mean(values) if full else None,'gp_gain_vs_sequential':statistics.mean(gpseq) if full else None,'gp_gain_vs_adaptive':statistics.mean(gpad) if full else None,'useful':useful,'harmful':harmful,'joint_useful':joint};expected_groups.append(eg)
    assert s['groups']==expected_groups
    for k in ['useful','harmful','joint_useful','scorable']:assert s[k]==sum(g[k] for g in expected_groups)
    for aggregate,field in [('family_mean_gain','mean_gain'),('gp_family_gain_vs_sequential','gp_gain_vs_sequential'),('gp_family_gain_vs_adaptive','gp_gain_vs_adaptive')]:
     vals=[g[field] for g in expected_groups]
     if None in vals:assert s[aggregate] is None
     else:close(s[aggregate],statistics.mean(vals))

def main():
 for n,h in read(A/'freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
 jobs=read(A/'jobs.json');cases={c['key']:c for c in read(ROOT/'artifacts/study_v154/prefix_inputs.json')['cases']};arms={j['key']:read(O/'arms'/(j['key']+'.json')) for j in jobs};choices=lines(O/'choices.jsonl');events=lines(O/'acquisitions.jsonl');completion=read(O/'completion.json');rows=read(ROOT/'artifacts/study_v151/inputs.json')['rows'];result=read(O/'comparison.json');nt=verify_collection(jobs,cases,arms,choices,events,completion);verify_report(rows,arms,result);mut=[]
 for name in ['source_value','selected_row','aggregate']:
  ev=copy.deepcopy(events);ch=copy.deepcopy(choices);re=copy.deepcopy(result)
  if name=='source_value':ev[0]['value']+=1
  elif name=='selected_row':ch[0]['row_id']=cases[jobs[0]['case']]['ids'][0]
  else:re['summary']['ecosystem']['1.0']['smollm3_3b']['family_mean_gain']+=.1
  try:
   if name=='aggregate':verify_report(rows,arms,re)
   else:verify_collection(jobs,cases,arms,ch,ev,completion)
  except AssertionError:mut.append({'name':name,'rejected':True})
  else:raise AssertionError('Undetected corruption '+name)
 receipt={'verified':True,'arms':140,'complete_arms':139,'unscorable_arms':1,'charged_attempts':len(events),'near_tie_argmax_differences':len(nt),'near_tie_details':nt,'EI_numerical_absolute_tolerance':1e-8,'mutations':mut,'scope':'independent covariance/lstsq/EI maximum; selected source values including missing target; full acquisition/arm budget and aggregates; no new collection'};(A/'replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
