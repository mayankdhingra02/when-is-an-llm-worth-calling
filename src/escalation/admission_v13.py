"""Metadata-only eligibility audit. Never opens an objective table or scores a run."""


def exposed_groups(*manifests):
    """Exposure persists across versions, seeds, codecs and later split renaming."""
    groups = set()
    for manifest in manifests:
        for entry in manifest['datasets']:
            if entry.get('split') in ('development', 'test'):
                group = entry.get('system_group')
                if not group:
                    raise ValueError('An exposed dataset lacks a resolved family')
                groups.add(group)
    return groups


def validate_prospective_split(cases, exposed, admitted):
    """Fail closed before new collection; metadata admission does not authorize inference."""
    assignment = {}
    for case in cases:
        group = case.get('system_group')
        split = case.get('split')
        if not group or split not in ('development', 'test'):
            raise ValueError('Resolved family and declared split required')
        if group not in admitted:
            raise ValueError(f'Family lacks prospective admission: {group}')
        if split == 'test' and group in exposed:
            raise ValueError(f'Previously exposed family cannot become untouched test: {group}')
        if group in assignment and assignment[group] != split:
            raise ValueError(f'Variants/seeds of family cross splits: {group}')
        assignment[group] = split
    if not cases:
        raise ValueError('Empty evaluation is not an admitted study')
    return assignment


def audit_registry(registry, exposed, evidence, contract):
    records = []
    for dataset in registry['datasets']:
        name = dataset['dataset_id']
        family = dataset.get('system_group')
        schema = dataset['schema']
        source = evidence.get(name, {})
        # Exact metadata names only: do not infer output size from CPU/energy/PSNR.
        has_size = 'size' in schema['objective_names']
        errors = [e for e in dataset.get('finite_domain_feasibility_exclusions', [])
                  if e != 'previously_exposed_family']
        checks = {
            'resolved_family': bool(family),
            'software_configuration': dataset.get('task_kind') == 'software_configuration',
            'schema_usable': not errors and schema['unique_configurations'] >= 20,
            'explicit_output_size_column': has_size,
            'runtime_and_output_size_documented': bool(source.get('runtime_and_size_documented')),
            'file_compression_task': source.get('task_class') == 'file_compression',
            'family_unexposed': bool(family) and family not in exposed,
            'correctness_evidence_available': source.get('roundtrip_correctness_verified') is True,
            'paired_noise_evidence_available': source.get('paired_noise_available') is True,
            'application_utility_resolved': contract.get('application_utility_approved') is True,
        }
        records.append({
            'dataset_id': name,
            'system_group': family,
            'objective_columns_metadata': schema['objective_names'],
            'has_size_metadata': has_size,
            'source_evidence': source,
            'checks': checks,
            'blockers': [key for key, ok in checks.items() if not ok],
            'prospective_evaluation_ready': all(checks.values()),
            'objective_values_read': False,
        })
    size_rows = [r for r in records if r['has_size_metadata']]
    size_groups = {r['system_group'] for r in size_rows if r['system_group']}
    return {
        'scope': 'metadata-only task admission, not an optimization experiment',
        'records': records,
        'summary': {
            'registry_tables': len(records),
            'size_column_tables': len(size_rows),
            'size_column_families': sorted(size_groups),
            'unexposed_size_column_families': sorted(size_groups - exposed),
            'previously_exposed_families': sorted(exposed),
            'prospective_ready_families': sorted({r['system_group'] for r in records
                                                 if r['prospective_evaluation_ready']}),
        },
        'new_model_requests': 0,
        'new_objective_acquisitions': 0,
        'new_collection_authorized': False,
    }
