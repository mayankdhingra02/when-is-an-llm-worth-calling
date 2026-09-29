"""A single deployable continuation; never reads another arm's outcomes."""
from escalation.transfer_v41 import rank

def portfolio(c,prefix,pool,acquire):
 if len(prefix.ids)!=10 or len(set(prefix.ids))!=10:raise ValueError('ten distinct prefix observations required')
 state=prefix.clone();fixed=rank(c,prefix,pool)
 if len(fixed)<10:raise ValueError('insufficient remaining pool')
 trace=[]
 for turn in range(10):
  mode='batch' if turn%2==0 else 'sequential'
  row=next(i for i in fixed if i not in state.ids) if mode=='batch' else rank(c,state,[i for i in state.order if i not in state.ids])[0]
  value=acquire(row);state.observe(row,value,c.directions);trace.append(dict(turn=turn,mode=mode,row=row,label=list(value)))
 assert len(state.ids)==len(set(state.ids))==20
 return state,trace
