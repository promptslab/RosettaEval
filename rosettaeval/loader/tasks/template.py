import copy
import json
import typing as typ

import jinja2
from jinja2 import meta

from rosettaeval.loader.tasks.decorators import load_from_file

Methods = typ.Literal["direct", "fewshots"]
Tasks = typ.Literal["medqa", "medmcqa"]


class BasePrompt:
    """A factory class to load a prompt template."""

    def format_and_validate_message(self, message: dict[str, str], sample: dict[str, typ.Any]) -> dict[str, str]:
        """Format the message template."""
        modified_message = copy.deepcopy(message)
        env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)  # noqa: S701
        template = env.from_string(modified_message["content"])

        ast = env.parse(modified_message["content"])
        undeclared = meta.find_undeclared_variables(ast)
        missing_vars = undeclared - set(sample.keys())
        if missing_vars:
            msg = f"Missing variables in the template: {missing_vars} in `{self.__class__}`."
            raise ValueError(msg)

        modified_message["content"] = template.render(**sample)
        return modified_message

    def __call__(self, messages: list[dict[str, str]], sample: dict[str, typ.Any]) -> list[dict[str, str]]:
        """Generate a prompt."""
        return [self.format_and_validate_message(msg, sample) for msg in messages]

    @classmethod
    @load_from_file(".json")
    def from_json(cls, f: typ.IO[str]) -> "BasePrompt":
        """Load a prompt template from a JSON file."""
        data = json.load(f)
        return cls(**data)


class DirectPromptTemplate(BasePrompt):
    """A few-shot prompt template."""

    system_template: str | None = None
    user_template: str

    def __call__(self, sample: dict[str, typ.Any], messages: list[dict[str, str]] | None) -> list[dict[str, str]]:
        """Generate a prompt."""
        messages = messages or []
        messages.append({"role": "user", "content": self.user_template})
        if self.system_template is None:
            return super().__call__(messages, sample)
        messages.insert(0, {"role": "system", "content": self.system_template})
        return super().__call__(messages, sample)


class FewShotPromptTemplate(DirectPromptTemplate):
    """A few-shot prompt template."""

    assistant_template: str
    examples: list[dict[str, typ.Any]]

    def __call__(self, sample: dict[str, typ.Any]) -> list[dict[str, str]]:
        """Generate a prompt."""
        messages = [
            self.format_and_validate_message({"role": "assistant", "content": self.assistant_template}, shot)
            for shot in self.examples
        ]
        return super().__call__(sample, messages)
