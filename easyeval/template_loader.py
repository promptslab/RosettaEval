import os
from glob import glob
from typing import List
from jinja2 import Template, Environment, FileSystemLoader, meta, BaseLoader

class TemplateLoader:
    """
    A class for loading and managing Jinja2 templates. It allows loading templates from files or strings,
    listing available templates, and getting template variables.
    """

    def __init__(self):
        """
        Initialize the TemplateLoader object and create an empty dictionary for loaded templates.
        """
        self.loaded_templates = {}

    def to_letter(self, index):
        return chr(65 + index)

    def load_template(
        self, template: str, from_string: bool = False
    ):
        """
        Load a Jinja2 template either from a string or a file.

        Args:
            template (str): Template string or path to the template file.
            from_string (bool): Whether to load the template from a string. Defaults to False.

        Returns:
            dict: Loaded template data.
        """
        if template in self.loaded_templates:
            return self.loaded_templates[template]

        if from_string:
            template_instance = Environment(loader=BaseLoader())
            template_instance.filters['to_letter'] = self.to_letter
            template = template_instance.from_string(template)
            
            template_data = {
                "template_name": "from_string",
                "template_dir": None,
                "environment": template_instance,
                "template":    template,
            }
            
        else:
            template_data = self._load_template_from_path(template)
        self.loaded_templates[template] = template_data
        return self.loaded_templates[template]

    def _load_template_from_path(self, template: str) -> dict:
        """
        Load a Jinja2 template from the given path.

        Args:
            template (str): Path to the template file.

        Returns:
            dict: Loaded template data.
        """
        
        self._verify_template_path(template)
        custom_template_dir, custom_template_name = os.path.split(template)
        environment = Environment(loader=FileSystemLoader(custom_template_dir))
        environment.filters['to_letter'] = self.to_letter
        template_instance = environment.get_template(custom_template_name)

        return {
            "template_name": custom_template_name,
            "template_dir":  custom_template_dir,
            "environment":   environment,
            "template":      template_instance}

    def _verify_template_path(self, templates_path: str):
        """
        Verify the existence of the template file.

        Args:
            templates_path (str): Path to the template file.

        Raises:
            ValueError: If the template file does not exist.
        """
        if not os.path.isfile(templates_path):
            raise ValueError(f"Templates path {templates_path} does not exist")