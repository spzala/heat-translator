
from hot.hot_parameter import HotParameter


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
                            'null': 'string' }

class TranslateInputs():
    '''Translate TOSCA Inputs to Heat Parameters'''

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
            #hot_constraints = TOSCA_TO_HOT_CONSTRAINTS_ATTRS[input.constraints]
            description = input.description
            hot_inputs.append(HotParameter(name=input.name,
                                          type=hot_input_type,
                                          description=input.description,
                                          constraints=hot_constraints))
        return hot_inputs

    def _translate_constraints(self):
        pass