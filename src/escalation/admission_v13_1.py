"""V13.1: conservatively preserve exposure under legacy split spellings."""
from .admission_v13 import audit_registry, validate_prospective_split


def exposed_groups(*manifests):
    groups = set()
    exposed_labels = {'development', 'test', 'heldout_smoke'}
    for manifest in manifests:
        for entry in manifest['datasets']:
            split = entry.get('split')
            if split == 'unused':
                continue
            if split not in exposed_labels:
                raise ValueError(f'Unknown historical split; exposure audit required: {split!r}')
            group = entry.get('system_group')
            if not group:
                raise ValueError('An exposed dataset lacks a resolved family')
            groups.add(group)
    return groups
