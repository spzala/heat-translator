from constraints import Constraint
from schema import Schema

class Properties(object):
    ''' Node type properties '''
    def __init__(self, properties):
        self.properties = properties

    def __contains__(self, key):
        return key in self.properties

    def __iter__(self):
        return iter(self.properties)

    def __len__(self):
        return len(self.properties)

    def __getitem__(self, key):
        '''Get a property value.'''
        return self.properties[key]
    
class Property(object):
    def __init__(self, name, nodetype, value):
        self.name = name
        self.nodetype = nodetype
        self.value = value
    
    def is_required(self):
        return Schema(self.nodetype).is_required(self.name)
    
    def get_name(self):
        return self.name
    
    def validate(self):
        self.validate_data_type()
        self.validate_constraints()
    
    def validate_data_type(self):
        data_type = Schema(self.nodetype).get_type(self.name)
        if data_type == Schema.STRING:
            return Constraint.validate_string(self.value)
        elif data_type == Schema.INTEGER:
            return Constraint.validate_integer(self.value)
        elif data_type == Schema.NUMBER:
            return Constraint.validate_number(self.value)
    
    def validate_constraints(self):
        constraints = Schema(self.nodetype).get_constraints(self.name)
        if constraints:
            for constraint in constraints:
                Constraint(self.name, self.value, constraint).validate()
