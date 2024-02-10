import random
import typing as typ

import datasets
import loguru

from rosetta_eval.loader.adapters import KNOWN_ADAPTERS, Adapter
from rosetta_eval.loader.types import Y
from rosetta_eval.loader.utils import get_first_row


def find_adapter(row: dict[str, typ.Any]) -> Adapter:
    """Find an adapter for a row."""
    for v in KNOWN_ADAPTERS:
        if v.can_handle(v.input_model, row):
            if loguru.logger.level("DEBUG"):
                translated_row = v().translate_row(row)
                loguru.logger.info(f"Found adapter: {v.__name__}")
                loguru.logger.debug(f"Input data: {row}")
                loguru.logger.debug(f"Output data: {translated_row.model_dump()}")
            return v()
    msg = f"Could not find an adapter for row: `{row}`"
    raise ValueError(msg)


def sample_dataset(
    dataset: datasets.Dataset,
    num_samples: int,
    seed: int | None = 42,
) -> datasets.Dataset:
    """Sample a dataset."""
    random.seed(seed)
    max_samples = min(num_samples, len(dataset))
    indices = random.sample(range(len(dataset)), max_samples)
    return dataset.select(indices)


def process_dataset(
    dataset: datasets.Dataset,
    num_proc: int | None = 1,
    num_samples: int | None = None,
    seed: int | None = 42,
) -> Y:
    """Translate a dataset using an `Adapter`."""
    row = get_first_row(dataset)
    adapter = find_adapter(row)

    if num_samples:
        dataset = sample_dataset(dataset, num_samples, seed)

    return adapter.translate(x=dataset, map_kwargs={"num_proc": num_proc})


def load_dataset(
    name_or_path: str,
    split: str,
    subset: str | None = None,
    num_proc: int | None = 1,
    num_samples: int | None = None,
    seed: int | None = 42,
    **kws: typ.Any,
) -> Y:
    """Load a multiple choice huggingface dataset."""
    loguru.logger.info(f"Loading dataset: {name_or_path}")
    dataset = datasets.load_dataset(name_or_path, subset, split=split, **kws)
    if isinstance(dataset, datasets.DatasetDict | datasets.IterableDataset | datasets.IterableDatasetDict):
        msg = f"Cannot handle dataset of type `{type(dataset)}`"
        raise NotImplementedError(msg)

    return process_dataset(dataset, num_proc, num_samples, seed)
