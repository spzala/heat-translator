from tosca.elements.node_template import NodeTemplate
from tosca.inputs import Input
from tosca.elements.relationship_graph import ToscaRelationshipGraph

SECTIONS = (VERSION, DESCRIPTION, INPUTS,
            NODE_TEMPLATES, OUTPUTS) = \
           ('tosca_definitions_version', 'description', 'inputs',
            'node_templates', 'outputs')

class Tosca(object):
    '''Read a Tosca profile'''
    def __init__(self, sourcedata):
        self.sourcedata = sourcedata
        self.version = self._get_version()
        self.description = self._get_description()
        
    def inputs(self):
        inputs = []
        for name, attrs in self._get_inputs().iteritems():
            inputs.append(Input(name, attrs))
        return inputs

    def nodetemplates(self):
        '''node templates objects. '''
        nodetemplates = []
        for nodetemplate, value in self._get_nodetemplates().iteritems():
            nodetemplates.append(NodeTemplate(nodetemplate, value))
        return nodetemplates
    
    def inputs(self):
        inputs = []
        for name, attrs in self._get_inputs().iteritems():
            inputs.append(Input(name, attrs))
        return inputs
    
    def nodetpl_relationshipgraph(self):
        return ToscaRelationshipGraph(self.nodetemplates())
    
    def _get_version(self):
        return self.sourcedata[VERSION]

    def _get_description(self):
        return self.sourcedata[DESCRIPTION]
    
    def _get_inputs(self):
        return self.sourcedata[INPUTS]

    def _get_nodetemplates(self):
        return self.sourcedata[NODE_TEMPLATES]

    def _get_outputs(self):
        return self.sourcedata[OUTPUTS]