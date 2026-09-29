"""Hand-computable synthetic data, excluded from research results."""
import sqlite3
import pytest
from escalation.flights_v88 import SCHEMAS,QUERIES,COLUMNS,integer,dimension,reference,validate_answer

def fixture():
    airlines=[dict(carrier='A',name='Air')]
    airports=[dict(faa='H',name='High',alt=600,tzone='America/NY'),dict(faa='L',name='Low',alt=10,tzone='Europe/London')]
    planes=[dict(tailnum='P',plane_year=1990,manufacturer='Old'),dict(tailnum='N',plane_year=2005,manufacturer='New')]
    specs=[(6,10,'A','P','H'),(6,None,'A','P','H'),(6,-5,'A','P','H'),(5,7,'A','P','H'),(6,4,'A','N','H'),(6,3,'A','X','H'),(6,8,'X','P','H'),(6,9,'A','P','L'),(6,6,'A','P','X')]
    flights=[dict(year=2013,month=m,day=1,arr_delay=d,carrier=a,tailnum=p,origin='NY',dest=t,distance=100) for m,d,a,p,t in specs]
    return dict(flights=flights,airlines=airlines,airports=airports,planes=planes)

def test_independent_python_and_sql_match_hand_answers():
    tables=fixture();expected={'monthly_carriers':[[5,'Air',1,0,7],[6,'Air',7,1,32]],'high_airport_routes':[['NY','H','High',7,700]],'summer_aircraft':[['Old','Air',1,10]]}
    actual=reference(tables['flights'],dimension(tables['airlines'],'carrier'),dimension(tables['airports'],'faa'),dimension(tables['planes'],'tailnum'))
    assert actual=={'input_flights':9,'answers':expected}
    db=sqlite3.connect(':memory:')
    for table,schema in SCHEMAS.items():
        db.execute('CREATE TABLE '+table+'('+','.join(k+' '+t for k,t in schema)+')')
        db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in schema)+')',[[r[k] for k,t in schema] for r in tables[table]])
    for name,query in QUERIES.items():
        cursor=db.execute(query);validate_answer(name,[c[0] for c in cursor.description],cursor.fetchall(),expected[name])
    db.close()

@pytest.mark.parametrize('value',['1.5','NaN','Infinity','-Infinity'])
def test_integer_rejects_bad_source(value):
    with pytest.raises(ValueError):integer(value)

def test_integer_null_and_integral():
    assert integer('NA') is None and integer('') is None and integer('2.0')==2

@pytest.mark.parametrize('rows',[[{'key':None}],[{'key':'a'},{'key':'a'}]])
def test_dimension_keys(rows):
    with pytest.raises(ValueError):dimension(rows,'key')

@pytest.mark.parametrize('rows',[[['Old','Air',1,11]],[['Old','Air',1.0,10]],[['Old','Air',True,10]],[['Old','Air',None,10]],[]])
def test_corrupt_answers(rows):
    with pytest.raises(ValueError):validate_answer('summer_aircraft',COLUMNS['summer_aircraft'],rows,[['Old','Air',1,10]])

def test_corrupt_headers():
    with pytest.raises(ValueError):validate_answer('summer_aircraft',['wrong'],[],[])
