import sys
import typing as typ

import datasets
import loguru
import pytest

from rosettaeval.loader.factory import adapt_dataset, find_adapter, sample_dataset
from rosettaeval.loader.tasks.adapter import Adapter
from rosettaeval.loader.tasks.medmcqa.base import MedMcQaQueryAdapter
from rosettaeval.loader.tasks.medqa.base import MedQaQueryAdapter

MEDQA_ROW = {
    "uid": "test-0",
    "question": "medqa test",
    "target": 2,
    "answers": ["answer 1", "answer 2", "answer 3", "answer 4"],
}

MEDMCQA_ROW = {
    "id": "test-0",
    "question": "medmcqa test",
    "opa": "answer 1",
    "opb": "answer 2",
    "opc": "answer 3",
    "opd": "answer 4",
    "cop": 2,
}


def mock_huggingface_dataset() -> datasets.Dataset:
    mock_data = {
        "uid": ["test-0", "test-1"],
        "question": ["medqa test", "medqa test"],
        "target": [2, 3],
        "answers": [
            ["answer 1", "answer 2", "answer 3", "answer 4"],
            ["answer 1", "answer 2", "answer 3", "answer 4"],
        ],
    }
    return datasets.Dataset.from_dict(mock_data)


@pytest.mark.parametrize(
    ("row", "expected_adapter"),
    [
        (MEDQA_ROW, MedQaQueryAdapter),
        (MEDMCQA_ROW, MedMcQaQueryAdapter),
    ],
)
def test_find_adapter(row: dict[str, typ.Any], expected_adapter: type[Adapter]) -> None:
    loguru.logger.remove()
    loguru.logger.add(sys.stderr, level="INFO")
    actual = find_adapter(row)
    assert isinstance(actual, expected_adapter)


@pytest.mark.parametrize(
    ("num_samples", "expected_length"),
    [
        (1, 1),
        (100, 2),
    ],
)
def test_sample_dataset(num_samples: int, expected_length: int) -> None:
    dataset = mock_huggingface_dataset()
    actual = sample_dataset(dataset, num_samples)
    assert len(actual) == expected_length


def test_process_dataset() -> None:
    dataset = mock_huggingface_dataset()
    actual = adapt_dataset(dataset)
    assert isinstance(actual, datasets.Dataset)
