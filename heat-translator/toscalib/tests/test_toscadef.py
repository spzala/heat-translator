from toscalib.elements.nodetype import NodeType
from base import TestBase


class ToscaDefTest(TestBase):

    def test_nodetype(self):
        computetype = NodeType('tosca.nodes.Compute')
        self.assertEqual(computetype.type, "tosca.nodes.Compute")
        self.assertEqual(computetype.parentnode.type, "tosca.nodes.Root")
        self.assertEqual(
            ['tosca.capabilities.Container'],
            [c.type for c in computetype.capabilities])
        self.assertEqual(
            ['disk_size', 'mem_size', 'num_cpus',
             'os_arch', 'os_version', 'os_distribution',
             'os_type', 'ip_address'],
            [p.name for p in computetype.properties])
        self.assertEqual(computetype.requirements, None)

        sctype = NodeType('tosca.nodes.SoftwareComponent')
        for r in sctype.requirements:
            self.assertEqual(r, {'host': 'tosca.nodes.Compute'})
        self.assertEqual(
            [{'host': 'tosca.nodes.Compute'}],
            [r for r in sctype.requirements])

        self.assertEqual(
            [('tosca.relationships.HostedOn', 'tosca.nodes.Compute')],
            [(relation.type, node.type) for
             relation, node in sctype.relationship.iteritems()])

        wptype = NodeType('tosca.nodes.WebApplication.WordPress')
        self.assertEqual(
            ['configure', 'create', 'delete', 'start', 'stop'],
            sorted(wptype.lifecycle_operations))
