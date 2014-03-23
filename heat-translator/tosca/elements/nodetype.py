import os
from yaml_parser import Parser
from statefulentitytype import StatefulEntityType
from capabilitytype import Capabilities
from properties import Property
import relationshiptype

nodetype_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "nodetypesdef.yaml"
nodetype_def = Parser(nodetype_def_file).load()

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces', 'capabilities')

class NodeTypes(object):
    '''Tosca built-in node types'''
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
    
class NodeType(StatefulEntityType):
    '''Tosca built-in node type'''
    def __init__(self, type):
        super(NodeType, self).__init__()
        self.type = type
        self.defs = NodeTypes()[type]
    
    def derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    def properties(self):
        '''returns a list of property objects '''
        properties = []
        props = self._get_value(PROPERTIES)
        for prop in props:
            properties.append(Property(prop, self.type))
        return properties
    
    def requirements(self):
        return self._get_value(REQUIREMENTS)

    def has_relationship(self):
        return self.relationship()
    
    def relationship(self):
        '''returns a dictionary containing relationship to a particular node type '''
        relationship = {}
        requirs = self.requirements()
        if requirs:
            for req in requirs:
                for x, y in req.iteritems():
                    relation = self.get_relation(x, y)
                    relationship[relation] = y
        return relationship
    
    @classmethod
    def get_relation(cls, key, type):
        relation = None
        ntype = cls(type)
        cap = ntype.capabilities()
        for c in cap:
            if c.name == key:
                rtypedef = relationshiptype.relationship_def
                for relationship, properties in rtypedef.iteritems():
                    for x, y in properties.iteritems():
                        if c.type in y:
                            relation = relationship
                            break
                if relation:
                    break
        return relation
    
    def capabilities(self): 
        '''returns a list of capability objects '''
        capabilities = []
        self.prop_val = None
        caps = self._get_value(CAPABILITIES) 
        for name, value in caps.iteritems():
            for x, y in value.iteritems():
                if x == 'type':
                    self.__set_cap_type(y)
                if x == 'properties':
                    self.__set_prop_type(y)
            capabilities.append(Capabilities(name, self.type_val, self.prop_val))
        return capabilities
    
       
    def lifecycle_operations(self):
       return self.interfaces_node_lifecycle_operations
   
    def lifecycle_inputs(self):
        inputs = []
        interfaces = self._get_value('interfaces')
        if interfaces:
            for name, value in interfaces.iteritems():
                if name == 'lifecycle':
                    for x, y in value.iteritems():
                        if x == 'inputs':
                            for i, j in y.iteritems():
                                inputs.append(i)
        return inputs
    
    def __set_cap_type(self, value):
        self.type_val = value
    
    def __set_prop_type(self, value):
        self.prop_val = value
    
    def get_capability(self, name):
        for key, value in self.capabilities():
            if key == name:
                return value
            
    def get_capability_type(self, name):
        for key, value in self.get_capability(name):
            if key == type:
                return value
    
    def parent_node(self):
        parent_node = None
        root = 'tosca.nodes.Root'
        if self.type != root:
            derived = self.derivedfrom()
            derived = None
            if derived:
                if 'derived_from' in derived:
                    parent_node = derived['derived_from']
            if parent_node == None:
                parent_node = NodeType('tosca.nodes.Root')
            return parent_node
    
    def _get_value(self, type):
        if type in self.defs:
            return self.defs[type]
    