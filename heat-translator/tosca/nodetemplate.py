import logging
from tosca.elements.nodetype import NodeType
from tosca.elements.capabilitytype import CapabilityTypeDef
from tosca.elements.interfacestype import InterfacesTypeDef
from tosca.elements.properties import PropertyDef

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')

log = logging.getLogger('tosca')


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
        cap_type = None
        caps = self._get_value(CAPABILITIES, self.nodetemplate)
        if caps:
            for name, value in caps.iteritems():
                for prop, val in value.iteritems():
                    for p, v in val.iteritems():
                        prop_name = p
                        prop_val = v
                for c in self.type_capabilities:
                    if c.name == name:
                        cap_type = c.type
                cap = CapabilityTypeDef(name, cap_type,
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

    @property
    def tpl_properties(self):
        tpl_props = []
        properties = self._get_value(PROPERTIES, self.nodetemplate)
        if properties:
            for name, value in properties.iteritems():
                prop = PropertyDef(name, None, self.name, value)
                tpl_props.append(prop)
        return tpl_props

    def _add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    @property
    def relatednodes(self):
        return self.related.keys()

    def tpl_relation(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]

    def ref_property(self, cap, cap_name, property):
        requirs = self.tpl_requirements
        tpl_name = None
        if requirs:
            for r in requirs:
                for i, j in r.iteritems():
                    if i == cap:
                        tpl_name = j
                        break
            if tpl_name:
                tpl = NodeTemplate(tpl_name, self.nodetemplates)
                caps = tpl.tpl_capabilities
                for c in caps:
                    if c.name == cap_name:
                        if c.property == property:
                            return c.property_value
