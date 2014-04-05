import logging
from tosca.elements.nodetype import NodeType
from tosca.elements.capabilitytype import CapabilityTypeDef
from tosca.elements.interfacestype import InterfacesTypeDef

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')

log = logging.getLogger("tosca.log")


class NodeTemplate(NodeType):
    ''' Node template from a Tosca profile.'''
    def __init__(self, name, nodetemplates):
        super(NodeTemplate, self).__init__(nodetemplates[name]['type'])
        self.name = name
        self.nodetemplates = nodetemplates
        self.nodetemplate = nodetemplates[self.name]
        self.type = self.nodetemplate['type']
        self.type_properties = self.properties
        self.type_capabilities = self.capabilities
        self.type_lifecycle_ops = self.lifecycle_operations
        self.type_relationship = self.relationship
        self.related = {}
        self.tpl_interfaces

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

    @property
    def tpl_capabilities(self):
        '''returns a list of capability objects '''
        tpl_cap = []
        prop_name = None
        prop_val = None
        caps = self._get_value(CAPABILITIES, self.nodetemplate)
        if caps:
            for name, value in caps.iteritems():
                for prop, val in value.iteritems():
                    for p, v in val.iteritems():
                        prop_name = p
                        prop_val = v
                cap = CapabilityTypeDef(name, name,
                                        self.name, prop_name, prop_val)
                tpl_cap.append(cap)
        return tpl_cap

    @property
    def tpl_interfaces(self):
        tpl_ifaces = []
        ifaces = self._get_value(INTERFACES, self.nodetemplate)
        if ifaces:
            for i in ifaces:
                for name, value in ifaces.iteritems():
                    for ops, val in value.iteritems():
                        iface = InterfacesTypeDef(None, name, self.name,
                                                  ops, val)
                        tpl_ifaces.append(iface)
        return tpl_ifaces

    def _add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    @property
    def relatednodes(self):
        return self.related.keys()

    def relation(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]
