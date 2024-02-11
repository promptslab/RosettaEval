import typing as typ

import pydantic

from rosettaeval.loader.tasks import adapter, models


class MedQaQueryModel(pydantic.BaseModel):
    """An input query model for MedQa."""

    uid: str = pydantic.Field(..., description="id")
    question: str = pydantic.Field(..., description="question")
    target: int = pydantic.Field(..., description="target")
    answers: list[str] = pydantic.Field(..., description="answers")


class MedQaQueryAdapter(adapter.Adapter[MedQaQueryModel, models.MultipleChoiceModel]):
    """An adapter for multiple-choice datasets."""

    input_model = MedQaQueryModel
    output_model = models.MultipleChoiceModel

    def translate_row(self, row: dict[str, typ.Any]) -> models.MultipleChoiceModel:
        """Translate a row."""
        m = self.input_model(**row)
        return self.output_model(
            id=m.uid,
            question=m.question,
            answers=m.answers,
            target=m.target,
        )
