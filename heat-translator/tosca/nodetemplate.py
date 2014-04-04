from tosca.elements.nodetype import NodeType

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')


class NodeTemplate(NodeType):
    ''' Node template from a Tosca profile.'''
    def __init__(self, name, nodetemplates):
        super(NodeTemplate, self).__init__(nodetemplates[name]['type'])
        self.name = name
        self.nodetemplates = nodetemplates
        self.nodetemplate = nodetemplates[self.name]
        self.type = self.nodetemplate['type']
        self.type_properties = self.properties()
        self.type_capabilities = self.capabilities()
        self.type_lifecycle_ops = self.lifecycle_operations()
        self.type_relationship = self.relationship()
        self.related = {}

    @property
    def value(self):
        return self.nodetemplate

    @property
    def tpl_requirements(self):
        return self._get_value(REQUIREMENTS, self.nodetemplate)

    @property
    def tpl_relationship(self):
        tpl_relation = {}
        requirs = self.tpl_requirements
        if requirs:
            for r in requirs:
                for x, y in r.iteritems():
                    for i, j in self.type_relationship.iteritems():
                        if x == i.keyword:
                            rtpl = NodeTemplate(y, self.nodetemplates)
                            tpl_relation[i] = rtpl
        return tpl_relation

    def _add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    @property
    def relatednodes(self):
        return self.related.keys()

    def relation(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]
