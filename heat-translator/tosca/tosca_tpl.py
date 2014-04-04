import tosca.utils.yamlparser
from tosca.inputs import Input
from tosca.nodetemplate import NodeTemplate
from tosca.elements.tpl_relationship_graph import ToscaGraph

SECTIONS = (VERSION, DESCRIPTION, INPUTS,
            NODE_TEMPLATES, OUTPUTS) = \
           ('tosca_definitions_version', 'description', 'inputs',
            'node_templates', 'outputs')


class ToscaTpl(object):
    '''
    Load the source data.
    '''
    def __init__(self, path):
        self.tpl = tosca.utils.yamlparser.load_yaml(path)
        self.version = self._version
        self.description = self._description
        self.inputs = self._inputs()
        self.nodetemplates = self._nodetemplates()
        self.outputs = self._output()
        self.graph = ToscaGraph(self.nodetemplates)

    def _inputs(self):
        inputs = []
        for name, attrs in self.tosca_inputs.iteritems():
            inputs.append(Input(name, attrs))
        return inputs

    def _nodetemplates(self):
        '''node templates objects. '''
        nodetemplates = []
        tpls = self.tosca_nodetemplates
        for name, value in tpls.iteritems():
            nodetemplates.append(NodeTemplate(name, tpls))
        return nodetemplates

    def _output(self):
        #TODO
        pass

    def _version(self):
        return self.tpl[VERSION]

    def _description(self):
        return self.tpl[DESCRIPTION]

    @property
    def tosca_inputs(self):
        return self.tpl[INPUTS]

    @property
    def tosca_nodetemplates(self):
        return self.tpl[NODE_TEMPLATES]

    @property
    def tosca_outputs(self):
        return self.tpl[OUTPUTS]

    @property
    def nodetemplate(self, tplname):
        return self.nodetemplates[tplname]
