"""Post-hoc exhaustive finite-case routing ceiling; no policy training or calls."""
from fractions import Fraction
import json,os
from collect_smollm_v47 import ROOT,read,write,sha

def envelope(rows):
    if not rows or len(rows)>20:raise ValueError('Bounded nonempty cohort required')
    counts={g:sum(r['system_group']==g for r in rows) for g in {r['system_group'] for r in rows}}
    gains=[];weights=[]
    for r in rows:
        ref=Fraction(str(r['references']['full_sequential_3nn']));target=Fraction(str(r['target']))
        if ref<=0 or target<=0:raise ValueError('Positive minimization targets required')
        gains.append((ref-target)/ref);weights.append(Fraction(1,len(counts)*counts[r['system_group']]))
    masks=[]
    for mask in range(1<<len(rows)):
        value=sum((w*g for i,(w,g) in enumerate(zip(weights,gains)) if mask>>i&1),Fraction(0))
        masks.append({'mask':format(mask,f'0{len(rows)}b'),'calls':mask.bit_count(),'gain_numerator':value.numerator,'gain_denominator':value.denominator,'mean_relative_gain':float(value)})
    by_calls=[]
    for n in range(len(rows)+1):
        vals=[Fraction(m['gain_numerator'],m['gain_denominator']) for m in masks if m['calls']==n]
        by_calls.append({'calls':n,'policies':len(vals),'best_gain':float(max(vals)),'worst_gain':float(min(vals))})
    return {'case_order':[r['key'] for r in rows],'bit_order':'rightmost bit selects case_order[0]',
      'masks':masks,'envelope':by_calls,'policies':len(masks),'positive_gain_policies':sum(m['gain_numerator']>0 for m in masks),
      'zero_gain_policies':sum(m['gain_numerator']==0 for m in masks),
      'observed_hindsight_gain':float(sum((w*max(g,Fraction(0)) for w,g in zip(weights,gains)),Fraction(0))),
      'never_dominates_all_nonempty_policies_in_quality_and_calls':all(g<=0 for g in gains)}

def main():
    source=ROOT/'results/v129_analysis/comparison.json';rows=read(source)['cases'];assert len(rows)==10
    result=envelope(rows);result.update(source_sha256=sha(source),scope='Post-hoc diagnostic of all deterministic decisions on these10exposed paired cases;not learned,deployable,held-out or a population bound',new_model_requests=0,new_objective_acquisitions=0)
    write(ROOT/'results/v129_analysis/policy_envelope.json',result)
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'artifacts/study_v129/mpl_cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    es=result['envelope'];fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
    ax.fill_between([e['calls'] for e in es],[100*e['worst_gain'] for e in es],[100*e['best_gain'] for e in es],alpha=.2,label='All decision masks')
    ax.plot([e['calls'] for e in es],[100*e['best_gain'] for e in es],marker='o',label='Hindsight upper reference')
    ax.axhline(0,color='black',linewidth=.8);ax.set_xlabel('Selected LLM escalations out of ten cases');ax.set_ylabel('Gain over never-escalate (%)')
    ax.set_title('Post-hoc ceiling on these ten observed cases');ax.legend(fontsize=8)
    fig.savefig(ROOT/'results/v129_analysis/policy_envelope.png',dpi=150,metadata={'Software':'llm-escalation-study V129'});plt.close(fig)
    text=f'''# V129 post-hoc routing ceiling

Exhaustively evaluated all {result['policies']} binary escalation masks using the actual paired model/sequential3NN targets, with equal family weights. This is an evaluator-only, post-hoc diagnostic; no controller was fitted and no new model or objective calls were made. Fractions compute gains from serialized positive targets without a floating-point tie tolerance.

Policies with positive quality gain: **{result['positive_gain_policies']}**. Policies with exactly zero gain: **{result['zero_gain_policies']}** (including never-escalate). The hindsight oracle's mean gain is **{100*result['observed_hindsight_gain']:.3f}%**. Never-escalate dominates every nonempty mask in quality and model-call count: **{result['never_dominates_all_nonempty_policies_in_quality_and_calls']}**. Tied-quality masks still make extra model requests. Random mixtures of these masks cannot have positive expected quality gain because expectations are convex combinations of the same nonpositive gains.

This result is restricted to these ten observed paired outcomes, this adapter/model/budget and these two exposed families. It is not a population guarantee, an untouched-system test, a calibrated risk bound or a claim about all LLM optimizers. The original six-family V127 study retained a positive exception and used a different output contract; it is not silently pooled into this certificate. No statistical independence is assigned to seeds. No native-time, energy or dollar saving is inferred.

![Hindsight envelope](../results/v129_analysis/policy_envelope.png)

Evidence: results/v129_analysis/policy_envelope.json retains every mask, exact rational gain, call count, case order and source hash. Run `.venv/bin/python scripts/policy_envelope_v129.py` to reproduce. This diagnostic explains why fitting a benefit router on these outcomes cannot demonstrate a quality gain over never-escalate; it does not validate any learned router.
'''
    (ROOT/'reports/policy_envelope_v129.md').write_text(text)
    print({k:result[k] for k in ['policies','positive_gain_policies','zero_gain_policies','observed_hindsight_gain','never_dominates_all_nonempty_policies_in_quality_and_calls']})
if __name__=='__main__':main()
