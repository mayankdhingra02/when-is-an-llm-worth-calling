"""Cheap incumbent-neighbor controls; feature/acquired-state inputs only."""
def choose(xs,prefix,state,direction,mode):
 if mode not in ['fixed_prefix_neighbor','adaptive_incumbent_neighbor'] or direction not in ['-','+']:raise ValueError('Unknown control')
 if len(prefix['ids'])!=10 or not 10<=len(state['ids'])<20 or state['ids'][:10]!=prefix['ids'] or state['labels'][:10]!=prefix['labels']:raise ValueError('Invalid shared prefix/budget')
 if len(state['ids'])!=len(state['labels']) or len(set(state['ids']))!=len(state['ids']) or set(state['order'])!=set(range(len(xs))) or len(state['order'])!=len(xs):raise ValueError('Invalid state')
 ref=prefix if mode=='fixed_prefix_neighbor' else state
 anchor=min(range(len(ref['ids'])),key=lambda k:ref['labels'][k][0] if direction=='-' else -ref['labels'][k][0]);anchor=ref['ids'][anchor]
 row=min((i for i in state['order'] if i not in set(state['ids'])),key=lambda i:sum(a!=b for a,b in zip(xs[i],xs[anchor])))
 return {'row_id':row,'anchor_id':anchor,'hamming_distance':sum(a!=b for a,b in zip(xs[row],xs[anchor]))}
