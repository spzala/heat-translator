#import re
import yaml

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

    def translate(self):
        self._translate_inputs()
        self._translate_node_templates()
        self._translate_outputs()

    def _translate_inputs(self):
        #TODO
        pass

    def _translate_node_templates(self):
        #TODO
        pass

    def _translate_outputs(self):
        #TODO
        pass
