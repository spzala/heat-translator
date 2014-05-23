#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

SECTIONS = (TYPE, PROPERTIES, MEDADATA, DEPENDS_ON, UPDATE_POLICY,
            DELETION_POLICY) = \
           ('type', 'properties', 'metadata',
            'depends_on', 'update_policy', 'deletion_policy')


class HotResource(object):
    ''' Base class for TOSCA node type translation to Heat resource type '''

    def __init__(self, nodetemplate, name=None, type=None, properties=None,
                 metadata=None, depends_on=None,
                 update_policy=None, deletion_policy=None):
        self.nodetemplate = nodetemplate
        if name:
            self.name = name
        else:
            self.name = nodetemplate.name
        self.type = type
        self.properties = properties
        # special case for HOT softwareconfig
        if type == 'OS::Heat::SoftwareConfig':
            self.properties['group'] = 'script'
        self.metadata = metadata
        if depends_on:
            self.depends_on = depends_on
        else:
            self.depends_on = []
        self.update_policy = update_policy
        self.deletion_policy = deletion_policy
        self.group_dependencies = {}

    def handle_properties(self):
        # the property can hold a value or the intrinsic function get_input
        # for value, copy it
        # for get_input, convert to get_param
        for prop in self.nodetemplate.tpl_properties:
            pass

    def handle_life_cycle(self):
        hot_resources = []
        deploy_lookup = {}
        interfaces_deploy_sequence = ['create', 'start', 'configure']

        # create HotResrouce for each interface used for deployment:
        # create, start, configure
        # ignore the other interfaces
        # observe the order:  create, start, configure
        # use the current HotResource for the first interface in this order

        # hold the original name since it will be changed during
        # the transformation
        node_name = self.name
        reserve_current = 'NONE'
        interfaces_actual = []
        for interface in self.nodetemplate.tpl_interfaces:
            interfaces_actual.append(interface.name)
        for operation in interfaces_deploy_sequence:
            if operation in interfaces_actual:
                reserve_current = operation
                break

        # create the set of SoftwareDeployment and SoftwareConfig for
        # the interface operations
        for interface in self.nodetemplate.tpl_interfaces:
            if interface.name in interfaces_deploy_sequence:
                config_name = node_name+'_'+interface.name+'_config'
                deploy_name = node_name+'_'+interface.name+'_deploy'
                hot_resources.append(
                    HotResource(self.nodetemplate,
                                config_name,
                                'OS::Heat::SoftwareConfig',
                                {'config':
                                    {'get_file': interface.implementation}}))
                if interface.name == reserve_current:
                    deploy_resource = self
                    self.name = deploy_name
                    self.type = 'OS::Heat::SoftwareDeployment'
                    self.properties = {'config': {'get_resource': config_name}}
                    deploy_lookup[interface.name] = self
                else:
                    deploy_resource = \
                        HotResource(self.nodetemplate,
                                    deploy_name,
                                    'OS::Heat::SoftwareDeployment',
                                    {'config': {'get_resource': config_name}})
                    hot_resources.append(deploy_resource)
                    deploy_lookup[interface.name] = deploy_resource

        # Add dependencies for the set of HOT resources in the sequence defined
        # in interfaces_deploy_sequence
        # TODO: find some better way to encode this implicit sequence
        group = {}
        for op, hot in deploy_lookup.iteritems():
            # position to determine potential preceding nodes
            op_index = interfaces_deploy_sequence.index(op)
            for preceding_op in \
                    reversed(interfaces_deploy_sequence[:op_index]):
                preceding_hot = deploy_lookup.get(preceding_op)
                if preceding_hot:
                    hot.depends_on.append(preceding_hot)
                    group[preceding_hot] = hot
                    break

        # save this dependency chain in the set of HOT resources
        self.group_dependencies.update(group)
        for hot in hot_resources:
            hot.group_dependencies.update(group)

        return hot_resources

    def handle_hosting(self):
        # handle hosting server for the OS:HEAT::SoftwareDeployment
        # from the TOSCA nodetemplate, traverse the relationship chain
        # down to the server
        if self.type == 'OS::Heat::SoftwareDeployment':
            # skip if already have hosting
            host_server = self.properties.get('server')
            if host_server is None:
                host_server = self.bottom_of_chain().\
                    properties['server']['get_resource']
                self.properties['server'] = {'get_resource': host_server}

    def top_of_chain(self):
        dependent = self.group_dependencies.get(self)
        if dependent is None:
            return self
        else:
            return dependent.top_of_chain()

    # TODO:  traverse using the relationship requirement:host in TOSCA
    def bottom_of_chain(self):
        if len(self.depends_on) == 0:
            return self
        else:
            for preceding in self.depends_on:
                return preceding.bottom_of_chain()

    def get_dict_output(self):
        resource_sections = {TYPE: self.type}
        if self.properties:
            resource_sections[PROPERTIES] = self.properties
        if self.metadata:
            resource_sections[MEDADATA] = self.metadata
        if self.depends_on:
            resource_sections[DEPENDS_ON] = []
            for depend in self.depends_on:
                resource_sections[DEPENDS_ON].append(depend.name)
        if self.update_policy:
            resource_sections[UPDATE_POLICY] = self.update_policy
        if self.deletion_policy:
            resource_sections[DELETION_POLICY] = self.deletion_policy

        return {self.name: resource_sections}
