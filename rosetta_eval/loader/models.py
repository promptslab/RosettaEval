import uuid

import pydantic

from rosetta_eval.loader.types import AnswerIndex


class MultipleChoiceModel(pydantic.BaseModel):
    """A base query data model."""

    id: str = pydantic.Field(
        default_factory=lambda: uuid.uuid4().hex,
        description="The unique identifier for the query.",
    )
    question: str = pydantic.Field(
        ...,
        description="The text of the question or query or instructions.",
    )
    answers: list[str] = pydantic.Field(..., description="A list of possible answers for the query. ")
    target: AnswerIndex = pydantic.Field(..., description="The index of the correct answer or completion. ")
