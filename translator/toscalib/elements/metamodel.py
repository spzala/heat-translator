# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from translator.toscalib.elements.nodetype import NodeType
from translator.toscalib.elements.statefulentitytype import StatefulEntityType


class ToscaMetaModelGraph(StatefulEntityType):
    '''Graph of Tosca Nodes connected via a specific relationship'''
    def __init__(self):
        self.nodetypes = self._nodetypes()
        self.vertices = {}
        self._create()

    def _nodetypes(self):
        nodetypes = []
        for node in self.TOSCA_DEF:
            if 'tosca.nodes' in node:
                nodetypes.append(NodeType(node))
        return nodetypes

    def _create_vertex(self, node):
        self.vertices[node.type] = node

    def create_edge(self, node1, node2, relationship):
        if node1 not in self.vertices:
            self._create_vertex(node1)
        if node2 not in self.vertices:
            self._create_vertex(node2)
        self.vertices[node1.type].add_next(self.vertices[node2.type],
                                           relationship)

    @property
    def verticeskeys(self):
        return self.vertices.keys()

    def vertex(self, node):
        if node in self.vertices:
            return self.vertices[node]

    def __iter__(self):
        return iter(self.vertices.values())

    def _create(self):
        for node in self.nodetypes:
            if node.relationship:
                relation = node.relationship()
                for relation, nodetype in relation.iteritems():
                    for tpl in self.nodetypes:
                        if tpl.type == nodetype.type:
                            self.create_edge(node, nodetype, relation)
            self._create_vertex(node)
