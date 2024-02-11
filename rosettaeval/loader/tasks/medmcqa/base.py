import typing as typ

import pydantic

from rosettaeval.loader.tasks import adapter, models


class MedMcQaQueryModel(pydantic.BaseModel):
    """An input query model for MedMcQa."""

    id: str = pydantic.Field(..., description="id")
    question: str = pydantic.Field(..., description="question")
    opa: str = pydantic.Field(..., description="option a")
    opb: str = pydantic.Field(..., description="option b")
    opc: str = pydantic.Field(..., description="option c")
    opd: str = pydantic.Field(..., description="option d")
    cop: int = pydantic.Field(..., description="correct option")


class MedMcQaQueryAdapter(adapter.Adapter[MedMcQaQueryModel, models.MultipleChoiceModel]):
    """An adapter for multiple-choice datasets."""

    input_model = MedMcQaQueryModel
    output_model = models.MultipleChoiceModel

    def translate_row(self, row: dict[str, typ.Any]) -> models.MultipleChoiceModel:
        """Translate a row."""
        m = self.input_model(**row)
        choices = [m.opa, m.opb, m.opc, m.opd]
        return self.output_model(
            id=m.id,
            question=m.question,
            answers=choices,
            target=m.cop,
        )
