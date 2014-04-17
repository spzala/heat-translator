import logging

from translator.toscalib.elements.constraints import Constraint
from translator.toscalib.elements.entitytype import EntityType

log = logging.getLogger('tosca')


class Input(object):
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema

    @property
    def type(self):
        return self.schema['type']

    @property
    def description(self):
        if EntityType.DESCRIPTION in self.schema:
            return self.schema['description']

    @property
    def default(self):
        if self.EntityType.DEFAULT in self.schema:
            return self.schema['default']

    @property
    def constraints(self):
        if EntityType.CONSTRAINTS in self.schema:
            return self.schema['constraints']

    def validate(self):
        self.validate_type(self.type)
        if self.constraints:
            self.validate_constraints(self.constraints)

    def validate_type(self, input_type):
        if input_type not in EntityType.PROPERTIES_TYPES:
            raise ValueError('Invalid type %s' % type)

    def validate_constraints(self, constraints):
        for constraint in constraints:
            for key in constraint.keys():
                if key not in Constraint.CONSTRAINTS:
                    raise ValueError('Invalid constraint %s' % constraint)
                if isinstance(key, dict):
                    #TODO
                    pass


class Output(object):
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs

    @property
    def description(self):
        return self.attrs['description']

    @property
    def value(self):
        return self.attrs['value']
