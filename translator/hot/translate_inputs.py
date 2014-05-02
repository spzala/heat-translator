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

TOSCA_TO_HOT_CONSTRAINTS_ATTRS = {'equal': 'allowed_values',
                                  'greater_than': 'range',
                                  'greater_or_equal': 'range',
                                  'less_than': 'range',
                                  'less_or_equal': 'range',
                                  'in_range': 'range',
                                  'valid_values': 'allowed_values',
                                  'length': 'length',
                                  'min_length': 'length',
                                  'max_length': 'length',
                                  'pattern': 'allowed_pattern'}

TOSCA_TO_HOT_INPUT_TYPES = {'string': 'string',
                            'integer': 'number',
                            'float': 'number',
                            'boolean': 'string',
                            'timestamp': 'string',
                            'null': 'string'}


class TranslateInputs():
    '''Translate TOSCA Inputs to Heat Parameters.'''

    def __init__(self, inputs, parsed_params):
        self.inputs = inputs
        self.parsed_params = parsed_params

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
                    hc, hvalue = self._translate_constraints(constraint_name,
                                                             value)
                    hot_constraints.append({hc: hvalue})
            cli_value = self.parsed_params[input.name]
            hot_inputs.append(HotParameter(name=input.name,
                                           type=hot_input_type,
                                           description=input.description,
                                           default=cli_value,
                                           constraints=hot_constraints))
        return hot_inputs

    def _translate_constraints(self, name, value):
        hot_constraint = TOSCA_TO_HOT_CONSTRAINTS_ATTRS[name]

        # Offset used to support less_than and greater_than.
        offset = 1

        if name == 'equal':
            hot_value = [value]
        elif name == "greater_than":
            hot_value = {"min": value + offset}
        elif name == "greater_or_equal":
            hot_value = {"min": value}
        elif name == "less_than":
            hot_value = {"max": value - offset}
        elif name == "less_or_equal":
            hot_value = {"max": value}
        elif name == "in_range":
            range_values = value.keys()
            min_value = min(range_values)
            max_value = max(range_values)
            hot_value = {"min": min_value, "max": max_value}
        elif name == "length":
            hot_value = {"min": value, "max": value}
        elif name == "min_length":
            hot_value = {"min": value}
        elif name == "max_length":
            hot_value = {"max": value}
        else:
            hot_value = value
        return hot_constraint, hot_value

 
    # check all properties for all node and ensure they are resolved to actual values given at the CLI
    # use these values as the default in HOT parameters
    def resolve_input(self):
        for n in self.tosca.nodetemplates:
            for node_prop in n.tpl_properties:
                if isinstance(node_prop.value,dict):
                    try:
                        #print " -> resolving %s with input %s" % (node_prop.name,node_prop.value['get_input'])
                        #this_input_name = node_prop.value['get_input']
                        cli_input = self.parsed_params[node_prop.value['get_input']]
                        node_prop.value = cli_input
                        #print " -> resolving %s with input %s" % (node_prop.name,cli_input)
                    except:
                        raise ValueError('Must specify all input values in TOSCA template, missing %s' % node_prop.value['get_input'])
