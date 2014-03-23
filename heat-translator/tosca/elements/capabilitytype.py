import os
from yaml_parser import Parser

capability_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "capabilitytypedef.yaml"
capability_def = Parser(capability_def_file).load()

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
    def __init__(self, type): 
        self.type = type
        self.defs = CapabilityTypeDefs()[type]
    
    def properties(self):
        pass
    
    def derived_from(self):
        pass
    #TODO - add more capabilities methods

class Capabilities(object): 
    '''node type capabilites ''' 
    def __init__(self, name, type, properties=None): 
        self.name = name
        self.type = type
        if properties:
            self.properties = properties    
