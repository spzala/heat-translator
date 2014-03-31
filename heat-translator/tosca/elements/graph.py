from nodetype import NodeTypes, NodeType


class ToscaGraph:
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

    def create_vertex(self, node):
        self.vertices[node.type] = node

    def create_edge(self, node1, node2, relationship):
        if node1 not in self.vertices:
            self.create_vertex(node1)
        if node2 not in self.vertices:
            self.create_vertex(node2)
        self.vertices[node1.type].add_next(self.vertices[node2.type],
                                           relationship)

    def get_vertices(self):
        return self.vertices.keys()

    def get_vertex(self, node):
        if node in self.vertices:
            return self.vertices[node]

    def __iter__(self):
        return iter(self.vertices.values())

    def create(self):
        for node in self.nodetypes:
            if node.has_relationship():
                relation = node.relationship()
                for relation, nodetype in relation.iteritems():
                    for tpl in self.nodetypes:
                        if tpl.type == nodetype.type:
                            self.create_edge(node, nodetype, relation)
            self.create_vertex(node)
