"""V176: check every numeric cell of the manuscript's result tables against sealed outputs or a recomputation from the case records.

Offline and read-only: no acquisition, model request or network access. Each table's source is listed in TABLE_MAP_V176.md.
Exit status 0 only if every expected table row appears verbatim in paper/overleaf_v173/main.tex.
"""
import json, re, sys
import numpy as np
from collect_smollm_v47 import ROOT, read
import revision_v174 as r174

TEX = ROOT/'paper/overleaf_v173/main.tex'
ARMS = {'smollm3_3b': 'SmolLM3-3B', 'qwen3_8b': 'Qwen3-8B', 'qwen3_14b': 'Qwen3-14B', 'gptoss_a1': 'gpt-oss-120b, draw 1', 'gptoss_a2': 'gpt-oss-120b, draw 2', 'gptoss_b': 'gpt-oss-120b, loop'}
ECO = {'berkeleydb': 'BerkeleyDB', 'dune_hsmgp': 'DUNE', 'hipacc': 'HIPAcc', 'llvm': 'LLVM', 'openvpn': 'OpenVPN', 'sac': 'SaC', 'spark_hadoop': 'Spark/Hadoop'}
CLS = {'random_full': 'Random search', 'adaptive_neighbor': 'Adaptive neighbour', 'gp_ei': 'GP-EI', 'prefix_optimizer': 'Prefix optimizer continued'}

def s2(x):  # signed, two decimals, percent units already applied; zero printed unsigned
    return '0.00' if round(x, 2) == 0 else f'{x:+.2f}'
def neg(x):  # minus sign only (Table 3 style)
    return f'{x:.2f}'

def table(tex, label):
    t = tex[tex.index('\\label{'+label+'}'):]; return t[:t.index('\\end{tabular}')]

