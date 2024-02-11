import abc
import typing as typ

import datasets
import pydantic

from rosettaeval.loader.tasks.models import MultipleChoiceModel
from rosettaeval.loader.tasks.types import Y

Im = typ.TypeVar("Im", bound=pydantic.BaseModel)
Om = typ.TypeVar("Om", bound=MultipleChoiceModel)
DictStrKey: typ.TypeAlias = dict[str, typ.Any]


class AsDict:
    """A callable that converts a pydantic model to a dict."""

    def __init__(self, fn: typ.Callable[[DictStrKey], pydantic.BaseModel]) -> None:
        self.fn = fn

    def __call__(self, x: DictStrKey) -> DictStrKey:
        """Call the inner functions and dump to dict."""
        m = self.fn(x)
        return m.model_dump()


class Adapter(typ.Generic[Im, Om], abc.ABC):
    """An adapter for a dataset."""

    input_model: type[Im]
    output_model: type[Om]

    @staticmethod
    def can_handle(input_model: type[Im], row: dict[str, typ.Any]) -> bool:
        """Can handle."""
        try:
            input_model(**row)  # Assumes input_model is defined at the class level or inherited
        except pydantic.ValidationError:
            return False
        else:
            return True

    def translate(self, x: Y, map_kwargs: dict | None = None) -> Y:
        """Translate a row, dataset or dataset dict."""
        map_kwargs = map_kwargs or {}
        if isinstance(x, datasets.Dataset):
            return self.translate_dset(x, **map_kwargs)
        if isinstance(x, datasets.DatasetDict):
            return datasets.DatasetDict({k: self.translate_dset(v, **map_kwargs) for k, v in x.items()})
        if isinstance(x, dict):
            return self.translate_row(x).model_dump()
        msg = f"Cannot adapt input of type `{type(x)}`"
        raise TypeError(msg)

    def translate_row(self, row: dict[str, typ.Any]) -> Om:
        """Translate a row."""
        raise NotImplementedError

    def translate_dset(self, dset: datasets.Dataset, **kwargs: typ.Any) -> datasets.Dataset:
        """Translate a dataset."""
        return dset.map(
            AsDict(self.translate_row),
            remove_columns=dset.column_names,
            desc=f"Adapting dataset using {self.__class__}",
            **kwargs,
        )
