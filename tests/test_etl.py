
import pandas as pd
import pytest

from scripts.etl import clean_dataset


def test_missing_required_column_raises_error(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    pd.DataFrame({
        "learner_id": ["L1"],
        "item_id": [1],
    }).to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="missing columns"):
        clean_dataset(input_file, output_file, "test")


def test_invalid_correct_value_is_removed(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    pd.DataFrame({
        "learner_id": ["L1", "L2"],
        "item_id": [1, 2],
        "skill_id": [1, 1],
        "response": ["A", "B"],
        "correct": [1, 3],
        "latency_ms": [100, 200],
    }).to_csv(input_file, index=False)

    clean_dataset(input_file, output_file, "test")
    result = pd.read_csv(output_file)

    assert len(result) == 1
    assert result["correct"].tolist() == [1]


def test_negative_latency_is_removed(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    pd.DataFrame({
        "learner_id": ["L1", "L2"],
        "item_id": [1, 2],
        "skill_id": [1, 1],
        "response": ["A", "B"],
        "correct": [1, 0],
        "latency_ms": [100, -5],
    }).to_csv(input_file, index=False)

    clean_dataset(input_file, output_file, "test")
    result = pd.read_csv(output_file)

    assert len(result) == 1
    assert result["latency_ms"].tolist() == [100]
