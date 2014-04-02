from entitytype import EntityType
from properties import PropertyDef


SECTIONS = (DERIVED_FROM, PROPERTIES) = \
           ('derived_from', 'properties')


class CapabilityTypeDef(EntityType):
    '''Tosca built-in capabilities type'''
    def __init__(self, name, ctype, ntype, property_nodetype=None):
        self.defs = self.TOSCA_DEF[ctype]
        self.name = name
        self.type = ctype
        self.nodetype = ntype
        self.property_nodetype = property_nodetype

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

    def derivedfrom(self):
        if self._derivedfrom():
            return CapabilityTypeDef(self._get_value(DERIVED_FROM))

    def _get_value(self, ctype):
        if ctype in self.defs:
            return self.defs[ctype]
