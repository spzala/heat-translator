# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from translator.toscalib.elements.capabilitytype import CapabilityTypeDef
from translator.toscalib.elements.interfacestype import InterfacesTypeDef
from translator.toscalib.elements.properties import PropertyDef
from translator.toscalib.elements.relationshiptype import RelationshipType
from translator.toscalib.elements.statefulentitytype import StatefulEntityType


SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')


class NodeType(StatefulEntityType):
    '''Tosca built-in node type'''
    def __init__(self, type):
        super(NodeType, self).__init__()
        if type not in self.TOSCA_DEF.keys():
            raise ValueError("Node type %(ntype)s is not a valid TOSCA type."
                             % {'ntype': type})
        self.defs = self.TOSCA_DEF[type]
        self.type = type
        self.related = {}

    def _derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    @property
    def parentnode(self):
        if self._derivedfrom():
            return NodeType(self._get_value(DERIVED_FROM))

    @property
    def properties(self):
        '''returns a list of property objects '''
        properties = []
        props = self._get_value(PROPERTIES)
        if props:
            for prop in props:
                properties.append(PropertyDef(prop, self.type))
        return properties

    @property
    def relationship(self):
        '''returns a dictionary containing relationship to a particular
         node type '''
        relationship = {}
        requirs = self.requirements
        if requirs is None:
            requirs = self._get_value(REQUIREMENTS, None, True)
        if requirs:
            for req in requirs:
                for x, y in req.iteritems():
                    relation = self._get_relation(x, y)
                    rtype = RelationshipType(relation, x)
                    relatednode = NodeType(y)
                    relationship[rtype] = relatednode
        return relationship

    def _get_relation(self, key, ndtype):
        relation = None
        ntype = NodeType(ndtype)
        cap = ntype.capabilities
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

    @property
    def capabilities(self):
        '''returns a list of capability objects '''
        typecapabilities = []
        prop_name = None
        prop_val = None
        self.cap_prop = None
        self.cap_type = None
        caps = self._get_value(CAPABILITIES)
        if caps is None:
            caps = self._get_value(CAPABILITIES, None, True)
        if caps:
            for name, value in caps.iteritems():
                for x, y in value.iteritems():
                    if x == 'type':
                        self.__set_cap_type(y)
                    if x == 'properties':
                        self.__set_cap_prop(y)
                if self.cap_prop:
                    for prop, value in self.cap_prop.iteritems():
                        prop_name = prop
                        prop_val = value
                cap = CapabilityTypeDef(name, self.cap_type,
                                        self.type, prop_name, prop_val)
                typecapabilities.append(cap)
        return typecapabilities

    @property
    def requirements(self):
        return self._get_value(REQUIREMENTS)

    def interfaces(self):
        return self._get_value(INTERFACES)

    @property
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

    @property
    def lifecycle_operations(self):
        '''return available life cycle operations if found, None otherwise.'''
        ops = None
        interfaces = self.interfaces()
        if interfaces:
            i = InterfacesTypeDef(self.type, 'tosca.interfaces.node.Lifecycle')
            ops = i.lifecycle_ops
        return ops

    def __set_cap_type(self, value):
        self.cap_type = value

    def __set_cap_prop(self, value):
        self.cap_prop = value

    def capability(self, name):
        for key, value in self.capabilities:
            if key == name:
                return value

    def capability_type(self, name):
        for key, value in self.capability(name):
            if key == type:
                return value

    def _get_value(self, ndtype, defs=None, parent=None):
        value = None
        if defs is None:
            defs = self.defs
        if ndtype in defs:
            value = defs[ndtype]
        if parent and not value:
            p = self.parentnode
            while value is None:
                #check parent node
                if not p:
                    break
                if p and p.type == 'tosca.nodes.Root':
                    break
                value = p._get_value(ndtype)
                p = p.parentnode
        return value

    def _add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    @property
    def relatednodes(self):
        if not self.related:
            for relation, nodetype in self.relationship.iteritems():
                for tpl in self.TOSCA_DEF.keys():
                    if tpl == nodetype.type:
                        self.related[NodeType(tpl)] = relation
        return self.related.keys()
