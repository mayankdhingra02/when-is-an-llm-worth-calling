"""Pure generation-contract checks; no labels or networking."""
IDS='0123456789ABCDEFGHIJ'
def check_payload(payload):
    if payload.get('n_predict')!=1 or payload.get('temperature')!=0 or payload.get('stream') is not False:raise ValueError('Frozen one-token decoding required')
def validate_response(response,used):
    raw=response.get('content')
    if type(raw) is not str or len(raw)!=1 or raw not in IDS or raw in used:raise ValueError('Invalid or duplicate ID')
    if response.get('tokens_predicted')!=1 or response.get('truncated') is not False:raise ValueError('Missing/invalid token count or truncated context')
    return raw
