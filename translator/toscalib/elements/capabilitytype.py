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

from translator.toscalib.elements.entitytype import EntityType
from translator.toscalib.elements.properties import PropertyDef


SECTIONS = (DERIVED_FROM, PROPERTIES) = \
           ('derived_from', 'properties')


class CapabilityTypeDef(EntityType):
    '''Tosca built-in capabilities type'''
    def __init__(self, name, ctype, ntype, property=None, prop_value=None):
        if ntype:
            self.defs = self.TOSCA_DEF[ctype]
        self.name = name
        self.type = ctype
        self.nodetype = ntype
        self.property = property
        self.property_value = prop_value

    @property
    def propertiesdef(self):
        '''returns a list of property objects '''
        properties = []
        props = self._get_value(PROPERTIES)
        if props:
            for prop in props:
                properties.append(PropertyDef(prop, self.type))
        return properties

    def _derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    @property
    def derivedfrom(self):
        if self._derivedfrom():
            return CapabilityTypeDef(self._get_value(DERIVED_FROM))

    def _get_value(self, ctype):
        if ctype in self.defs:
            return self.defs[ctype]
