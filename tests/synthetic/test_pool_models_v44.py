"""Authorization fixtures only; never run model inference."""
import pytest


def test_requires_new_exact_approval_before_enabling_requests(monkeypatch):
    monkeypatch.syspath_prepend("scripts")
    from run_pool_models_v44 import authorized_config
    fixture = {"granted": True, "additional_requests": 60, "request_cap": 350,
        "runtime_cap_seconds": 3600, "stage_seconds": 450, "max_new_vectors": 600,
        "new_downloads": 0, "external_spend_usd": 0, "request_retries": 0,
        "protocol_freeze_sha256": "synthetic", "user_authorization": "SYNTHETIC ONLY"}
    c = authorized_config(fixture, "synthetic")
    assert c["inference"]["max_new_model_requests"] == 350
    assert c["inference"]["allow_paid_api"] is False
    assert c["resources"]["max_experiment_runtime_minutes"] == 60
    for key, bad in (("granted", False), ("request_cap", 351), ("stage_seconds", 451),
                     ("external_spend_usd", 1), ("request_retries", 1),
                     ("user_authorization", ""), ("protocol_freeze_sha256", "changed")):
        with pytest.raises(PermissionError):
            authorized_config({**fixture, key: bad}, "synthetic")
