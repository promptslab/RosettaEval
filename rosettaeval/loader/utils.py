import secrets
import typing

import datasets


def get_first_row(dataset: datasets.Dataset | datasets.DatasetDict) -> dict[str, typing.Any]:
    """Get the first row of a dataset."""
    if isinstance(dataset, datasets.DatasetDict):
        # Choose a random split from the DatasetDict
        split_names = list(dataset.keys())
        random_split = secrets.choice(split_names)
        dataset = dataset[random_split]
    return dataset[0]
