import random
import json
from rosettaeval.template_loader import TemplateLoader
import os


class PUBMEDQA:
    """
    A class to generate prompts for medical multiple-choice questions (MCQs)
    using various methods like few-shots, chain-of-thought (cot), etc.

    Attributes:
        instruction (str): The instruction or task description.
        method (str): The method used for generating prompts (e.g., 'fewshots', 'cot').
        n_example (int): The number of examples to use for generating the prompt.
    """

    def __init__(self, method, n_example, instruction = None):
        self.instruction = instruction
        self.method = method
        self.n_example = n_example
        # Correct way to construct the path
        current_file_dir = os.path.dirname(__file__)

        # Define supported methods and their directories
        # er and sc are dependent on cot methods, thus reusing the templates
        supported_methods = {
            "fewshots": "few_shots/",
            "cot": "cot/",
            "er": "cot/",
            "sc": "cot/",
        }

        method_path = supported_methods.get(method)

        if not method_path:
            raise ValueError(
                f"Method '{method}' is not supported. Choose from {list(supported_methods.keys())}."
            )

        # Load examples and template
        
        examples_path = os.path.join(current_file_dir, supported_methods[self.method], 'examples.json')
        self.examples = self._read_json_from_path(examples_path)["examples"]

        temp_path = os.path.join(current_file_dir, supported_methods[self.method], 'prompt.jinja')
        
        self.sampling = random.sample(self.examples, k=n_example)
        self.jinja_template = TemplateLoader().load_template(temp_path)

    def _read_json_from_path(self, path):
        """Utility method to read JSON from a given path."""
        try:
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from the file {path}.")

    def get_prompt(self, sample):
        """
        Generates a prompt for a given sample MCQ.

        Args:
            sample (dict): A dictionary containing MCQ information.

        Returns:
            str: A formatted prompt string.
        """
        prompt_full = self.jinja_template["template"].render(
            instruction=self.instruction,
            question=sample["question"],
            choices=sample["choices"],
            examples=self.sampling,
        )
        return {"full_prompt": prompt_full, "sample": sample}