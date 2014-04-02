from statefulentitytype import StatefulEntityType

SECTIONS = (LIFECYCLE, CONFIGURE) = \
           ('tosca.interfaces.node.Lifecycle',
            'tosca.interfaces.relationship.Configure')


class InterfacesTypeDef(StatefulEntityType):
    '''Tosca built-in interfaces type'''
    def __init__(self, ntype, interfacetype):
        self.defs = self.TOSCA_DEF[interfacetype]
        self.nodetype = ntype
        self.type = interfacetype

    def lifecycle_ops(self):
        if self.type == LIFECYCLE:
            ops = []
            for name, value in self.defs.iteritems():
                ops.append(name)
            return ops

    def configure_ops(self):
        if self.type == CONFIGURE:
            ops = []
            for name, value in self.defs.iteritems():
                ops.append(name)
            return ops
