import os
from schema import Schema
from yaml_parser import Parser

nodetype_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "nodetypesdef.yaml"
nodetype_def = Parser(nodetype_def_file).load()

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces', 'capabilities')

class NodeType(object):
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
        return self._get_value(DERIVED_FROM)

    def properties(self):
        return self._get_value(PROPERTIES)
    
    def requirements(self):
        return self._get_value(REQUIREMENTS)
    
    def interfaces(self):
        return self._get_value(INTERFACES)
    
    def capabilities(self):
        return self._get_value(CAPABILITIES) 
    
    def schema(self):
        return Schema(self.type)
    
    def get_relationshiptype(self):
        pass #return object
    
    def parent_node(self):
        parent_node = None
        root = 'tosca.nodes.Root'
        if self.type != root:
            derived = self.derivedfrom()
            derived = None
            if derived:
                if 'derived_from' in derived:
                    pass 
                    #parent_node = derived['derived_from']
            if parent_node == None:
                parent_node = NodeType('tosca.nodes.Root')
            return parent_node
    
    def _get_value(self, type):
        d = self[self.type]
        for a, b in d.iteritems():
            if a == type:
                return b
        