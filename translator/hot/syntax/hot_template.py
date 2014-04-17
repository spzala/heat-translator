import textwrap

import yaml

class HotTemplate(object):

    SECTIONS = (VERSION, DESCRIPTION, PARAMETER_GROUPS, PARAMETERS,
                RESOURCES, OUTPUTS, MAPPINGS) = \
               ('heat_template_version', 'description', 'parameter_groups',
                'parameters', 'resources', 'outputs', '__undefined__')

    VERSIONS = (LATEST,) = ('2013-05-23',)

    def __init__(self):
        self.resources = []
        self.outputs = []
        self.parameters = []
        self.description = ""

    def output_to_yaml(self):
        dict_output = {}
        # Version
        version_string = self.VERSION + ": " + self.LATEST + "\n\n"

        # Description
        desc_str = ""
        if self.description:
            # Wrap the text to a new line if the line exceeds 80 characters.
            wrapped_txt = "\n  ".join(textwrap.wrap(self.description, 80))
            desc_str = self.DESCRIPTION + ": >\n  " + wrapped_txt + "\n\n"

        # Parameters
        all_params = {}
        for parameter in self.parameters:
            all_params.update(parameter.get_dict_output())
        dict_output.update({self.PARAMETERS: all_params})

        # Resources
        all_resources = {}
        for resource in self.resources:
            all_resources.update(resource.get_dict_output())
        dict_output.update({self.RESOURCES: all_resources})

        # Outputs
        all_outputs = {}
        for output in self.outputs:
            all_outputs.update(output.get_dict_output())
        dict_output.update({self.OUTPUTS: all_outputs})

        yaml_string = yaml.dump(dict_output)
        return version_string + desc_str + yaml_string
