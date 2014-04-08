import logging
import tosca.utils.yamlparser
from tosca.nodetemplate import NodeTemplate
from tosca.parameters import Input, Output
from tosca.elements.tpl_relationship_graph import ToscaGraph

SECTIONS = (VERSION, DESCRIPTION, INPUTS,
            NODE_TEMPLATES, OUTPUTS) = \
           ('tosca_definitions_version', 'description', 'inputs',
            'node_templates', 'outputs')

log = logging.getLogger("tosca.model")


class ToscaTpl(object):
    '''
    Load the source data.
    '''
    def __init__(self, path):
        self.tpl = tosca.utils.yamlparser.load_yaml(path)
        self.version = self._tpl_version()
        self.description = self._tpl_description()
        self.inputs = self._inputs()
        self.nodetemplates = self._nodetemplates()
        self.outputs = self._outputs()
        self.graph = ToscaGraph(self.nodetemplates)

    def _inputs(self):
        inputs = []
        for name, attrs in self._tpl_inputs().iteritems():
            input = Input(name, attrs)
            if not isinstance(input.schema, dict):
                raise ValueError(("The input %(input)s has no attributes.")
                                 % {'input': input})
            input.validate()
            inputs.append(input)
        return inputs

    def _nodetemplates(self):
        '''node templates objects. '''
        nodetemplates = []
        tpls = self._tpl_nodetemplates()
        for name, value in tpls.iteritems():
            tpl = NodeTemplate(name, tpls)
            tpl.validate()
            nodetemplates.append(tpl)
        return nodetemplates

    def _outputs(self):
        outputs = []
        for name, attrs in self._tpl_outputs().iteritems():
            outputs.append(Output(name, attrs))
        return outputs

    def _tpl_version(self):
        return self.tpl[VERSION]

    def _tpl_description(self):
        return self.tpl[DESCRIPTION]

    def _tpl_inputs(self):
        return self.tpl[INPUTS]

    def _tpl_nodetemplates(self):
        return self.tpl[NODE_TEMPLATES]

    def _tpl_outputs(self):
        return self.tpl[OUTPUTS]
