import os

import yaml

from translator.hot.syntax.hot_template import HotTemplate
from translator.hot.translate_inputs import TranslateInputs
from translator.hot.translate_nodetemplates import TranslateNodeTemplates
from translator.hot.translate_outputs import TranslateOutputs
import translator.toscalib.utils.yamlparser

SECTIONS = (VERSION, DESCRIPTION, PARAMETERS,
            RESOURCES, OUTPUTS) = \
           ('heat_template_version', 'description', 'parameters',
            'resources', 'outputs')

HEAT_VERSIONS = '2013-05-23'

if hasattr(yaml, 'CSafeDumper'):
    yaml_dumper = yaml.CSafeDumper
else:
    yaml_dumper = yaml.SafeDumper

yaml_tpl = {}


class TOSCATranslator(object):

    ''' Invokes translation methods.'''
    def __init__(self, tosca):
        super(TOSCATranslator, self).__init__()
        self.tosca = tosca
        self.hot_template = HotTemplate()

    def translate(self):
        self.hot_template.description = self.tosca.description
        self.hot_template.parameters = self._translate_inputs()
        self.hot_template.resources = self._translate_node_templates()
        self.hot_template.outputs = self._translate_outputs()
        return self.hot_template.output_to_yaml()

    def _translate_inputs(self):
        translator = TranslateInputs(self.tosca.inputs)
        return translator.translate()

    def _translate_node_templates(self):
        translator = TranslateNodeTemplates(self.tosca.nodetemplates,
                                            self.hot_template)
        return translator.translate()

    def _translate_outputs(self):
        translator = TranslateOutputs(self.tosca.outputs)
        return translator.translate()
