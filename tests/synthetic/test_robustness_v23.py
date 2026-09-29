"""Synthetic arithmetic fixtures; never measured model data."""
import copy
import pytest
from escalation.robustness_v23 import analyze, BASELINES, CONDITIONS

def fixture():
    rows = [{'dataset':'synthetic','system_group':'synthetic','seed':11,'condition':c,'status':'completed',
             'llm_loss': loss, **{b:.1 for b in BASELINES}} for c,loss in zip(CONDITIONS,[.05,.15,.1])]
    return rows, {(r['dataset'],r['seed'],r['condition']) for r in rows}

def test_gain_envelope_sign_flip_and_material_counts():
    rows,expected=fixture();out=analyze(rows,expected);r=out['aggregate']['classical_loss']
    assert r['minimum']==pytest.approx(-.05) and r['maximum']==pytest.approx(.05)
    assert r['mean']==pytest.approx(0) and r['sign_flip']==1 and r['positive_all']==0
    assert r['positive_any']==r['material_any']==1 and r['material_all']==0

def test_ties_and_exact_repeat_do_not_create_benefit_or_extra_cases():
    rows,expected=fixture()
    for r in rows:r['llm_loss']=.1
    rows.append(dict(rows[0],condition='assigned_ids_repeat',llm_loss=-100))
    out=analyze(rows,expected)
    assert out['presentation_count']==3 and out['aggregate']['first_display_loss']['positive_any']==0

@pytest.mark.parametrize('mutation',['missing','duplicate','nan','group','baseline'])
def test_denominator_and_consistency_fail_closed(mutation):
    rows,expected=fixture();rows=copy.deepcopy(rows)
    if mutation=='missing':rows.pop()
    if mutation=='duplicate':rows.append(rows[0])
    if mutation=='nan':rows[0]['llm_loss']=float('nan')
    if mutation=='group':rows[0]['system_group']='other'
    if mutation=='baseline':rows[0]['classical_loss']=.3
    with pytest.raises(ValueError):analyze(rows,expected)

def test_matched_control_changes_are_not_held_constant():
    rows,expected=fixture()
    for row in rows:row['first_display_loss']=row['llm_loss']
    out=analyze(rows,expected)
    assert out['aggregate']['first_display_loss']['minimum']==out['aggregate']['first_display_loss']['maximum']==0
