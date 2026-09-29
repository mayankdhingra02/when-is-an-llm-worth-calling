"""Acquired-only H2 model interface and explicit bounded authorization checks."""
import json,math
from .h2_v84 import CONFIGS,SEEDS,PRIOR,choose,incumbent,guard
ARMS=['rf_lcb','llm','prior']

def vectors():return [[c['mask'],int(c['recompile']),c['analyze_sample']] for c in CONFIGS]

def messages(observations):
    rows=[];seen=set()
    for o in observations:
        cid=o['config_id'];loss=o['query_seconds']
        if type(cid) is not int or cid in seen or not 0<=cid<len(CONFIGS):raise ValueError('Invalid acquired candidate')
        if type(loss) not in (int,float) or not math.isfinite(loss) or loss<=0:raise ValueError('Invalid acquired time')
        seen.add(cid);rows.append({'configuration':vectors()[cid],'query_seconds':loss})
    return [{'role':'system','content':'Choose one unmeasured H2 database configuration to minimize aggregate query time. Return only the JSON integer array [index_mask,recompile,analyze_sample]. Do not repeat an observed configuration.'},
      {'role':'user','content':'H2 2.3.232, fresh in-memory database with 100000 rows. Columns id,grp,acct,score,tick,amount: for i=0..99999, id=tick=i, grp=(i*37)%97, acct=(i*29)%997, score=(i*13)%10000, amount=(i*7919)%100000. All queries return COUNT(*) and SUM(amount). Three predicates: grp=? AND score BETWEEN ? AND ?; acct=? AND grp=?; tick>=? AND tick<?. For t=0..15: first uses grp=(t*7)%97, score lower=(t*431)%9000 and upper=lower+500; second acct=(t*43)%997 and grp=(t*11)%97; third lower=(t*5701)%90000 and upper=lower+1000. Each query suite runs these48queries;32warm-up suites precede128scored suites. Exact answers are checked. Primary metric is aggregate scored-query seconds, lower is better. Index creation/analyze and process time are recorded separately, excluded from this objective. Query cache fixed8; result reuse disabled; automatic analyze disabled. Primary-key index on id always exists. index_mask enables at most3of6additional indexes: bit0=grp, bit1=acct, bit2=score, bit3=(grp,score), bit4=(acct,grp), bit5=tick. recompile is0or1 (always recompile statements when1). analyze_sample is0,100,2000or10000;0skips explicit ANALYZE. All336legal combinations form the domain. You only have outcomes for the acquired configurations below; no unacquired timing values are available. Observations in acquisition order: '+json.dumps(rows,separators=(',',':'))+'. Propose one new legal configuration.'}]

def authorize(record,digest,argument):
    if record is None:raise PermissionError('No explicit new 35-request allowance recorded')
    expected={'granted':True,'frozen_scope_sha256':digest,'max_generation_requests':35,'max_physical_trials':115,'max_stage_seconds':1800,'max_new_download_bytes':0,'max_external_spend_usd':0}
    if argument!=digest or any(record.get(k)!=v for k,v in expected.items()):raise PermissionError('Approval does not match frozen scope')
    if not isinstance(record.get('user_message'),str) or not record['user_message'].strip():raise PermissionError('Missing user authorization provenance')

def check_cfg(cfg):
    expected={'max_generation_requests':35,'max_physical_evaluations':115,'max_stage_seconds':1800,'max_output_tokens':64,'context_tokens':4096,'host':'127.0.0.1','port':18492,'retries':0,'max_external_spend_usd':0,'max_new_download_bytes':0,'allow_paid_api':False}
    if any(cfg.get(k)!=v for k,v in expected.items()):raise ValueError('Unsafe or changed experiment scope')
