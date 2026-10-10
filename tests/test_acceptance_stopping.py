from psychocore.acceptance import evaluate_item_acceptance
from psychocore.stopping import standard_error, should_stop


def test_acceptance_passes_valid_item():
    result = evaluate_item_acceptance(150, 0.35)
    assert result["accepted"] is True


def test_acceptance_rejects_small_sample():
    result = evaluate_item_acceptance(40, 0.35)
    assert result["accepted"] is False


def test_acceptance_rejects_low_point_biserial():
    result = evaluate_item_acceptance(150, 0.10)
    assert result["accepted"] is False


def test_standard_error():
    assert abs(standard_error(25) - 0.2) < 1e-9


def test_stopping_rule():
    assert should_stop(25, 10) is True
    assert should_stop(2, 10) is False
    assert should_stop(2, 20) is True
