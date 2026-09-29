"""Checks for the V177 audit-bundle tooling. Synthetic and configuration checks only; nothing enters research aggregates."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts'))
import verify_bundle_v177 as vb
import reproduce_bundle_v177 as rb

def test_latest_sealed_manifest_is_v176():
    assert vb.LATEST == 'artifacts/study_v176/evidence_manifest.json'

def test_cited_earlier_studies_are_paper_studies():
    assert {131, 132, 134, 136} <= vb.PAPER_STUDIES
    assert vb.category('results/v131_native/wavpack/raw.json') == 'other_files_not_needed_to_reproduce_the_paper'
    assert vb.category('results/v119_classical/x.json') == 'earlier_or_unrelated_iterations'

def test_suite_includes_cited_experiment_verifiers():
    names = [n for n, *_ in rb.CORE]
    assert 'verify_router_v132' in names and 'verify_feedback_v136' in names

def test_receipt_only_checks_never_claim_a_pass():
    receipts = {k: v for k, v in rb.NOT_IN_BUNDLE.items() if 'receipt' in v}
    assert set(receipts) == {'verify_native_study_v153', 'verify_apps_v168', 'verify_ezr_v169', 'verify_ezr_v170'}
    assert all(v['status'].startswith('not rerun by this offline workflow') for v in receipts.values())
    assert not set(receipts) & {n for n, *_ in rb.CORE}
