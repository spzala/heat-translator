from statefulentitytype import StatefulEntityType

SECTIONS = (LIFECYCLE, CONFIGURE) = \
           ('tosca.interfaces.node.Lifecycle',
            'tosca.interfaces.relationship.Configure')


class InterfacesTypeDef(StatefulEntityType):
    '''Tosca built-in interfaces type'''
    def __init__(self, ntype, interfacetype,
                 tpl_name=None, name=None, value=None):
        if ntype:
            self.defs = self.TOSCA_DEF[interfacetype]
        self.nodetype = ntype
        self.tpl_name = tpl_name
        self.type = interfacetype
        self.name = name
        self.value = value
        self.implementation = None
        self.input = None
        if value:
            if isinstance(self.value, dict):
                for i, j in self.value.iteritems():
                    if i == 'implementation':
                        self.implementation = j
                    if i == 'input':
                        self.input = j
            else:
                self.implementation = value

    def lifecycle_ops(self):
        if self.defs:
            if self.type == LIFECYCLE:
                ops = []
                for name, value in self.defs.iteritems():
                    ops.append(name)
                return ops

    def configure_ops(self):
        if self.defs:
            if self.type == CONFIGURE:
                ops = []
                for name, value in self.defs.iteritems():
                    ops.append(name)
                return ops
