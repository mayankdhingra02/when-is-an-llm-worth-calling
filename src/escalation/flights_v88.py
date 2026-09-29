"""Real-data query contract and independent Python reference; no objective labels."""
import csv
from collections import defaultdict
from decimal import Decimal
SCHEMAS={
 'flights':[('year','INTEGER'),('month','INTEGER'),('day','INTEGER'),('arr_delay','INTEGER'),('carrier','VARCHAR'),('tailnum','VARCHAR'),('origin','VARCHAR'),('dest','VARCHAR'),('distance','INTEGER')],
 'airlines':[('carrier','VARCHAR'),('name','VARCHAR')],
 'airports':[('faa','VARCHAR'),('name','VARCHAR'),('alt','INTEGER'),('tzone','VARCHAR')],
 'planes':[('tailnum','VARCHAR'),('plane_year','INTEGER'),('manufacturer','VARCHAR')]}
CONFIGS=[{'name':'one_thread','threads':1,'disabled_optimizers':''},{'name':'four_threads','threads':4,'disabled_optimizers':''},{'name':'join_order_off','threads':1,'disabled_optimizers':'join_order'}]
QUERIES={
 'monthly_carriers':"""SELECT f.month,a.name,COUNT(*) AS flights,
 SUM(CASE WHEN f.arr_delay IS NULL THEN 1 ELSE 0 END) AS missing_arrival_delay,
 SUM(CASE WHEN f.arr_delay>0 THEN f.arr_delay ELSE 0 END) AS positive_delay_minutes
 FROM flights f JOIN airlines a ON f.carrier=a.carrier
 GROUP BY f.month,a.name ORDER BY f.month,a.name""",
 'high_airport_routes':"""SELECT f.origin,f.dest,d.name,COUNT(*) AS flights,SUM(f.distance) AS distance_miles
 FROM flights f JOIN airports d ON f.dest=d.faa WHERE d.alt>500
 GROUP BY f.origin,f.dest,d.name ORDER BY f.origin,f.dest,d.name""",
 'summer_aircraft':"""SELECT p.manufacturer,a.name,COUNT(*) AS flights,SUM(f.arr_delay) AS delay_minutes
 FROM flights f JOIN planes p ON f.tailnum=p.tailnum JOIN airlines a ON f.carrier=a.carrier
 JOIN airports d ON f.dest=d.faa
 WHERE f.month BETWEEN 6 AND 8 AND f.arr_delay>0 AND p.plane_year<2000 AND d.tzone LIKE 'America/%'
 GROUP BY p.manufacturer,a.name ORDER BY p.manufacturer,a.name"""}
COLUMNS={'monthly_carriers':['month','name','flights','missing_arrival_delay','positive_delay_minutes'],'high_airport_routes':['origin','dest','name','flights','distance_miles'],'summer_aircraft':['manufacturer','name','flights','delay_minutes']}

def integer(text):
    if text in ['NA','']:return None
    d=Decimal(text)
    if not d.is_finite() or d!=d.to_integral_value():raise ValueError('Noninteger source value')
    return int(d)

def typed_rows(path,table):
    with path.open(newline='') as f:
        reader=csv.DictReader(f)
        for raw in reader:
            row={}
            for name,kind in SCHEMAS[table]:
                source='year' if table=='planes' and name=='plane_year' else name
                v=raw[source];row[name]=integer(v) if kind=='INTEGER' else None if v in ['NA',''] else v
            yield row

def dimension(rows,key):
    result={}
    for row in rows:
        if row[key] is None or row[key] in result:raise ValueError('Null/duplicate dimension key')
        result[row[key]]=row
    return result

def reference(flights,airlines,airports,planes):
    q1=defaultdict(lambda:[0,0,0]);q2=defaultdict(lambda:[0,0]);q3=defaultdict(lambda:[0,0]);count=0
    for f in flights:
        count+=1;a=airlines.get(f['carrier']);d=airports.get(f['dest']);p=planes.get(f['tailnum']);delay=f['arr_delay']
        if a:
            z=q1[f['month'],a['name']];z[0]+=1;z[1]+=int(delay is None);z[2]+=max(0,delay) if delay is not None else 0
        if d and d['alt'] is not None and d['alt']>500:
            assert f['distance'] is not None;z=q2[f['origin'],f['dest'],d['name']];z[0]+=1;z[1]+=f['distance']
        if a and d and p and 6<=f['month']<=8 and delay is not None and delay>0 and p['plane_year'] is not None and p['plane_year']<2000 and d['tzone'] is not None and d['tzone'].startswith('America/'):
            assert p['manufacturer'] is not None;z=q3[p['manufacturer'],a['name']];z[0]+=1;z[1]+=delay
    return {'input_flights':count,'answers':{name:[list(k)+v for k,v in sorted(q.items())] for name,q in zip(QUERIES,[q1,q2,q3])}}

def validate_answer(name,columns,rows,expected):
    if list(columns)!=COLUMNS[name]:raise ValueError('Column mismatch')
    if any(type(v) not in [str,int] for row in rows for v in row):raise ValueError('Unexpected answer type')
    if [list(r) for r in rows]!=expected:raise ValueError('Independent answer mismatch')
