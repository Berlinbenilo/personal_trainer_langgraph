from jinja2 import Template


class PromptJinjaTemplate:
    def __init__(self, template, input_variables):
        self.template = Template(template)
        self.input_variables = input_variables

    def format(self, **kwargs):
        return self.template.render(**kwargs)
