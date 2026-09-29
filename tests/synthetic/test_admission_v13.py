"""Synthetic admission fixtures; excluded from all measured research outcomes."""
import pytest
from escalation.admission_v13 import audit_registry, exposed_groups, validate_prospective_split


def test_variant_and_seed_cannot_cross_split():
    with pytest.raises(ValueError, match='cross splits'):
        validate_prospective_split([
            {'system_group': 'codec', 'split': 'development', 'variant': 'a', 'seed': 11},
            {'system_group': 'codec', 'split': 'test', 'variant': 'b', 'seed': 71},
        ], set(), {'codec'})


def test_old_test_and_development_families_stay_exposed():
    exposed = exposed_groups({'datasets': [
        {'system_group': 'codec', 'split': 'test'},
        {'system_group': 'database', 'split': 'development'},
        {'system_group': 'unused', 'split': 'unused'},
    ]})
    assert exposed == {'codec', 'database'}
    for family in exposed:
        with pytest.raises(ValueError, match='Previously exposed'):
            validate_prospective_split([{'system_group': family, 'split': 'test'}], exposed, exposed)


def test_unadmitted_and_empty_evaluations_fail_closed():
    with pytest.raises(ValueError, match='lacks prospective admission'):
        validate_prospective_split([{'system_group': 'fresh', 'split': 'test'}], set(), set())
    with pytest.raises(ValueError, match='Empty evaluation'):
        validate_prospective_split([], set(), set())


def test_valid_grouped_split_allows_repeated_seeds():
    cases = [{'system_group': group, 'split': split, 'seed': seed}
             for group, split in [('dev', 'development'), ('new', 'test')]
             for seed in (11, 23)]
    assert validate_prospective_split(cases, {'dev'}, {'dev', 'new'}) == {'dev': 'development', 'new': 'test'}


def fixture(column='size'):
    return {'datasets': [{'dataset_id': 'synthetic/codec', 'system_group': 'codec',
        'task_kind': 'software_configuration', 'finite_domain_feasibility_exclusions': [],
        'schema': {'objective_names': ['performance', column], 'unique_configurations': 30}}]}


def test_output_size_does_not_prove_video_quality_or_correctness():
    audit = audit_registry(fixture(), set(), {'synthetic/codec': {
        'runtime_and_size_documented': True, 'task_class': 'video_encoding'}}, {})
    row = audit['records'][0]
    assert row['checks']['explicit_output_size_column']
    assert not row['prospective_evaluation_ready']
    assert 'file_compression_task' in row['blockers']
    assert 'correctness_evidence_available' in row['blockers']


def test_generic_metric_names_are_not_guessed_as_output_size():
    audit = audit_registry(fixture('PSNR-'), set(), {}, {})
    assert audit['summary']['size_column_tables'] == 0
    assert not audit['new_collection_authorized']
    assert audit['new_objective_acquisitions'] == 0
