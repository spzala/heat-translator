
INPUT_CONSTRAINTS = (CONSTRAINTS, DESCRIPTION, LENGTH, RANGE,
                     MIN, MAX, ALLOWED_VALUES, ALLOWED_PATTERN) = \
                    ('constraints', 'description', 'length', 'range',
                     'min', 'max', 'allowed_values', 'allowed_pattern')

TOSCA_TO_HOT_CONSTRAINTS_ATTRS = {'valid_values': 'allowed_values',
                            'valid_pattern': 'allowed_pattern'}

class TranslateInputs():
    '''Translate TOSCA Inputs to Heat Parameters'''
    
    def __init__(self, inputs):
        self.inputs = inputs
        #TODO
