from node_template import NodeTemplate
from relationshiptype import RelatonshipType

class NodeTpl:
    def __init__(self, nodetpl_object):
        self.name = nodetpl_object.get_name()
        self.related = {}

    def add_next(self,nodetpl,relationship):
        self.related[nodetpl] = relationship

    def get_relatednodetpls(self):
        return self.related.keys()

    def get_name(self):
        return self.name

    def get_relationship(self,nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]

class ToscaRelationshipGraph:
    '''Graph with Tosca Nodes connected via a specific relationship'''
    def __init__(self, tosca_profile):
        self.tosca_profile = tosca_profile
        self.nodetemplates = tosca_profile.nodetemplates()
        self.vertices = {}
        self.create()

    def create_vertex(self, ntpl):
        nodetpl = NodeTpl(ntpl)
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
        for ntpl in self.nodetemplates:
            self.create_vertex(ntpl)
            if ntpl.has_relationship:
                hosted_on = ntpl.get_hostedOn_relationship()
                connects_to = ntpl.get_connectsTo_relationship()
                depends_on = ntpl.get_dependsOn_relationship()
            if hosted_on:
                relationshiptype = RelatonshipType('host')
                self.createedge(relationshiptype, hosted_on, ntpl)
            for connect in connects_to:
                relationshiptype = RelatonshipType('database_endpoint')
                self.createedge(relationshiptype, connect, ntpl)
            for depends in depends_on:
                relationshiptype = RelatonshipType('dependency')
                self.createedge(relationshiptype, depends, ntpl)
                        
    def createedge(self, relationshiptype, node1, node2):
        for tpl in self.nodetemplates:
            if tpl.get_name() == node1:
                etpl = NodeTemplate(node1, tpl.get_value())
                self.create_edge(node2, etpl, relationshiptype)
