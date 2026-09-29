"""Shared V172 helpers: frozen-input verification, stage metadata and the decision rule."""
from collect_smollm_v47 import ROOT, read, sha
A = ROOT/'artifacts/study_v172'; M = ROOT/'results/v172_models'; E = ROOT/'results/v172_eval'
# Stages of record (amendment 1: A1R replaces the failed A1 for Qwen3-14B split 1).
STAGES = {'A1R': ('qwen3_14b', 1), 'A2': ('qwen3_14b', 2), 'B1': ('qwen3_8b_redraw', 1), 'B2': ('qwen3_8b_redraw', 2)}
FAILED_STAGES = {'A1': 'pre-start port bind failure (OSError 48); zero requests; superseded by A1R under amendment 1'}
ORDER = ['P', 'A1', 'A1R', 'A2', 'B1', 'B2']

def config(): return read(ROOT/'configs/study_v172.json')

def freeze_names():
    """freeze.json then freeze_amendmentN.json in numeric order, discovered on disk (no list to edit per amendment)."""
    return ['freeze.json']+sorted((p.name for p in A.glob('freeze_amendment*.json')), key=lambda n: int(n[len('freeze_amendment'):-len('.json')]))

FREEZES = freeze_names()

def frozen_hashes():
    """Original pre-collection freeze overlaid, in order, by each amendment freeze (later entries supersede)."""
    merged = {}
    for name in freeze_names():
        if (A/name).exists(): merged.update(read(A/name)['sha256'])
    return merged

def verify_freeze():
    merged = frozen_hashes()
    for n, h in merged.items():
        if sha(ROOT/n) != h: raise ValueError('Changed frozen input: '+n)
    return merged

def stage_info(stage, cfg):
    arm, split = STAGES[stage]; a = cfg['arms'][arm]
    return {'stage': stage, 'arm': arm, 'split': split, 'model_key': a['model_key'], 'seed_field': a['seed_field']}

def require_previous(stage, cfg=None):
    for s in ORDER[:ORDER.index(stage)]:
        if not (M/s/'summary.json').exists(): raise RuntimeError('Previous stage not ended: '+s)

def decision(ecosystems_14b, ecosystems_redraw, threshold=2):
    """Frozen V172 primary rule plus attribution amendment."""
    if ecosystems_14b < threshold:
        return 'close_router_question'
    if ecosystems_redraw < threshold:
        return 'scale_consistent_headroom_router_question_testable'
    return 'headroom_also_under_8b_resampling_scale_not_supported'
