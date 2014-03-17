import re
import yaml

from tosca.elements.relationship_graph import ToscaRelationshipGraph

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
        self.test_graph()
        self._translate_inputs()
        self._translate_node_templates()
        self._translate_outputs()

    def test_graph(self):
        g = ToscaRelationshipGraph(self.tosca)
        for k in g:
            for w in k.get_relatednodetpls():
                print("( %s , %s )" % (k.get_name(), w.get_name()))
                print k.get_relationship(w).name()

    def _translate_inputs(self):
        #TODO
        pass
    
    def _translate_node_templates(self):
        #TODO
        pass
        
    def _translate_outputs(self):
        #TODO
        pass
