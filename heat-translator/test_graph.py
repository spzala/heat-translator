from tosca.elements.graph import ToscaGraph


class TestGraph():
    def __init__(self):
        pass

    def test(self):
        graph = ToscaGraph()
        vertices = graph.vertices
        for name, node in vertices.iteritems():
            #print name
            #props = node.properties()
            #for p in props:
                #print p.name
            for relatednode in node.get_relatednodes():
                print("( %s , %s )" % (node.get_type(),
                                       relatednode.get_type()))
                print node.get_relationship(relatednode).type
