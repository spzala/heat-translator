from constraints import Constraint
from entitytype import EntityType


class PropertyDef(EntityType):
    '''Property type '''
    def __init__(self, name, nodetype=None, tpl_name=None, value=None):
        self.name = name
        self.nodetype = nodetype
        self.tpl_name = tpl_name
        self.value = value
        if nodetype:
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
        if self.nodetype:
            for prop_key, prop_vale in self.schema.iteritems():
                if prop_key == self.REQUIRED and prop_vale:
                    return True

    @property
    def constraints(self):
        if self.nodetype:
            if self.CONSTRAINTS in self.schema:
                return self.schema[self.CONSTRAINTS]

    @property
    def description(self):
        if self.nodetype:
            if self.DESCRIPTION in self.schema:
                return self.schema[self.DESCRIPTION]

    def validate(self):
        #TODO: can't do data type validation because user
        #input is not provided until runtime
        #self.validate_data_type()
        if self.nodetype:
            self._validate_constraints()

    def _validate_constraints(self):
        constraints = self.constraints
        if constraints:
            for constraint in constraints:
                Constraint(self.name, self.value, constraint).validate()
