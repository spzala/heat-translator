from nodetype import *
from relationshiptype import RelationshipType

class Node:
    def __init__(self, nodetpl_object):
        self.type = nodetpl_object.type
        self.related = {}

    def add_next(self,nodetpl,relationship):
        self.related[nodetpl] = relationship

    def get_relatednodes(self):
        return self.related.keys()

    def get_type(self):
        return self.type

    def get_relationship(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]

class RelationshipGraph:
    '''Graph of Tosca Nodes connected via a specific relationship'''
    def __init__(self):
        self.nodetypes = self.nodetypes()
        self.vertices = {}
        self.create()

    def nodetypes(self):
        nodetypes = []
        for node in NodeTypes():
            nodetypes.append(NodeType(node))
        return nodetypes
            
    def create_vertex(self, ntpl):
        nodetpl = Node(ntpl)
        self.vertices[ntpl] = nodetpl
        return nodetpl

    def create_edge(self, ntpl1, ntpl2, relationship):
        if ntpl1 not in self.vertices:
            vertex = self.create_vertex(ntpl1)
        if ntpl2 not in self.vertices:
            vertex = self.create_vertex(ntpl2)
        self.vertices[ntpl1].add_next(self.vertices[ntpl2], relationship)

    def get_vertices(self):
        return self.vertices.keys()
    
    def get_vertex(self, ntpl):
        if ntpl in self.vertices:
            return self.vertices[n]

    def __iter__(self):
        return iter(self.vertices.values())
    
    def create(self):  
        for ntpl in self.nodetypes:
            self.create_vertex(ntpl)
            if ntpl.has_relationship():
                relation = ntpl.relationship()
                for key, value in relation.iteritems():
                    self.createedge(key, value, ntpl)
                        
    def createedge(self, relationshiptype, node1, node2):
        rtype = RelationshipType(relationshiptype)
        for tpl in self.nodetypes:
            if tpl.type == node1:
                etpl = NodeType(node1)
                self.create_edge(node2, etpl, rtype)
