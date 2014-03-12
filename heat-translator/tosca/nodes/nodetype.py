from nodetypes_def import Nodetype_Def
from roottype import RootNodeType
from relationshiptype import RelatonshipType

class NodeType(RootNodeType):
    ''' Tosca node type as per the node type definition '''
    def __init__(self, nodetype): 
        super(NodeType, self).__init__()
        self.nodetype = nodetype
    
    def get_properties(self):
        ''' get properties for a given node type'''
        return Nodetype_Def().properties(self.nodetype)

    def get_capabilities(self):
        ''' get capabilities for a given node type'''
        return Nodetype_Def().capabilities(self.nodetype)
    
    def get_parentnode(self):
        ''' get parent node for a given node type'''
        return Nodetype_Def().derivedfrom(self.nodetype)
    
    def get_requirements(self):
        ''' get requirements for a given node type'''
        return Nodetype_Def().requirements(self.nodetype)
    
    def get_interfaces(self):
        ''' get interfaces for a given node type'''
        return Nodetype_Def().interfaces(self.nodetype)
    
    def get_relationshiptype(self):
        pass #return object
    
    def parent_node(self):
        parent_node = None
        derived = self.get_properties()
        if derived:
            if 'derived_from' in derived:
                parent_node = derived['derived_from']
            
    def has_parent(self):
        return self.parent_node() is not None
        
    