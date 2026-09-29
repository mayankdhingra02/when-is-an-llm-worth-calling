"""Post-hoc behavioral-rule comparison; no model, labels, or controller features."""
IDS='0123456789ABCDEFGHIJ'
RULES=('display_prefix','lowest_ids','highest_ids','endpoint_sequence')

def predictions(display):
    if len(display)!=20 or set(display)!=set(IDS):raise ValueError('Exact20 distinct IDs required')
    ranks=[IDS.index(i) for i in display];direction=1 if ranks[1]>ranks[0] else -1
    continuation=[ranks[0]+direction*i for i in range(10)]
    endpoint=[IDS[i] for i in continuation] if all(0<=i<20 for i in continuation) else None
    return {'display_prefix':list(display[:10]),'lowest_ids':list(IDS[:10]),'highest_ids':list(IDS[::-1][:10]),'endpoint_sequence':endpoint}

def compare(display,output):
    if len(output)!=10 or len(set(output))!=10 or not set(output)<=set(IDS):raise ValueError('Invalid measured ID sequence')
    return {name:{'defined':p is not None,'sequence_match':p==output,'set_match':p is not None and set(p)==set(output)} for name,p in predictions(display).items()}

def nonmonotone_assignment():
    return [IDS[i] for pair in zip(range(10),range(19,9,-1)) for i in pair]
