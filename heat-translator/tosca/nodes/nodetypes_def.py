import os
from yaml_loader import Loader

nodetype_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + "nodetypesdef.yaml"
nodetype_def = Loader(nodetype_def_file).load()

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces', 'capabilities')

class Nodetype_Def(object):
    ''' Load node type definition '''
    def __init__(self):
        self.defs = nodetype_def
            
    def __contains__(self, key):
        return key in self.defs

    def __iter__(self):
        return iter(self.defs)

    def __len__(self):
        return len(self.defs)

    def __getitem__(self, key):
        '''Get a section.'''
        return self.defs[key]
    
    def derivedfrom(self, nodetype):
        return self.getKey(nodetype, DERIVED_FROM)

    def properties(self, nodetype):
        return self.getkey(nodetype, PROPERTIES)
    
    def requirements(self, nodetype):
        return self.getkey(nodetype, REQUIREMENTS)
    
    def interfaces(self, nodetype):
        return self.getkey(nodetype, INTERFACES)
    
    def capabilities(self, nodetype):
        return self.getkey(nodetype, CAPABILITIES) 
    
    def getkey(self, nodetype, key):
        nodetype = self.defs[nodetype]
        for name, value in nodetype.iteritems():
            if name == key:
                return value
        
