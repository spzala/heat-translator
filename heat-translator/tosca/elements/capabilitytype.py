import os
from yaml_parser import Parser
from properties import PropertyDef

capability_def_file = (os.path.dirname(os.path.abspath(__file__))
                       + os.sep + 'defs' + os.sep + "capabilitytypedef.yaml")
capability_def = Parser(capability_def_file).load()

SECTIONS = (DERIVED_FROM, PROPERTIES) = \
           ('derived_from', 'properties')


class CapabilityTypeDefs(object):
    '''Tosca built-in capabilities types'''
    def __init__(self):
        self.defs = capability_def

    def __contains__(self, key):
        return key in self.defs

    def __iter__(self):
        return iter(self.defs)

    def __len__(self):
        return len(self.defs)

    def __getitem__(self, key):
        '''Get a section.'''
        return self.defs[key]


class CapabilityTypeDef(object):
    '''Tosca built-in capabilities type'''
    def __init__(self, name, ctype, ntype, property_nodetype=None):
        self.name = name
        self.type = ctype
        self.defs = CapabilityTypeDefs()[self.type]
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
