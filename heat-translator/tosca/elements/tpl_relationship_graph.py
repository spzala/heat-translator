
class ToscaGraph(object):
    '''Graph of Tosca Node Templates connected via a specific relationship'''
    def __init__(self, nodetemplates):
        self.nodetemplates = nodetemplates
        self.vertices = {}
        self.create()

    def create_vertex(self, node):
        self.vertices[node.name] = node

    def create_edge(self, node1, node2, relationship):
        if node1 not in self.vertices:
            self.create_vertex(node1)
        if node2 not in self.vertices:
            self.create_vertex(node2)
        self.vertices[node1.name]._add_next(self.vertices[node2.name],
                                            relationship)

    def get_vertices(self):
        return self.vertices.keys()

    def get_vertex(self, node):
        if node in self.vertices:
            return self.vertices[node]

    def __iter__(self):
        return iter(self.vertices.values())

    def create(self):
        for node in self.nodetemplates:
            if node.tpl_relationship:
                relation = node.tpl_relationship
                for relation, nodetpls in relation.iteritems():
                    for tpl in self.nodetemplates:
                        if tpl.name == nodetpls.name:
                            self.create_edge(node, nodetpls, relation)
            self.create_vertex(node)
