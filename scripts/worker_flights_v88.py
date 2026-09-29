"""Offline DuckDB execution on real CC0 data; no TPC extension/package execution."""
import argparse,csv,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.flights_v88 import SCHEMAS,CONFIGS,QUERIES,COLUMNS,typed_rows,dimension,reference,validate_answer
DATA=ROOT/'data/flights_v88';ART=ROOT/'artifacts/study_v88';RUNTIME=ROOT/'.local-runtime/duckdb-v87';DB=DATA/'flights.duckdb'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def connection(readonly=False):
    sys.path.insert(0,str(RUNTIME));import duckdb
    assert duckdb.__version__=='1.4.4'
    c=duckdb.connect(str(DB),read_only=readonly,config={'threads':1,'memory_limit':'512MiB','extension_directory':str(ROOT/'.local-runtime/duckdb-v88-extensions'),'autoinstall_known_extensions':'false','autoload_known_extensions':'false','temp_directory':str(DATA/'tmp')})
    c.execute("SET home_directory='"+str(DATA).replace("'","''")+"'");return c

def prepare():
    assert not DB.exists() and not (DATA/'normalized').exists();start=time.monotonic();norm=DATA/'normalized';norm.mkdir();counts={};dimensions={}
    def normalize(table):
        with (norm/(table+'.csv')).open('w',newline='') as out:
            w=csv.writer(out);names=[x[0] for x in SCHEMAS[table]];w.writerow(names);n=0
            for row in typed_rows(DATA/(table+'.csv'),table):
                n+=1;w.writerow(['NA' if row[k] is None else row[k] for k in names]);yield row
            counts[table]=n
    for table,key in [('airlines','carrier'),('airports','faa'),('planes','tailnum')]:dimensions[table]=dimension(normalize(table),key)
    answers=reference(normalize('flights'),dimensions['airlines'],dimensions['airports'],dimensions['planes']);assert counts['flights']==answers['input_flights']==336776
    write(DATA/'query_contract.json',{'queries':QUERIES,'columns':COLUMNS,'expected':answers,'row_counts':counts,'reference':'Independent Python csv/dictionary aggregation; no DuckDB objective SQL during setup'})
    c=connection()
    for table,columns in SCHEMAS.items():
        types='{'+','.join("'"+k+"':'"+t+"'" for k,t in columns)+'}';path=str(norm/(table+'.csv')).replace("'","''")
        c.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv('{path}',header=true,auto_detect=false,columns={types},nullstr='NA')")
        assert c.execute('SELECT count(*) FROM '+table).fetchone()[0]==counts[table]
    c.execute('CHECKPOINT');c.close()
    write(ART/'data_manifest.json',{'database':str(DB.relative_to(ROOT)),'sha256':sha(DB),'bytes':DB.stat().st_size,'row_counts':counts,'query_contract_sha256':sha(DATA/'query_contract.json'),'setup_seconds':time.monotonic()-start,'objective_queries_executed':0,'normalized_files':{str(p.relative_to(ROOT)):sha(p) for p in norm.glob('*.csv')}})

def trial(index,out):
    cfg=CONFIGS[index];contract=read(DATA/'query_contract.json');assert contract['queries']==QUERIES and contract['columns']==COLUMNS;c=connection(True)
    c.execute('SET enable_external_access=false');c.execute('SET threads='+str(cfg['threads']));c.execute("SET disabled_optimizers='"+cfg['disabled_optimizers']+"'")
    settings=dict(c.execute("SELECT name,value FROM duckdb_settings() WHERE name IN ('threads','disabled_optimizers','memory_limit','enable_external_access','autoinstall_known_extensions','autoload_known_extensions')").fetchall())
    assert settings['threads']==str(cfg['threads']) and settings['disabled_optimizers']==cfg['disabled_optimizers'] and settings['memory_limit']=='512.0 MiB'
    assert all(settings[k]=='false' for k in ['enable_external_access','autoinstall_known_extensions','autoload_known_extensions']);write(out/'settings.json',settings)
    plans={name:c.execute('EXPLAIN '+query).fetchall() for name,query in QUERIES.items()};write(out/'plans.json',plans)
    rows=[];total=0.;checking=0.
    for rep in range(19):
        for name,query in QUERIES.items():
            t=time.perf_counter();cursor=c.execute(query);answer=cursor.fetchall();seconds=time.perf_counter()-t
            cols=[r[0] for r in cursor.description];t=time.perf_counter();validate_answer(name,cols,answer,contract['expected']['answers'][name]);checking+=time.perf_counter()-t
            if rep>=3:total+=seconds
            rows.append({'repetition':rep,'query':name,'scored':rep>=3,'seconds':seconds,'columns':cols,'rows':answer});write(out/'answers.json',rows)
    c.close();write(out/'result.json',{'configuration':cfg,'query_seconds':total,'answer_check_seconds':checking,'warmup_suites':3,'scored_suites':16,'scored_queries':48,'checked_queries':57,'answers_sha256':sha(out/'answers.json')})
def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--config',type=int,choices=range(3));p.add_argument('--out');a=p.parse_args()
    if a.prepare:prepare()
    else:assert a.config is not None and a.out;trial(a.config,Path(a.out))
if __name__=='__main__':main()
