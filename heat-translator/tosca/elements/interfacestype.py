import os
from yaml_parser import Parser

interfaces_def_file = (os.path.dirname(os.path.abspath(__file__))
                       + os.sep + 'defs' + os.sep + "interfacesdef.yaml")
interfaces_def = Parser(interfaces_def_file).load()

SECTIONS = (LIFECYCLE, CONFIGURE) = \
           ('tosca.interfaces.node.Lifecycle',
            'tosca.interfaces.relationship.Configure')


class InterfacesTypeDefs(object):
    '''Tosca built-in interfaces types'''
    def __init__(self):
        self.defs = interfaces_def

    def __contains__(self, key):
        return key in self.defs

    def __iter__(self):
        return iter(self.defs)

    def __len__(self):
        return len(self.defs)

    def __getitem__(self, key):
        '''Get a section.'''
        return self.defs[key]


class InterfacesTypeDef(object):
    '''Tosca built-in interfaces type'''
    def __init__(self, ntype, interfacetype):
        self.nodetype = ntype
        self.type = interfacetype
        self.defs = InterfacesTypeDefs()[self.type]

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
