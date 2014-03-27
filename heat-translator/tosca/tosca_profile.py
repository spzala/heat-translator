from tosca.inputs import Input
from tosca.elements.graph import ToscaGraph
from tosca.nodetemplate import NodeTemplate

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
        self.inputs = self.inputs()
        self.nodetemplates = self.nodetemplates()
        self.noderoot = self.nodetpl_relationshipgraph()
        self.output = self.output()
        
    def inputs(self):
        inputs = []
        for name, attrs in self._get_inputs().iteritems():
            inputs.append(Input(name, attrs))
        return inputs

    def nodetemplates(self):
        '''node templates objects. '''
        nodetemplates = []
        tpls = self._get_nodetemplates()
        for name, value in tpls.iteritems():
            nodetemplates.append(NodeTemplate(name, value))
        return nodetemplates
    
    def nodetemplate(self, name):
        '''node templates objects. '''
        for nodetemplate, value in self._get_nodetemplates().iteritems():
            if nodetemplate == name:
                return value 
    
    def inputs(self):
        inputs = []
        for name, attrs in self._get_inputs().iteritems():
            inputs.append(Input(name, attrs))
        return inputs
    
    def output(self):
        #TODO
        pass
    
    def nodetpl_relationshipgraph(self):
        pass
        #return ToscaGraph(self.nodetemplates)
    
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