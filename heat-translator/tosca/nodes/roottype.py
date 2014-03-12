from nodetypes_def import Nodetype_Def

class RootNodeType(object):
    '''Tosca root node type'''
    def __init__(self):
        #TODO
        self.name = 'tosca.nodes.Root'
        self.defs = Nodetype_Def()[self.name]

class RootRelationshipType(object):
    '''Tosca root relations type'''
    def __init__(self):
        #TODO
        pass  
    