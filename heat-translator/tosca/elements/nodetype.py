from capabilitytype import Capabilities
from tosca.log.toscalog import logger
import os
from properties import PropertyDef
import relationshiptype
from relationshiptype import RelationshipType
from statefulentitytype import StatefulEntityType
from yaml_parser import Parser

nodetype_def_file = (os.path.dirname(os.path.abspath(__file__))
                     + os.sep + 'defs' + os.sep + "nodetypesdef.yaml")
nodetype_def = Parser(nodetype_def_file).load()

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')


class NodeTypes(object):
    '''Tosca built-in node types'''
    def __init__(self):
        logger.info('adsf')
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
        self.related = {}

    def derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    def properties(self):
        '''returns a list of property objects '''
        properties = []
        props = self._get_value(PROPERTIES)
        if props:
            for prop in props:
                properties.append(PropertyDef(prop, self.type))
        return properties

    def relationship(self):
        '''returns a dictionary containing relationship to a particular
        node type '''
        relationship = {}
        requirs = self.requirements()
        if requirs:
            for req in requirs:
                for x, y in req.iteritems():
                    relation = self.get_relation(x, y)
                    rtype = RelationshipType(relation)
                    relatednode = self.ntype(x, y)
                    relationship[rtype] = relatednode
        return relationship

    @classmethod
    def ntype(cls, key, ndtype):
        return cls(ndtype)

    def capabilities(self):
        '''returns a list of capability objects '''
        capabilities = []
        self.prop_val = None
        caps = self._get_value(CAPABILITIES)
        if caps:
            for name, value in caps.iteritems():
                for x, y in value.iteritems():
                    if x == 'type':
                        self.__set_cap_type(y)
                    if x == 'properties':
                        self.__set_prop_type(y)
                cap = Capabilities(name, self.type_val, self.prop_val)
                capabilities.append(cap)
        else:
            logger.info('%s does not provide capabilities. ' % self.type)
        return capabilities

    def requirements(self):
        return self._get_value(REQUIREMENTS)

    def has_relationship(self):
        return self.relationship()

    @classmethod
    def get_relation(cls, key, ndtype):
        relation = None
        ntype = cls(ndtype)
        cap = ntype.capabilities()
        for c in cap:
            if c.name == key:
                rtypedef = relationshiptype.relationship_def
                for relationship, properties in rtypedef.iteritems():
                    for y in properties.itervalues():
                        if c.type in y:
                            relation = relationship
                            break
                if relation:
                    break
        return relation

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
                            for i in y.iterkeys():
                                inputs.append(i)
        else:
            logger.info('%s does not have life cycle input. ' % self.type)
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
        root = 'tosca.nodes.Root'
        parent_node = root
        if self.type != root:
            parent_node = self.derivedfrom()
            parent_node = NodeType(parent_node)
            if parent_node is None:
                parent_node = NodeType(root)
            return parent_node

    def _get_value(self, ndtype):
        if ndtype in self.defs:
            return self.defs[ndtype]

    def add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    def get_relatednodes(self):
        return self.related.keys()

    def get_type(self):
        return self.type

    def get_relationship(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]
