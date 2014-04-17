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

from translator.hot.syntax.hot_parameter import HotParameter


INPUT_CONSTRAINTS = (CONSTRAINTS, DESCRIPTION, LENGTH, RANGE,
                     MIN, MAX, ALLOWED_VALUES, ALLOWED_PATTERN) = \
                    ('constraints', 'description', 'length', 'range',
                     'min', 'max', 'allowed_values', 'allowed_pattern')

TOSCA_TO_HOT_CONSTRAINTS_ATTRS = {'valid_values': 'allowed_values',
                                  'valid_pattern': 'allowed_pattern'}

TOSCA_TO_HOT_INPUT_TYPES = {'string': 'string',
                            'integer': 'number',
                            'float': 'number',
                            'boolean': 'string',
                            'timestamp': 'string',
                            'null': 'string'}


class TranslateInputs():
    '''Translate TOSCA Inputs to Heat Parameters.'''

    def __init__(self, inputs):
        self.inputs = inputs

    def translate(self):
        return self._translate_inputs()

    def _translate_inputs(self):
        hot_inputs = []
        for input in self.inputs:
            hot_input_type = TOSCA_TO_HOT_INPUT_TYPES[input.type]

            hot_constraints = []
            if input.constraints:
                for constraint in input.constraints:
                    constraint_name, value = constraint.iteritems().next()
                    hc = TOSCA_TO_HOT_CONSTRAINTS_ATTRS[constraint_name]
                    hot_constraints.append({hc: value})
            hot_inputs.append(HotParameter(name=input.name,
                                           type=hot_input_type,
                                           description=input.description,
                                           constraints=hot_constraints))
        return hot_inputs

    def _translate_constraints(self):
        #TODO(pvaneck): Add more refined constraint translation.
        pass
