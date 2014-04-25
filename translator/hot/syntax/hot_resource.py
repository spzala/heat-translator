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

    def __init__(self, nodetemplate, name=None, type=None, properties=None, metadata=None,
                 depends_on=None, update_policy=None, deletion_policy=None):
        self.nodetemplate = nodetemplate
        if name:
            self.name = name
        else:
            self.name = nodetemplate.name
        self.type = type
        self.properties = properties
        self.metadata = metadata
        if depends_on:
            self.depends_on = depends_on
        else:
            self.depends_on = []
        self.update_policy = update_policy
        self.deletion_policy = deletion_policy

    def handle_properties(self):
        pass
    
    def handle_life_cycle(self):
        hot_resources = []
        deploy_lookup = {}

        # create HotResrouce for each interface
        # the create interface is special since it's the minimum required
        # so use the current HotResource for create
        # hold the original name since it will be changed during the transformation
        node_name = self.name
        for interface in self.nodetemplate.tpl_interfaces:
            config_name = node_name+'_'+interface.name+'_config'
            deploy_name = node_name+'_'+interface.name+'_deploy'
            hot_resources.append(HotResource(self.nodetemplate, 
                                         config_name, 
                                         'OS::Heat::SoftwareConfig', 
                                         {'config':interface.implementation}))
            if interface.name=='create':
                deploy_resource = self
                self.name = deploy_name
                self.type = 'OS::Heat::SoftwareDeployment'
                self.properties = {'config': config_name}
            else:
                deploy_resource = HotResource(self.nodetemplate, 
                                              deploy_name, 
                                              'OS::Heat::SoftwareDeployment', 
                                              {'config':config_name})
            hot_resources.append(deploy_resource)
            deploy_lookup[interface.name] = deploy_resource

        
        # Add dependencies for the set of HOT resources in the sequence:  create, start, configure
        # todo: find some better way to encode this implicit sequence
        create_resource=deploy_lookup.get('create')
        start_resource=deploy_lookup.get('start')
        configure_resource=deploy_lookup.get('configure')
        if configure_resource:
            if start_resource:
                configure_resource.depends_on.append(start_resource.name)
            elif create_resource:
                configure_resource.depends_on.append(create_resource.name)
        if start_resource:
            if create_resource:
                start_resource.depends_on.append(create_resource.name)
                
        return hot_resources

        
    def get_dict_output(self):
        resource_sections = {TYPE: self.type}
        if hasattr(self, 'properties'):
            resource_sections[PROPERTIES] = self.properties
        if hasattr(self, 'metadata'):
            resource_sections[MEDADATA] = self.metadata
        if hasattr(self, 'depends_on'):
            resource_sections[DEPENDS_ON] = self.depends_on
        if hasattr(self, 'update_policy'):
            resource_sections[UPDATE_POLICY] = self.update_policy
        if hasattr(self, 'deletion_policy'):
            resource_sections[DELETION_POLICY] = self.deletion_policy

        return {self.name: resource_sections}
