import os
from yaml_parser import Parser

rootnode_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "rootnode.yaml"
rootnode_def = Parser(rootnode_def_file).load()

class RootNodeType(object):
    '''Tosca root node type'''
    def __init__(self):
        #TODO
        self.name = 'tosca.nodes.Root'

class RootRelationshipType(object):
    '''Tosca root relations type'''
    def __init__(self):
        #TODO
        pass  
    