
from hot.syntax.hot_output import HotOutput

TOSCA_TO_HOT_GET_ATTRS = {'ip_address':'first_address'}

class TranslateOutputs():
    '''Translate TOSCA Outputs to Heat Parameters'''

    def __init__(self, outputs):
        self.outputs = outputs      # outputs is a list

    def translate(self):
        return self._translate_outputs()

    def _translate_outputs(self):
        hot_outputs = []
        for output in self.outputs:
            hot_value = {}
            if 'get_property' in output.value:     # value is a dict
                get_parameters = output.value['get_property']
                if get_parameters[1] in TOSCA_TO_HOT_GET_ATTRS:
                    get_parameters[1] = TOSCA_TO_HOT_GET_ATTRS[get_parameters[1]]
                hot_value['get_attr'] = get_parameters
                hot_outputs.append(HotOutput(output.name,hot_value,output.description))
            else:
                hot_output.append(HotOutput(output.name,output.value,output.description))
        return hot_outputs