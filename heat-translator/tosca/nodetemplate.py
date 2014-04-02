from tosca.elements.nodetype import NodeType


class NodeTemplate(NodeType):
    ''' Node template from a Tosca profile.'''
    def __init__(self, name, nodetemplate):
        super(NodeTemplate, self).__init__(nodetemplate['type'])
        self.name = name
        self.nodetemplate = nodetemplate
        self.type_properties = self.properties()
        self.type_capabilities = self.capabilities()
        self.type_lifecycle_ops = self.lifecycle_operations()
        self.type_relationship = self.relationship()

    @classmethod
    def ntype(cls, key, type):
        return NodeType(type)

    @classmethod
    def get_relation(cls, key, type):
        relation = None
        ntype = NodeType(type)
        cap = ntype.capabilities()
        for c in cap:
            if c.name == key:
                for r in cls.RELATIONSHIP_TYPE:
                    rtypedef = cls.TOSCA_DEF[r]
                    for relationship, properties in rtypedef.iteritems():
                        if c.type in properties:
                            relation = c.type
                            break
                    if relation:
                        break
        return relation

    def get_name(self):
        return self.name

    def get_value(self):
        return self.nodetemplate

    def get_type(self):
        return self.nodetemplate['type']
