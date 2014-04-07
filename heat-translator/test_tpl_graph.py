class TestTPLGraph():
    '''this class is just for testing as an aid while development.'''
    def __init__(self, tosca):
        self.tosca = tosca

    def test(self):
        graph = self.tosca.graph
        vertices = graph.vertices
        for name, node in vertices.iteritems():
            #print name
            #props = node.properties()
            #for p in props:
                #print p.name
            for relatednode in node.relatednodes:
                print("( %s , %s )" % (node.name,
                                       relatednode.name))
                print node.tpl_relation(relatednode).type
