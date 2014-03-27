from properties import Property
from properties import Properties
from tosca.elements.relationshiptype import RelationshipType
from tosca.inputs import Input
from tosca.inputs import InputParameters
from tosca.elements.nodetype import NodeType
import tosca.elements.relationshiptype

class NodeTemplate(NodeType):
    ''' Node template from a Tosca profile.'''
    
    '''relationship variable holds relevant relationship type objects '''
    hostedon = []
    dependson = []
    connectsto = []
    def __init__(self, name, nodetemplate):
        super(NodeTemplate, self).__init__(nodetemplate['type'])
        self.name = name
        self.nodetemplate = nodetemplate
        if 'properties' in self.nodetemplate:
            self.properties = self.properties()
            for p in self.properties:
                pass
                #print p.name
        if 'capabilities' in self.nodetemplate:
            self.capabilities = self.capabilities()
            for c in self.capabilities:
                pass
                #print c.name
                #print c.type
                #print self.name
        if 'interfaces' in self.nodetemplate:
            self.lifecycle_ops = self.lifecycle_operations()
            #print self.lifecycle_ops
            #print self.name
        
        if 'requirements' in self.nodetemplate:
            self.relationship = self.relationship()
            '''
            for relationship, node in self.relationship.iteritems():
               print self.name
               print relationship
               print node
            '''
    
    @classmethod
    def get_relation(cls, key, type):
        relation = None
        ntype = NodeType(type)
        cap = ntype.capabilities()
        for c in cap:
            if c.name == key:
                rtypedef = tosca.elements.relationshiptype.relationship_def
                for relationship, properties in rtypedef.iteritems():
                    for x, y in properties.iteritems():
                        if c.type in y:
                            relation = relationship
                            break
                if relation:
                    break
        return relation
        
    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.nodetemplate
    
    def get_type(self):
        return self.nodetemplate['type']