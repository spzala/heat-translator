from constraints import Constraint
from entitytype import EntityType


class PropertyDef(EntityType):
    '''Property type '''
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.schemata = self._schemata(name)
        if value:
            self.value = value
        self.constraints = self.get_constraints()

    def _schemata(self, name):
        node = self.TOSCA_DEF[self.type]
        for key, value in node.iteritems():
            if key == 'properties':
                if isinstance(value, dict):
                    for k, v in value.iteritems():
                        if k == self.name:
                            return v

    def is_required(self):
        ''' return true if property is a required for a given node '''
        return self.name in self.required()

    def get_schema(self, property_name):
        ''' get schema for a given property'''
        schema = {}
        if isinstance(self.schemata, dict):
            for prop_key, prop_val in self.schemata.iteritems():
                if prop_key == property_name:
                    for attr, value in prop_val.iteritems():
                        schema[attr] = value
        return schema

    def get_constraints(self):
        s = self.get_schema(self.name)
        if self.CONSTRAINTS in s:
            return s[self.CONSTRAINTS]

    def get_description(self, property_name):
        return self.get_schema(property_name)[self.DESCRIPTION]

    ''' list all the requirement for a given node type '''
    def required(self):
        required = []
        for prop_key, prop_vale in self.schemata.iteritems():
            for attr, value in prop_vale.iteritems():
                if attr == self.REQUIRED and value:
                    required.append(prop_key)
        return required

    def set_value(self, value):
        self.value = value

    def set_contraints(self, constrains):
        self.constrains = constrains

    def validate(self):
        #TODO: can't do data type validation because user
        #input is not provided until runtime
        #self.validate_data_type()
        self.validate_constraints()

    def validate_constraints(self):
        constraints = self.constraints
        if constraints:
            for constraint in constraints:
                Constraint(self.name, self.value, constraint).validate()
