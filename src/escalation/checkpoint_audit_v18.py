"""Retrospective evaluator only. Never import into optimizer/router feature code."""
import math


def decompose(labels, prefix, arm):
    """Attribute feasible runtime savings with one fixed reference denominator."""
    if not labels or any(len(y)!=2 or not all(math.isfinite(v) and v>0 for v in y) for y in labels):
        raise ValueError('Positive finite runtime/size vectors required')
    ids=prefix['ids'];final=arm['ids']
    if len(ids)!=10 or len(set(ids))!=10 or len(final)!=20 or len(set(final))!=20:
        raise ValueError('Exact unique10/20 budgets required')
    if any(type(i) is not int or not 0<=i<len(labels) for i in final) or final[:10]!=ids:
        raise ValueError('Invalid or mismatched saved prefix')
    if prefix['labels']!=[labels[i] for i in ids] or arm['labels']!=[labels[i] for i in final]:
        raise ValueError('Saved labels differ from source')
    ref=prefix['reference_row']
    if ids[0]!=ref or prefix['size_cap']!=labels[ref][1] or arm['size_cap']!=prefix['size_cap']:
        raise ValueError('Reference and acquired size cap must match')
    cap=prefix['size_cap'];feasible=[i for i,y in enumerate(labels) if y[1]<=cap]
    def best(indices):return min((labels[i][0],i) for i in indices if labels[i][1]<=cap)
    reference=labels[ref][0];checkpoint,checkpoint_id=best(ids);cheap,cheap_id=best(final);ideal,ideal_id=best(feasible)
    if (cheap,cheap_id)!=(arm['best_feasible_ms'],arm['best_row']):raise ValueError('Incumbent mismatch')
    if not 0<ideal<=cheap<=checkpoint<=reference:raise ValueError('Incumbent monotonicity violated')
    before=(reference-checkpoint)/reference;after=(checkpoint-cheap)/reference;remaining=(cheap-ideal)/reference
    total=(reference-ideal)/reference
    if not math.isclose(before+after+remaining,total,rel_tol=1e-12,abs_tol=1e-12):raise ValueError('Decomposition identity violated')
    return {'candidate_count':len(labels),'feasible_count':len(feasible),'size_cap_bytes':cap,
        'reference_ms':reference,'checkpoint_ms':checkpoint,'cheap_ms':cheap,'hindsight_ms':ideal,
        'reference_id':ref,'checkpoint_best_id':checkpoint_id,'cheap_best_id':cheap_id,'hindsight_best_id':ideal_id,
        'reference_headroom':total,'checkpoint_headroom':(checkpoint-ideal)/checkpoint,
        'cheap_headroom':(cheap-ideal)/cheap,
        'pre_checkpoint_saved_fraction_of_reference':before,
        'continuation_saved_fraction_of_reference':after,
        'remaining_fraction_of_reference':remaining,
        'cheap_continuation_improved':cheap<checkpoint,
        'checkpoint_at_recorded_optimum':checkpoint==ideal}
