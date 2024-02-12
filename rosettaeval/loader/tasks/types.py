import typing as typ

import datasets
from pydantic import BeforeValidator

ANSWER_CHOICES_LETTERS = typ.Literal["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

Y = dict[str, typ.Any] | datasets.Dataset | datasets.DatasetDict
Methods = typ.Literal["direct", "fewshots"]


def _answer_to_int(x: int | ANSWER_CHOICES_LETTERS) -> int:
    """Convert an answer to an integer."""
    if isinstance(x, int):
        return x
    values = typ.get_args(ANSWER_CHOICES_LETTERS)
    if x not in values:
        msg = f"Invalid answer: `{x}`"
        raise ValueError(msg)
    return values.index(x)


AnswerIndex = typ.Annotated[
    int,
    BeforeValidator(lambda x: _answer_to_int(x)),
]
