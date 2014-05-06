# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from translator.toscalib.elements.constraints import Constraint
from translator.toscalib.elements.entitytype import EntityType


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
