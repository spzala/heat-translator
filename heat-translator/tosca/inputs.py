from tosca.nodes.constraints import Constraint
from tosca.nodes.schema import Schema

class InputParameters(object):
    def __init__(self, inputs):
        self.inputs = inputs

    def __contains__(self, key):
        return key in self.inputs

    def __iter__(self):
        return iter(self.inputs)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, key):
        '''Get a input value.'''
        return self.inputs[key]

class Input(object):
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema
    
    def get_type(self):
        return self.schema['type']
    
    def get_description(self):
        if self.has_default():
            return self.schema['description']
    
    def get_default(self):
        if self.has_default():
            return self.schema['default']
    
    def get_constraints(self):
        if self.has_constraints():
            return self.schema['constraints']
    
    def has_default(self):
        '''Return whether the input has a default value.'''
        return Schema.DEFAULT in self.schema

    def has_description(self):
        '''Return whether the parameter has description.'''
        return Schema.DESCRIPTION in self.schema
    
    def has_constraints(self):
        '''Return whether a given input has constraints'''
        return Schema.CONSTRAINTS in self.schema
        
    def validate(self):
        self.validate_type(self.get_type())
        if self.has_constraints():
            self.validate_constraints(self.get_constraints())
        
    def validate_type(self, input_type):
        if input_type not in Schema.TYPES:
            raise ValueError('Invalid type %s' % type)
    
    def validate_constraints(self, constraints):
        for constraint in constraints:
            for key in constraint.keys():
                if key not in Constraint.CONSTRAINTS:
                    raise ValueError('Invalid constraint %s' % constraint)
                if isinstance(key, dict):
                    #TODO
                    pass
    