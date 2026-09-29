"""Checks for the V175 second-revision analysis: synthetic logic tests plus manuscript/analysis agreement.
Synthetic fixtures never enter research aggregates."""
import json, re, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts'))
from revision_v175 import trivial_gap

ANALYSIS = ROOT/'results/v175_revision/analysis.json'
PAPER = ROOT/'paper/overleaf_v173/main.tex'

def pol(always, ctl):
    W = ['ecosystem_weighted', 'engine_weighted', 'case_weighted']
    return {'policies': {'never': {w: 0. for w in W}, 'always': {w: always for w in W}, 'ctl': {w: ctl for w in W}}}

def test_trivial_gap_uses_better_trivial_policy():
    out = trivial_gap({'a': pol(-.05, .001), 'b': pol(.004, .001)})
    assert out['a']['case_weighted']['better_trivial'] == 'never' and out['a']['case_weighted']['controller_minus_better_trivial'] == pytest.approx(.001)
    assert out['b']['case_weighted']['better_trivial'] == 'always' and out['b']['case_weighted']['controller_minus_better_trivial'] == pytest.approx(-.003)

@pytest.mark.skipif(not ANALYSIS.exists(), reason='analysis not generated')
def test_manuscript_matches_analysis():
    a = json.loads(ANALYSIS.read_text()); tex = PAPER.read_text()
    names = {'smollm3_3b': 'SmolLM3-3B', 'qwen3_8b': 'Qwen3-8B', 'qwen3_14b': 'Qwen3-14B', 'gptoss_a1': 'gpt-oss-120b, draw 1', 'gptoss_a2': 'gpt-oss-120b, draw 2', 'gptoss_b': 'gpt-oss-120b, loop'}
    table = tex[tex.index(r'\label{tab:match}'):]; table = table[:table.index(r'\end{tabular}')]
    for k, v in a['useful_case_matching'].items():
        row = f"{names[k]} & {v['useful_cases']} & {v['ecosystems_with_useful_case']} & {v['classical_better_or_equal']} & {v['within_margin']} & {v['llm_ahead_by_more_than_margin']} \\\\"
        assert row in table, row
    tot = [sum(v[x] for v in a['useful_case_matching'].values()) for x in ['useful_cases', 'classical_better_or_equal', 'within_margin', 'llm_ahead_by_more_than_margin']]
    assert f"Total & {tot[0]} & -- & {tot[1]} & {tot[2]} & {tot[3]} \\\\" in table and f"In {tot[1]} of the {tot[0]} arm--case pairs" in tex
    s = a['selector_vs_reference']
    assert f"Policy vs.\\ sequential 3NN & ${s['ecosystem_weighted']*100:+.2f}\\%$ & ${s['case_weighted']*100:+.2f}\\%$ & {s['better_by_margin']} & {s['worse_by_margin']} \\\\".replace('+', '') in tex or \
           f"Policy vs.\\ sequential 3NN & ${s['ecosystem_weighted']*100:.2f}\\%$ & ${s['case_weighted']*100:.2f}\\%$ & {s['better_by_margin']} & {s['worse_by_margin']} \\\\" in tex
    gaps = [x[w]['controller_minus_better_trivial'] for x in a['controller_vs_better_trivial_policy'].values() for w in x]
    assert max(gaps) < .0003 and 'by as much as 0.03 percentage points' in tex and 'more than 0.02 percentage points' not in tex
    for w, text in [('engine_weighted', '0.019'), ('case_weighted', '0.011')]:  # paper states these relative to never calling
        assert f"{max(x[w]['best_controller_gain'] for x in a['controller_vs_better_trivial_policy'].values())*100:.3f}" == text
    b = a['controller_vs_better_trivial_policy']['gptoss_b']['case_weighted']
    assert b['better_trivial'] == 'always' and f"{b['better_trivial_gain']*100:.2f}\\%" in tex and round(-b['controller_minus_better_trivial']*100, 2) >= .38
    checkpoint = [p[w] for m in a['checkpoint_rules_reaggregation_v154'].values() for n, p in m.items() if n.startswith(('bora', 'rank_draw', 'rank_expected')) for w in ['ecosystem_weighted', 'engine_weighted', 'case_weighted']]
    assert max(checkpoint) < 0
    c = a['accounting']['cost_usd']
    assert f"\\${c['ledger_total']:.2f} in total" in tex and f"\\${c['reported_arms_total']:.3f}" in tex
    assert f"\\${c['preflight_and_provider_probes']+c['aborted_first_attempt_recorded']:.3f}" in tex
    assert a['cross_check'] == {'llm_ahead_counts_match_v174_baseline_set_wins': True, 'router_ecosystem_values_match_v174': True}