def rows_rq1(base):
    cs = list(base.values()); eco = [c['ecosystem'] for c in cs]; out = []
    labels = {**{k: CLS[k] for k in ['random_full', 'adaptive_neighbor', 'gp_ei']}, 'smollm3_3b': 'SmolLM3-3B', 'qwen3_8b': 'Qwen3-8B', 'qwen3_14b': 'Qwen3-14B',
              'gptoss_a1': 'gpt-oss-120b, one-shot, draw 1', 'gptoss_a2': 'gpt-oss-120b, one-shot, draw 2', 'gptoss_b': 'gpt-oss-120b, iterative loop'}
    for a, lab in labels.items():
        g = [r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs]; lg = [r174.logg(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs]
        out.append(f"{lab} & ${neg(100*r174.group_mean(g, eco))}\\%$ & ${neg(100*r174.group_mean(lg, eco))}\\%$ & {sum(x > r174.M for x in g)} & {sum(x < -r174.M for x in g)} & "
                   f"{100*r174.group_mean([max(0., x) for x in g], eco):.2f}\\% \\\\")
    return out

def rows_eco(base):
    cols = ['random_full', 'adaptive_neighbor', 'gp_ei', 'smollm3_3b', 'qwen3_8b', 'qwen3_14b', 'gptoss_a1', 'gptoss_a2', 'gptoss_b']; out = []
    for e, lab in ECO.items():
        cs = [c for c in base.values() if c['ecosystem'] == e]
        out.append(lab+' & '+' & '.join(f"${100*np.mean([r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs]):+.2f}$" for a in cols)+' \\\\')
    return out

def rows_weights(v174):
    W = v174['weighting']; out = []
    for a, lab in {**CLS, **ARMS}.items():
        w = W[a]; lo, hi = w['leave_one_ecosystem_out_range']
        out.append(f"{lab} & ${100*w['equal_ecosystem']:+.2f}$ & ${100*w['equal_engine']:+.2f}$ & ${100*w['case_weighted']:+.2f}$ & ${100*w['equal_ecosystem_excluding_dune']:+.2f}$ & $[{100*lo:+.2f}, {100*hi:+.2f}]$ \\\\")
    return out

def rows_native():
    syn = read(ROOT/'artifacts/study_v170/synthesis.json')['per_application_model']; audit = read(ROOT/'results/v171_audit/audit.json')['native_cohort']
    g = {(r['engine'], r['model']): r for r in syn}; out = []
    # "Robust wins (any arm)" counts robust wins over the reference: every classical arm has none in the whole native cohort,
    # so the per-system count is the LLM arms' robust wins over sequential 3NN (wins over other comparators are not counted).
    assert sum(v['robust_over_sequential'] for m in audit.values() for v in m['arms'].values()) == 0
    labels = {'cvc5': 'cvc5 (N-queens)', 'ortools': 'OR-Tools CP-SAT (N-queens)', 'ripgrep': 'ripgrep', 'hnswlib': 'hnswlib', 'polars': 'Polars', 'xgboost': 'XGBoost'}
    for e, lab in labels.items():
        a, b = g[(e, 'smollm3_3b')], g[(e, 'qwen3_8b')]
        wins = a['robust_wins']['sequential_3nn']+b['robust_wins']['sequential_3nn']
        out.append(f"{lab} & ${100*a['mean_gains']['sequential_3nn']:+.2f}\\%$ & ${100*b['mean_gains']['sequential_3nn']:+.2f}\\%$ & {wins} \\\\")
    return out

def rows_deployable(v174, v175):
    s = v175['selector_vs_reference']; d = v174['deployable_classical_policy']['llm_vs_policy']
    out = [f"Policy vs.\\ sequential 3NN & ${100*s['ecosystem_weighted']:+.2f}\\%$ & ${100*s['case_weighted']:+.2f}\\%$ & {s['better_by_margin']} & {s['worse_by_margin']} \\\\"]
    for a, lab in ARMS.items():
        x = d[a]; out.append(f"{lab} & ${100*x['equal_ecosystem']:+.2f}\\%$ & ${100*x['case_weighted']:+.2f}\\%$ & {x['better_by_margin']} & {x['worse_by_margin']} \\\\")
    return out

def rows_match(v175):
    m = v175['useful_case_matching']; K = ['useful_cases', 'ecosystems_with_useful_case', 'classical_better_or_equal', 'within_margin', 'llm_ahead_by_more_than_margin']
    out = [f"{lab} & "+' & '.join(str(m[a][k]) for k in K)+' \\\\' for a, lab in ARMS.items()]
    out.append(f"Total & {sum(m[a]['useful_cases'] for a in m)} & -- & "+' & '.join(str(sum(m[a][k] for a in m)) for k in K[2:])+' \\\\')
    return out

def rows_rq2(v174):
    P, X = v174['prespecified_baseline_wins'], v174['extended_baseline_wins']; out = []
    for a, lab in ARMS.items():
        pe = P[a]['per_ecosystem']; oth = [e for e in pe if e not in ('hipacc', 'spark_hadoop')]
        cell = lambda es: f"{sum(pe[e]['wins'] for e in es)}/{sum(pe[e]['cases'] for e in es)}"
        ext = X[a]; ext_s = '0' if ext['win_cases'] == 0 else f"{ext['ecosystems_with_win']} ({ext['win_cases']} case{'s' if ext['win_cases'] > 1 else ''})"
        out.append(f"{lab} & {cell(['hipacc'])} & {cell(['spark_hadoop'])} & {cell(oth)} & {P[a]['ecosystems_with_win']} & {ext_s} \\\\")
    return out

def rows_rq4(v174):
    R = v174['routers_all_arms']; C = read(ROOT/'results/v154_controllers/comparison.json')['models']['ecosystem']; M = ['smollm3_3b', 'qwen3_8b']
    def calls(x): return str(int(x)) if float(x).is_integer() else f'{x:.2f}'
    out = []
    for p, lab in [('never', 'Never call'), ('always', 'Always call'), ('selected_predictor', 'Benefit predictor (inner-CV selection)'), ('ridge_extended_q80', 'Ridge, 18 features, 80th percentile'),
                   ('tree_extended_q80', 'Regression tree, 80th percentile'), ('uncertainty_q80', 'Bootstrap uncertainty, 80th percentile')]:
        x = [R[m]['policies'][p] for m in M]; out.append(f"{lab} & {x[0]['calls']} & {x[1]['calls']} & ${s2(100*x[0]['equal_ecosystem_gain'])}\\%$ & ${s2(100*x[1]['equal_ecosystem_gain'])}\\%$ \\\\")
    for p, lab in [('bora_1.0', 'BORA-inspired checkpoint rule'), ('rank_expected_1.0', 'Rank-reliability rule (expected calls)')]:
        x = [C[m][p] for m in M]; out.append(f"{lab} & {calls(x[0]['calls'])} & {calls(x[1]['calls'])} & ${s2(100*x[0]['family_mean_gain'])}\\%$ & ${s2(100*x[1]['family_mean_gain'])}\\%$ \\\\")
    out.append(f"Hindsight oracle & -- & -- & ${s2(100*R[M[0]]['oracle_equal_ecosystem'])}\\%$ & ${s2(100*R[M[1]]['oracle_equal_ecosystem'])}\\%$ \\\\")
    return out

def rows_routers_strong(v174):
    R = v174['routers_all_arms']; out = []
    for a in ['qwen3_14b', 'gptoss_a1', 'gptoss_a2', 'gptoss_b']:
        P = R[a]['policies']; f = lambda p: f"${s2(100*P[p]['equal_ecosystem_gain'])}\\%$ ({P[p]['calls']})"
        out.append(f"{ARMS[a]} & {len(R[a]['groups_with_useful_gt_1pct'])} & {f('selected_predictor')} & {f('ridge_extended_q80')} & {f('uncertainty_q80')} & ${s2(100*R[a]['oracle_equal_ecosystem'])}\\%$ \\\\")
    return out

def rows_ops(v174, v175):
    O, A = v174['operations'], v175['accounting']['rows']; out = []
    for a, inv in [('smollm3_3b', '1 (interrupted)'), ('qwen3_8b', '0'), ('qwen3_14b', '0')]:
        o = O[a]; fb = f"{o['fallback_cases']} case" if o['fallback_cases'] == 1 else str(o['fallback_cases'])
        out.append(f"{ARMS[a]} & {o['logical_requests']} & 0 & -- & {inv} & {fb} & {o['mean_request_seconds']:.1f}\\,s & -- \\\\")
    for a in ['gptoss_a1', 'gptoss_a2', 'gptoss_b']:
        o, x = O[a], A[a]; inv = f"{x['invalid_responses']} (truncated)" if x['invalid_responses'] else '0'; fb = f"{x['fallbacks']} rounds" if a == 'gptoss_b' else str(x['fallbacks'])
        out.append(f"{ARMS[a]} & {x['planned_calls']} & {x['retry_calls']} & {x['rate_limited_attempts']} & {inv} & {fb} & {o['mean_seconds_per_200']:.1f}\\,s & \\${o['reported_cost_usd']:.2f} \\\\")
    return out

def rows_cohort(base):
    labels = {'berkeleydb': ('BerkeleyDB (C)', 'DeepPerf / SPLConqueror', 'time (min.)'), 'dune_hsmgp': ('DUNE', 'DeepPerf / SPLConqueror', 'time (min.)'),
              'hipacc': ('HIPAcc', 'DeepPerf / SPLConqueror', 'time (min.)'), 'llvm': ('LLVM', 'DeepPerf / SPLConqueror', 'time (min.)'), 'sac': ('SaC', 'DeepPerf / SPLConqueror', 'time (min.)'),
              'openvpn': ('OpenVPN', 'Performance Evolution', 'throughput (max.)'), 'spark': ('Spark', 'Tuneful', 'duration (min.)'), 'hadoop_mapreduce': ('Hadoop MapReduce', 'Scout', 'capped duration (min.)')}
    task = lambda k: re.sub(r'_(11|23|37|53|71)(?=(_normal)?$)', '', k); out = []
    for e, (lab, src, obj) in labels.items():
        cs = [c for c in base.values() if c['engine'] == e]
        out.append(f"{lab} & {src} & {obj} & {len({task(c['key']) for c in cs})} & {len(cs)} \\\\")
    out.append(f"Total & & & & {len(base)} \\\\")
    return out

def text_phrases(base, v174, v175):
    """Headline numbers quoted in the running text, recomputed from the case records or read from sealed outputs."""
    cs = list(base.values()); eco = [c['ecosystem'] for c in cs]; W = v174['weighting']; M = r174.M
    def g(ref, a, c): return r174.gain(c['raw'][ref], c['raw'][a], c['direction'])
    def pair(ref, a): x = [g(ref, a, c) for c in cs]; return sum(v > M for v in x), sum(v < -M for v in x)
    means = [-100*W[a]['equal_ecosystem'] for a in r174.LLM]
    hr = [100*r174.group_mean([max(0., g('sequential_3nn', a, c)) for c in cs], eco) for a in ['qwen3_14b', 'gptoss_a1', 'gptoss_a2', 'gptoss_b']]
    disagree = sum(abs(g('gptoss_a1', 'gptoss_a2', c)) > M for c in cs)
    b11 = base['spark::bayes_11']; m = v175['useful_case_matching']
    return [f"by {min(means):.1f}\\% to {max(means):.1f}\\%", f"gained {100*W['gptoss_b']['case_weighted']:.1f}\\%",
            f"In {sum(v['classical_better_or_equal'] for v in m.values())} of the {sum(v['useful_cases'] for v in m.values())} arm--case pairs",
            f"(log-ratio ${100*W['gptoss_b']['case_weighted_log']:+.2f}\\%$)", f"GP-EI gains a similar {100*W['gp_ei']['case_weighted']:.2f}\\%",
            f"Hindsight headroom for these arms is {min(hr):.2f}--{max(hr):.2f}\\%", f"disagreed by more than 1\\% in {disagree} of 70 cases",
            "Qwen3-14B was more than 1\\% better than the earlier 8B draw in {} cases and worse in {}".format(*pair('qwen3_8b', 'qwen3_14b')),
            "more than 1\\% better than Qwen3-8B in {} cases and worse in {}".format(*pair('qwen3_8b', 'gptoss_a1')),
            "({} cases better and {} worse)".format(*pair('gptoss_a1', 'gptoss_b')),
            f"It beat the reference by {100*g('sequential_3nn', 'gptoss_a1', b11):.1f}\\% in both one-shot draws" if round(g('sequential_3nn', 'gptoss_a1', b11), 3) == round(g('sequential_3nn', 'gptoss_a2', b11), 3) else 'MISMATCH draws',
            f"It beat the reference by {100*g('sequential_3nn', 'gptoss_b', b11):.1f}\\% in the loop, and GP-EI by {100*g('gp_ei', 'gptoss_b', b11):.0f}\\%"]

def main():
    tex = TEX.read_text(); base = r174.load_cases(); v174 = read(ROOT/'results/v174_revision/analysis.json'); v175 = read(ROOT/'results/v175_revision/analysis.json')
    checks = {'tab:cohort': rows_cohort(base), 'tab:rq1': rows_rq1(base), 'tab:eco': rows_eco(base), 'tab:weights': rows_weights(v174), 'tab:native': rows_native(),
              'tab:deployable': rows_deployable(v174, v175), 'tab:match': rows_match(v175), 'tab:rq2': rows_rq2(v174), 'tab:rq4': rows_rq4(v174),
              'tab:routers-strong': rows_routers_strong(v174), 'tab:ops': rows_ops(v174, v175)}
    report = {}; bad = []
    for label, rows in checks.items():
        t = table(tex, label); miss = [r for r in rows if r not in t]; report[label] = {'rows_checked': len(rows), 'missing': miss}; bad += [(label, r) for r in miss]
    phrases = text_phrases(base, v174, v175); miss = [p for p in phrases if p not in tex]; bad += [('text', p) for p in miss]
    if miss: report['text'] = {'rows_checked': len(phrases), 'missing': miss}
    print(json.dumps({'tables_checked': len(checks), 'rows_checked': sum(len(r) for r in checks.values()), 'text_phrases_checked': len(phrases), 'mismatches': len(bad),
                      'detail': {k: v for k, v in report.items() if v['missing']}}, indent=1))
    sys.exit(1 if bad else 0)

if __name__ == '__main__': main()
