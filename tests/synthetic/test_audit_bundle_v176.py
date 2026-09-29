"""Checks for the V176 audit-bundle tooling. Synthetic fixtures only; nothing enters research aggregates."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts'))
from verify_bundle_v176 import category
from check_tables_v176 import s2

def test_exclusion_categories_are_path_based():
    assert category('models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf') == 'model_weights'
    assert category('.local-runtime/llama-b11146/llama-server') == 'third_party_runtimes_and_native_builds'
    assert category('.native-v160/search_corpus/README.rst') == 'third_party_runtimes_and_native_builds'
    assert category('output/llm_escalation_v45_review.zip') == 'earlier_packaged_bundles'
    assert category('results/v67_candidates_physical/x.json') == 'earlier_or_unrelated_iterations'
    assert category('artifacts/study_v1/freeze.json') == 'earlier_or_unrelated_iterations'
    assert category('CLAUDE_HANDOFF.md') == 'workflow_notes'
    assert category('results/v173_models/B1/responses.jsonl') == 'other_files_not_needed_to_reproduce_the_paper'

def test_signed_formatting_prints_zero_unsigned():
    assert s2(0.001) == '0.00' and s2(-0.004) == '0.00' and s2(0.52) == '+0.52' and s2(-2.95) == '-2.95'

def test_offline_guard_blocks_network():
    code = "import socket\ntry:\n    socket.create_connection(('127.0.0.1', 9), timeout=1)\nexcept RuntimeError as e:\n    print('blocked', e)\n"
    env = dict(os.environ, PYTHONPATH=str(ROOT/'scripts/guard_v176'))
    p = subprocess.run([sys.executable, '-c', code], env=env, capture_output=True, text=True, timeout=30)
    assert p.stdout.startswith('blocked offline guard'), p.stdout+p.stderr

def test_relocation_recovers_one_root(tmp_path, monkeypatch):
    import verify_v172_relocated_v176 as rel
    for s in ['A', 'B']:
        d = tmp_path/'results/v172_models'/s; d.mkdir(parents=True)
        (d/'runtime.json').write_text(json.dumps({'command': ['/orig/root/.local-runtime/llama-b11146/llama-server', '-m', 'x']}))
    monkeypatch.setattr(rel, 'ROOT', tmp_path); monkeypatch.setattr(rel, 'STAGES', {'A': 0, 'B': 0})
    assert rel.recorded_root() == Path('/orig/root')
    (tmp_path/'results/v172_models/B/runtime.json').write_text(json.dumps({'command': ['/other/.local-runtime/llama-b11146/llama-server']}))
    with pytest.raises(AssertionError): rel.recorded_root()
