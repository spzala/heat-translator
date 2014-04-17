#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from translator.hot.syntax.hot_template import HotTemplate
from translator.hot.translate_inputs import TranslateInputs
from translator.hot.translate_nodetemplates import TranslateNodeTemplates
from translator.hot.translate_outputs import TranslateOutputs


class TOSCATranslator(object):
    '''Invokes translation methods.'''

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
