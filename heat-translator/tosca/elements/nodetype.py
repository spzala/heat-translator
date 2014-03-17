import os
from roottype import RootNodeType
from schema import Schema
from yaml_parser import Parser

nodetype_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "nodetypesdef.yaml"
nodetype_def = Parser(nodetype_def_file).load()

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces', 'capabilities')

class NodeType(RootNodeType):
    '''Tosca built-in node type'''
    def __init__(self, type):
        super(NodeType, self).__init__()
        self.type = type
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
    
    def derivedfrom(self):
        return self.getKey(self.type, DERIVED_FROM)

    def properties(self):
        return self.getkey(self.type, PROPERTIES)
    
    def requirements(self):
        return self.getkey(self.type, REQUIREMENTS)
    
    def interfaces(self):
        return self.getkey(self.type, INTERFACES)
    
    def capabilities(self):
        return self.getkey(self.type, CAPABILITIES) 
    
    def schema(self):
        return Schema(self.type)
    
    def get_relationshiptype(self):
        pass #return object
    
    def parent_node(self):
        parent_node = None
        derived = self.properties()
        if derived:
            if 'derived_from' in derived:
                parent_node = derived['derived_from']
        if parent_node == None:
            parent_node = RootNodeType()
    
    def getkey(self, nodetype, key):
        nodetype = self.defs[nodetype]
        for name, value in nodetype.iteritems():
            if name == key:
                return value
        
