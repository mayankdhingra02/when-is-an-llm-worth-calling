"""Offline native DuckDB worker, generator guarded by explicit EULA grant."""
import argparse,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.duckdb_v87 import CONFIGS,QUERY_IDS,authorize,validate_answer
ART=ROOT/'artifacts/study_v87';DATA=ROOT/'data/duckdb_v87';RUNTIME=ROOT/'.local-runtime/duckdb-v87'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def permission():
    p=ART/'eula_approval.json';authorize(read(p) if p.exists() else None,(ROOT/'artifacts/sources/v87/DBGEN_LICENSE').read_bytes())
def connection(db,readonly=False):
    sys.path.insert(0,str(RUNTIME));import duckdb
    assert duckdb.__version__=='1.4.4';home=ROOT/'.local-runtime/duckdb-v87-home'
    c=duckdb.connect(str(db),read_only=readonly,config={'threads':1,'memory_limit':'512MiB','extension_directory':str(home/'extensions'),'autoinstall_known_extensions':'false','autoload_known_extensions':'false','temp_directory':str(DATA/'tmp')})
    c.execute("SET home_directory = '"+str(home).replace("'","''")+"'")
    return c

def prepare():
    permission();assert not DATA.exists();DATA.mkdir(parents=True);start=time.monotonic();db=DATA/'tpch_sf01.duckdb';c=connection(db)
    extension=ROOT/'.local-runtime/duckdb-v87-tpch.duckdb_extension';assert extension.is_file()
    # Default signature validation stays on; no unsigned-extension bypass.
    c.execute("LOAD '"+str(extension).replace("'","''")+"'")
    c.execute('SET enable_external_access=false')
    queries=dict(c.execute('SELECT query_nr, query FROM tpch_queries() WHERE query_nr IN (4,12,13) ORDER BY query_nr').fetchall())
    answers=dict(c.execute('SELECT query_nr, answer FROM tpch_answers() WHERE scale_factor=0.1 AND query_nr IN (4,12,13) ORDER BY query_nr').fetchall())
    assert sorted(queries)==sorted(answers)==QUERY_IDS
    write(DATA/'query_contract.json',{'queries':queries,'answers':answers,'scale_factor':0.1,'query_ids':QUERY_IDS,'owner_version':'1.4.4'})
    c.execute('CALL dbgen(sf=0.1)')
    counts={t:c.execute('SELECT count(*) FROM '+t).fetchone()[0] for t in ['customer','lineitem','nation','orders','part','partsupp','region','supplier']}
    assert counts['customer']==15000 and counts['orders']==150000 and counts['part']==20000 and counts['supplier']==1000 and counts['region']==5 and counts['nation']==25
    c.execute('CHECKPOINT');c.close()
    write(ART/'data_manifest.json',{'database':str(db.relative_to(ROOT)),'bytes':db.stat().st_size,'sha256':sha(db),'table_rows':counts,'data_generator_seconds':time.monotonic()-start,'objective_queries_executed':0,'query_contract_sha256':sha(DATA/'query_contract.json'),'extension_sha256':sha(extension),'runtime_native_sha256':{str(p.relative_to(ROOT)):sha(p) for p in RUNTIME.glob('*.so')}})

def trial(index,out):
    permission();contract=read(DATA/'query_contract.json');cfg=CONFIGS[index];db=DATA/'tpch_sf01.duckdb';c=connection(db,True)
    c.execute('SET enable_external_access=false');c.execute('SET threads='+str(cfg['threads']));c.execute("SET disabled_optimizers='"+cfg['disabled_optimizers']+"'")
    settings=dict(c.execute("SELECT name,value FROM duckdb_settings() WHERE name IN ('threads','disabled_optimizers','memory_limit','enable_external_access','autoinstall_known_extensions','autoload_known_extensions')").fetchall())
    assert settings['threads']==str(cfg['threads']) and settings['disabled_optimizers']==cfg['disabled_optimizers'] and settings['memory_limit']=='512.0 MiB'
    assert all(settings[k]=='false' for k in ['enable_external_access','autoinstall_known_extensions','autoload_known_extensions']);write(out/'settings.json',settings)
    records=[];total=0.;validation=0.
    for rep in range(19):
        for q in QUERY_IDS:
            start=time.perf_counter();cursor=c.execute(contract['queries'][str(q)]);observed=cursor.fetchall();seconds=time.perf_counter()-start
            cols=[x[0] for x in cursor.description];v=time.perf_counter();canon=validate_answer(contract['answers'][str(q)],cols,observed);validation+=time.perf_counter()-v
            if rep>=3:total+=seconds
            records.append({'repetition':rep,'query_id':q,'scored':rep>=3,'seconds':seconds,'columns':cols,'rows':canon});write(out/'answers.json',records)
    c.close();write(out/'result.json',{'configuration':cfg,'query_seconds':total,'validation_seconds':validation,'warmup_suites':3,'scored_suites':16,'scored_queries':48,'checked_queries':57,'answers_sha256':sha(out/'answers.json')})
def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--config',type=int,choices=range(3));p.add_argument('--out');a=p.parse_args()
    if a.prepare:prepare()
    else:assert a.config is not None and a.out;trial(a.config,Path(a.out))
if __name__=='__main__':main()
