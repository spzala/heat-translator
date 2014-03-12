from nodetypes_def import Nodetype_Def

class CapabilityType(object):
    '''Capability type for a given node type'''
    def __init__(self, nodetype): 
        self.nodetype = nodetype
        self.capabilities = Nodetype_Def().capabilities(self.nodetype)
    
    def capabilities(self):
        if self.capabilities:
            return self.capabilities
    
    #TODO - add more capabilities methods