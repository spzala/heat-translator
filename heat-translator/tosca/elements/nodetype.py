from capabilitytype import CapabilityTypeDef
from interfacestype import InterfacesTypeDef
from properties import PropertyDef
from relationshiptype import RelationshipType
from statefulentitytype import StatefulEntityType


SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')


class NodeType(StatefulEntityType):
    '''Tosca built-in node type'''
    def __init__(self, type):
        super(NodeType, self).__init__()
        self.defs = self.TOSCA_DEF[type]
        self.type = type
        self.related = {}

    def _derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    def derivedfrom(self):
        if self._derivedfrom():
            return NodeType(self._get_value(DERIVED_FROM))

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
        if requirs is None:
            requirs = self._get_value(REQUIREMENTS, None, True)
        if requirs:
            for req in requirs:
                for x, y in req.iteritems():
                    relation = self.get_relation(x, y)
                    rtype = RelationshipType(relation, x)
                    #relatednode = self.ntype(x, y)
                    relatednode = NodeType(y)
                    relationship[rtype] = relatednode
        return relationship

    def get_relation(self, key, ndtype):
        relation = None
        ntype = NodeType(ndtype)
        cap = ntype.capabilities()
        for c in cap:
            if c.name == key:
                for r in self.RELATIONSHIP_TYPE:
                    rtypedef = ntype.TOSCA_DEF[r]
                    for relationship, properties in rtypedef.iteritems():
                        if c.type in properties:
                            relation = r
                            break
                    if relation:
                        break
        return relation

    def capabilities(self):
        '''returns a list of capability objects '''
        capabilities = []
        self.prop_val = None
        caps = self._get_value(CAPABILITIES)
        if caps is None:
            caps = self._get_value(CAPABILITIES, None, True)
        if caps:
            for name, value in caps.iteritems():
                for x, y in value.iteritems():
                    if x == 'type':
                        self.__set_cap_type(y)
                    if x == 'properties':
                        self.__set_prop_type(y)
                cap = CapabilityTypeDef(name, self.type_val,
                                        self.type, self.prop_val)
                capabilities.append(cap)
        return capabilities

    def requirements(self):
        return self._get_value(REQUIREMENTS)

    def has_relationship(self):
        return self.relationship()

    def interfaces(self):
        return self._get_value(INTERFACES)

    def lifecycle_inputs(self):
        inputs = []
        interfaces = self.interfaces()
        if interfaces:
            for name, value in interfaces.iteritems():
                if name == 'tosca.interfaces.node.Lifecycle':
                    for x, y in value.iteritems():
                        if x == 'inputs':
                            for i in y.iterkeys():
                                inputs.append(i)
        return inputs

    def lifecycle_operations(self):
        '''return available life cycle operations if found, None otherwise.'''
        ops = None
        interfaces = self.interfaces()
        if interfaces:
            i = InterfacesTypeDef(self.type, 'tosca.interfaces.node.Lifecycle')
            ops = i.lifecycle_ops()
        return ops

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

    def _get_value(self, ndtype, defs=None, parent=None):
        value = None
        if defs is None:
            defs = self.defs
        if ndtype in defs:
            value = defs[ndtype]
        if parent and not value:
            p = self.derivedfrom()
            while value is None:
                #check parent node
                if not p:
                    break
                if p and p.type == 'tosca.nodes.Root':
                    break
                value = p._get_value(ndtype)
                p = p.derivedfrom()
        return value

    def add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    def get_relatednodes(self):
        return self.related.keys()

    def get_type(self):
        return self.type

    def get_relationship(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]
