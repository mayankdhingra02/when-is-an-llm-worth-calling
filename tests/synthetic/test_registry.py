import copy,json
import pytest
from escalation.registry import inspect_features,split_groups,validate_assignments
from escalation.study_plan import preflight


def row(group,alias=None):
    return {'system_group':group,'dataset_id':group,'aliases':[alias or group],
            'exclusion_reasons':[],'upstream_path':group+'.csv','path':group+'.csv','sha256':'test',
            'schema':{'feature_matrix_sha256':group}}


def test_registry_never_parses_objective_values(tmp_path):
    p=tmp_path/'fixture.csv'
    p.write_text('flag,real_INDEX,Cost-\n0,1,SECRET\n1,0,DO_NOT_PARSE\n')
    first=inspect_features(p)
    p.write_text('flag,real_INDEX,Cost-\n0,1,999\n1,0,-900\n')
    assert first==inspect_features(p)
    assert first['feature_names']==['flag','real_INDEX']
    assert first['objective_values_inspected'] is False


def test_group_gate_does_not_count_variants_as_systems():
    rows=[row('a') for _ in range(50)]
    assert split_groups(rows)['available']==1
    assert split_groups(rows)['assignments']=={}


def test_split_determinism_alias_and_exposure_guard():
    rows=[row(f'system{i}') for i in range(20)]
    a=split_groups(rows)
    assert a==split_groups(rows[::-1])
    assert list(a['assignments'].values()).count('test')==8
    validate_assignments(rows,a['assignments'])
    with pytest.raises(ValueError):validate_assignments([row('apache')],{'apache':'test'})
    with pytest.raises(ValueError):validate_assignments([row('a','same'),row('b','same')],{'a':'development','b':'test'})
    rows=[row('a'),row('b')];rows[1]['schema']['feature_matrix_sha256']='a'
    with pytest.raises(ValueError):validate_assignments(rows,{'a':'development','b':'test'})


def test_resource_plan_does_not_authorize_larger_run():
    config=json.load(open('configs/study_v4.json'))
    registry={'datasets':[row(f'system{i}') for i in range(20)]}
    result=preflight(config,registry,{'requests':66,'experiment_seconds':1156},
                     {'inference':{'max_new_model_requests':100},'resources':{'max_experiment_runtime_minutes':30}})
    assert result['planned_model_requests']==203
    assert result['planned_new_label_accesses']==6000
    assert not result['ready']
    assert 'proposed_larger_resource_limits_not_authorized' in result['reasons']
