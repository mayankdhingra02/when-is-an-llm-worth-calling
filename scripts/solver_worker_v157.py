"""One real, isolated native solve of a fixed N-queens instance; never model output."""
import argparse,json,time,resource

def valid_queens(rows,n):
 return (len(rows)==n and all(type(v) is int and 0<=v<n for v in rows)
         and len(set(rows))==n and len({v+i for i,v in enumerate(rows)})==n
         and len({v-i for i,v in enumerate(rows)})==n)

def solve(engine,config,n,limit):
 started=time.perf_counter();rows=[];stats={}
 if engine=='cvc5':
  import cvc5
  from cvc5 import Kind
  s=cvc5.Solver();s.setLogic('QF_LIA');s.setOption('produce-models','true');s.setOption('seed','0');s.setOption('sat-random-seed','0');s.setOption('tlimit-per',str(round(limit*1000)))
  for key,val in config.items():s.setOption(key,str(val).lower())
  x=[s.mkConst(s.getIntegerSort(),'q'+str(i)) for i in range(n)]
  for v in x:s.assertFormula(s.mkTerm(Kind.GEQ,v,s.mkInteger(0)));s.assertFormula(s.mkTerm(Kind.LT,v,s.mkInteger(n)))
  for vals in [x,[s.mkTerm(Kind.ADD,v,s.mkInteger(i)) for i,v in enumerate(x)],[s.mkTerm(Kind.SUB,v,s.mkInteger(i)) for i,v in enumerate(x)]]:s.assertFormula(s.mkTerm(Kind.DISTINCT,*vals))
  built=time.perf_counter();begin_cpu=time.process_time();r=s.checkSat();end=time.perf_counter();cpu=time.process_time()-begin_cpu;status=str(r)
  if r.isSat():rows=[int(str(s.getValue(v))) for v in x]
  version=s.getVersion().decode()
 elif engine=='ortools':
  import ortools
  from ortools.sat.python import cp_model
  m=cp_model.CpModel();x=[m.new_int_var(0,n-1,'q'+str(i)) for i in range(n)]
  m.add_all_different(x);m.add_all_different([v+i for i,v in enumerate(x)]);m.add_all_different([v-i for i,v in enumerate(x)])
  s=cp_model.CpSolver();s.parameters.num_search_workers=1;s.parameters.random_seed=0;s.parameters.max_time_in_seconds=limit
  for key,val in config.items():setattr(s.parameters,key,val)
  built=time.perf_counter();begin_cpu=time.process_time();r=s.solve(m);end=time.perf_counter();cpu=time.process_time()-begin_cpu;status=s.status_name(r)
  if r in [cp_model.OPTIMAL,cp_model.FEASIBLE]:rows=[s.value(v) for v in x]
  stats={'branches':s.num_branches,'conflicts':s.num_conflicts};version=ortools.__version__
 else:raise ValueError(engine)
 return {'engine':engine,'version':version,'config':config,'n':n,'limit':limit,'status':status,'rows':rows,'correct':valid_queens(rows,n),'solve_seconds':end-built,'solve_cpu_seconds':cpu,'import_build_seconds':built-started,'worker_seconds':time.perf_counter()-started,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'stats':stats}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--engine',required=True);a.add_argument('--config',required=True);a.add_argument('--n',type=int,required=True);a.add_argument('--limit',type=float,required=True);q=a.parse_args()
 print(json.dumps(solve(q.engine,json.loads(q.config),q.n,q.limit),allow_nan=False))
