"""Fixed repetition schedule and descriptive timing comparison, no optimizer."""
import random
import statistics

def schedule(settings, repetitions=20, seed=2026092532):
    if repetitions != 20 or not settings or len({s['config_id'] for s in settings}) != len(settings):
        raise ValueError('Twenty rounds of distinct configurations required')
    rng = random.Random(seed); result = []
    for repetition in range(repetitions):
        block = sorted(settings, key=lambda s:s['config_id']); rng.shuffle(block)
        for setting in block:
            result.append({'trial_id':len(result),'repetition':repetition,'setting':setting})
    return result

def compare(cheap, reference):
    if len(cheap)!=20 or len(reference)!=20 or any(v<=0 for v in cheap+reference):
        raise ValueError('Twenty positive paired observations required')
    gains=[(r-c)/r for c,r in zip(cheap,reference)]
    ordered=sorted(gains)
    def percentile(p):
        position=(len(ordered)-1)*p; lower=int(position); upper=min(lower+1,len(ordered)-1)
        return ordered[lower]+(position-lower)*(ordered[upper]-ordered[lower])
    return {'relative_gain_of_medians':(statistics.median(reference)-statistics.median(cheap))/statistics.median(reference),
        'median_paired_relative_gain':statistics.median(gains),'paired_p10':percentile(.1),'paired_p90':percentile(.9),
        'rounds_faster':sum(v>0 for v in gains),'rounds_equal':sum(v==0 for v in gains),'rounds_slower':sum(v<0 for v in gains)}
