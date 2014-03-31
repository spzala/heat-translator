from constraints import Constraint
from entitytype import EntityType
import os
from yaml_parser import Parser

schema_file = (os.path.dirname(os.path.abspath(__file__))
               + os.sep + 'defs' + os.sep + 'properties_schema.yaml')
properties = Parser(schema_file).load()


class Properties(object):
    '''Tosca built-in properties types'''
    def __init__(self):
        self.defs = properties

    def __contains__(self, key):
        return key in self.defs

    def __iter__(self):
        return iter(self.defs)

    def __len__(self):
        return len(self.defs)

    def __getitem__(self, key):
        '''Get a section.'''
        return self.defs[key]


class PropertyDef(EntityType):
    '''Property type '''
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.schemata = Properties()[type]
        if value:
            self.value = value

    def is_required(self):
        ''' return true if property is a required for a given node '''
        return self.name in self.required()

    def get_schema(self, property_name):
        ''' get schema for a given property'''
        schema = {}
        for prop_key, prop_vale in self.schemata.iteritems():
            if prop_key == property_name:
                for attr, value in prop_vale.iteritems():
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

    def validate(self):
        #TODO: can't do data type validation because user
        #input is not provided until runtime
        #self.validate_data_type()
        self.validate_constraints()

    def validate_constraints(self):
        constraints = self.get_constraints()
        if constraints:
            for constraint in constraints:
                Constraint(self.name, self.value, constraint).validate()
