"""Hand-computable synthetic evaluation fixtures; no measured model results."""
from fractions import Fraction as F
import pytest
from escalation.pool_analysis_v44 import contrast, aggregate, unique_requests, observed_total, selected_rows


@pytest.mark.parametrize("direction,reference,treatment,ceiling,expected", [
    ("-", 100, 95, 90, F(1, 2)), ("+", 100, 105, 110, F(1, 2)),
    ("-", 100, 110, 90, F(-1)), ("+", 100, 90, 110, F(-1)),
])
def test_capture_keeps_harm_signed(direction, reference, treatment, ceiling, expected):
    r = contrast(F(reference), F(treatment), F(ceiling), direction)
    assert r["signed_capture"] == expected
    assert r["positive_capture"] == max(F(0), expected)


@pytest.mark.parametrize("direction,treatment,ceiling", [("-", 100, 100), ("-", 120, 110), ("+", 100, 100), ("+", 80, 90)])
def test_capture_is_undefined_without_positive_headroom(direction, treatment, ceiling):
    r = contrast(F(100), F(treatment), F(ceiling), direction)
    assert r["signed_capture"] is r["positive_capture"] is None


@pytest.mark.parametrize("direction,treatment,ceiling", [("-", 80, 90), ("+", 120, 110)])
def test_impossible_super_ceiling_result_rejected(direction, treatment, ceiling):
    with pytest.raises(ValueError): contrast(F(100), F(treatment), F(ceiling), direction)


def test_family_aggregation_preserves_denominators_and_harm():
    rows = []
    for group, treatment in (("a", 95), ("b", 110)):
        for _ in range(5):
            r = contrast(F(100), F(treatment), F(90), "-")
            rows.append({"system_group": group, "attains_ceiling": False,
                         "exact": {k: str(v) if v is not None else None for k, v in r.items() if k != "attains_ceiling"}})
    result = aggregate(rows, {"a", "b"})
    assert result["equal_family_mean"] == pytest.approx(-.025)
    assert result["mean_signed_capture_on_positive_headroom_cases"] == pytest.approx(-.25)
    assert result["hindsight_positive_gain_capture_ratio"] == pytest.approx(.25)
    assert result["positive_headroom_cases"] == 10
    with pytest.raises(ValueError): aggregate(rows[:-1], {"a", "b"})
    with pytest.raises(ValueError): aggregate(rows, {"a"})


def test_unknown_usage_not_zero_and_duplicate_request_not_deduplicated():
    assert observed_total([{"tokens": 7}, {"tokens": None}], "tokens") is None
    assert observed_total([{"tokens": 7}, {}], "tokens") is None
    assert observed_total([{"tokens": 7}, {"tokens": 3}], "tokens") == 10
    for value in (-1, float("nan"), float("inf"), True):
        with pytest.raises(ValueError): observed_total([{"tokens": value}], "tokens")
    with pytest.raises(ValueError): unique_requests([{"request_id": 1}, {"request_id": 1}])
    with pytest.raises(ValueError): unique_requests([{"request_id": True}])


def test_actual_selection_and_fallback_must_agree_with_response():
    pool = {"mapping": {str(i): i + 10 for i in range(10)}}
    prompt = {"pool": pool, "fallback_rows": list(range(20, 30))}
    valid = {"status": "response", "raw_output": "\n".join(str(i) for i in range(10))}
    assert selected_rows(valid, prompt, {"fallback": None}) == list(range(10, 20))
    with pytest.raises(ValueError): selected_rows(valid, prompt, {"fallback": "spurious"})
    for invalid in ({"status": "error", "raw_output": None}, {"status": "response", "raw_output": "0\n0"}):
        assert selected_rows(invalid, prompt, {"fallback": "invalid response"}) == prompt["fallback_rows"]
        with pytest.raises(ValueError): selected_rows(invalid, prompt, {"fallback": None})


def test_empty_headroom_aggregate_reports_null():
    r = contrast(F(100), F(100), F(100), "-")
    rows = [{"system_group": "a", "attains_ceiling": True,
             "exact": {k: str(v) if v is not None else None for k, v in r.items() if k != "attains_ceiling"}} for _ in range(5)]
    result = aggregate(rows, {"a"})
    assert result["positive_headroom_cases"] == 0
    assert result["mean_signed_capture_on_positive_headroom_cases"] is None
    assert result["hindsight_positive_gain_capture_ratio"] is None


def test_driver_refuses_missing_real_collection_without_writes(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend("scripts")
    from analyze_pool_models_v44 import main
    monkeypatch.chdir(tmp_path)
    with pytest.raises(RuntimeError, match="No real V44 collection"):
        main()
    assert list(tmp_path.iterdir()) == []
