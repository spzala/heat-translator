
class ToscaGraph(object):
    '''Graph of Tosca Node Templates connected via a specific relationship'''
    def __init__(self, nodetemplates):
        self.nodetemplates = nodetemplates
        self.vertices = {}
        self._create()

    def _create_vertex(self, node):
        self.vertices[node.name] = node

    def _create_edge(self, node1, node2, relationship):
        if node1 not in self.vertices:
            self._create_vertex(node1)
        self.vertices[node1.name]._add_next(node2,
                                            relationship)

    def vertex(self, node):
        if node in self.vertices:
            return self.vertices[node]

    def __iter__(self):
        return iter(self.vertices.values())

    def _create(self):
        for node in self.nodetemplates:
            if node.tpl_relationship:
                relation = node.tpl_relationship
                for relation, nodetpls in relation.iteritems():
                    for tpl in self.nodetemplates:
                        if tpl.name == nodetpls.name:
                            self._create_edge(node, tpl, relation)
            self._create_vertex(node)
