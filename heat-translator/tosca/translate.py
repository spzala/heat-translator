import re
import yaml

from tosca.nodes.node_template import NodeTemplate
from tosca.nodes.nodetypes_def import Nodetype_Def
from tosca.nodes.relationship_graph import ToscaRelationshipGraph
from tosca.nodes.roottype import RootNodeType
from tosca.translation.translate_inputs import TranslateInputs
from tosca.translation.translate_nodetemplates import TranslateNodeTemplates

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
        heat_tpl = {}
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
    