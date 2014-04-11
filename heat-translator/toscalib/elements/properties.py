from constraints import Constraint
from entitytype import EntityType


class PropertyDef(EntityType):
    '''Property type '''
    def __init__(self, name, nodetype, value=None, tpl_name=None):
        self.name = name
        self.nodetype = nodetype
        self.tpl_name = tpl_name
        self.value = value
        self.schema = self._schema()

    def _schema(self):
        node = self.TOSCA_DEF[self.nodetype]
        for key, value in node.iteritems():
            if key == 'properties':
                if isinstance(value, dict):
                    for k, v in value.iteritems():
                        if k == self.name:
                            return v

    @property
    def required(self):
        ''' return true if property is a required for a given node '''
        for prop_key, prop_vale in self.schema.iteritems():
            if prop_key == self.REQUIRED and prop_vale:
                return True

    @property
    def constraints(self):
        if self.CONSTRAINTS in self.schema:
            return self.schema[self.CONSTRAINTS]

    @property
    def description(self):
        if self.DESCRIPTION in self.schema:
            return self.schema[self.DESCRIPTION]

    def validate(self):
        '''Validate, if not a reference property.'''
        if not isinstance(self.value, dict):
            self._validate_constraints()
            self._validate_datatype()

    def _validate_datatype(self):
        dtype = self.schema['type']
        if dtype == self.STRING:
            return Constraint.validate_string(self.value)
        elif dtype == self.INTEGER:
            return Constraint.validate_integer(self.value)
        elif dtype == self.NUMBER:
            return Constraint.validate_number(self.value)
        elif dtype == self.LIST:
            return Constraint.validate_list(self.value)

    def _validate_constraints(self):
        constraints = self.constraints
        if constraints:
            for constraint in constraints:
                Constraint(self.name, self.value, constraint).validate()
