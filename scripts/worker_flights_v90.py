"""No-network native trial with exact V88 independent reference answers."""
import argparse,time
from pathlib import Path
from worker_flights_v88 import connection,read,write,sha,DATA,QUERIES,COLUMNS,validate_answer
from escalation.flights_v90 import CONFIGS,WARMUP,SCORED,CHECKED

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=int,choices=range(12),required=True);p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out)
    cfg=CONFIGS[a.config];contract=read(DATA/'query_contract.json');assert contract['queries']==QUERIES and contract['columns']==COLUMNS;c=connection(True)
    c.execute('SET enable_external_access=false');c.execute('SET threads='+str(cfg['threads']));c.execute("SET disabled_optimizers='"+cfg['disabled_optimizers']+"'")
    settings=dict(c.execute("SELECT name,value FROM duckdb_settings() WHERE name IN ('threads','disabled_optimizers','memory_limit','enable_external_access','autoinstall_known_extensions','autoload_known_extensions')").fetchall())
    assert settings['threads']==str(cfg['threads']) and set(filter(None,settings['disabled_optimizers'].split(',')))==set(filter(None,cfg['disabled_optimizers'].split(','))) and settings['memory_limit']=='512.0 MiB'
    assert all(settings[k]=='false' for k in ['enable_external_access','autoinstall_known_extensions','autoload_known_extensions']);write(out/'settings.json',settings)
    write(out/'plans.json',{name:c.execute('EXPLAIN '+q).fetchall() for name,q in QUERIES.items()})
    rows=[];total=0.;checking=0.
    for rep in range(WARMUP+SCORED):
        for name,query in QUERIES.items():
            start=time.perf_counter();cursor=c.execute(query);answer=cursor.fetchall();seconds=time.perf_counter()-start
            columns=[r[0] for r in cursor.description];start=time.perf_counter();validate_answer(name,columns,answer,contract['expected']['answers'][name]);checking+=time.perf_counter()-start
            if rep>=WARMUP:total+=seconds
            rows.append({'repetition':rep,'query':name,'scored':rep>=WARMUP,'seconds':seconds,'columns':columns,'rows':answer})
    c.close();write(out/'answers.json',rows);write(out/'result.json',{'configuration':cfg,'query_seconds':total,'answer_check_seconds':checking,'checked_queries':CHECKED,'scored_queries':SCORED*3,'answers_sha256':sha(out/'answers.json')})
if __name__=='__main__':main()
