"""Exact answer and authorization checks; independent of DuckDB import."""
import csv,hashlib,io
CONFIGS=[{'name':'one_thread','threads':1,'disabled_optimizers':''},{'name':'four_threads','threads':4,'disabled_optimizers':''},{'name':'join_order_off','threads':1,'disabled_optimizers':'join_order'}]
QUERY_IDS=[4,12,13]
def authorize(grant,license_bytes):
    if not isinstance(grant,dict) or grant.get('granted') is not True:raise PermissionError('Explicit TPC EULA authorization required')
    if grant.get('license_sha256')!=hashlib.sha256(license_bytes).hexdigest():raise PermissionError('Authorization does not match inspected EULA')
    if not grant.get('user_message'):raise PermissionError('Actual user message required')

def expected_rows(answer,columns):
    rows=list(csv.reader(io.StringIO(answer),delimiter='|'))
    if not rows or rows[0]!=list(columns):raise ValueError('Expected-answer header mismatch')
    rows=rows[1:]
    if any(len(r)!=len(columns) for r in rows):raise ValueError('Expected-answer shape mismatch')
    return rows

def validate_answer(answer,columns,observed):
    expected=expected_rows(answer,columns)
    # Only string/int columns are admitted for the three count queries.
    if any(type(v) not in [str,int] for r in observed for v in r):raise ValueError('Unexpected result type')
    canonical=[[str(v) for v in r] for r in observed]
    if canonical!=expected:raise ValueError('Exact owner-answer mismatch')
    return canonical
