import os
from yaml_parser import Parser

capability_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "capabilitytype_def.yaml"
capability_def = Parser(capability_def_file).load()

class CapabilityType(object):
    '''Tosca built-in capabilities type'''
    def __init__(self, type): 
        self.type = type
        self.defs = capability_def
    
    def capabilities(self):
        if self.capabilities:
            return self.capabilities
    
    #TODO - add more capabilities methods