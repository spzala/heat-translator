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

        #create HotResrouce for the interfaces except the first
        for interface in self.nodetemplate.tpl_interfaces[1:]:
            config_name = self.name+'_'+interface.name+'_config'
            hot_resources.append(HotResource(self.nodetemplate, 
                                         config_name, 
                                         'OS::Heat::SoftwareConfig', 
                                         {'config':interface.implementation}))
            hot_resources.append(HotResource(self.nodetemplate, 
                                         self.name+'_'+interface.name+'_deploy', 
                                         'OS::Heat::SoftwareDeployment', 
                                         {'config':config_name}))
        
        # let the current HotResource be the first interface
        if len(self.nodetemplate.tpl_interfaces) >=1:
            interface = self.nodetemplate.tpl_interfaces[0]
            config_name = self.name+'_'+interface.name+'_config'
            self.name +='_'+interface.name+'_deploy'
            self.type = 'OS::Heat::SoftwareDeployment'
            self.properties = {'config': config_name}
            hot_resources.append(HotResource(self.nodetemplate, 
                                             config_name, 
                                             'OS::Heat::SoftwareConfig', 
                                             {'config':interface.implementation}))
        
        return hot_resources

    def _software_deployment_for_interface(self, implementation):
        # sequence:  create, start, configure
 
        deploy_name = self.name+'_'+lifecycle+'_deploy'
        deploy_properties = {'config': config_name }
        hot_deploy = HotResource(self.nodetemplate, deploy_name, 'OS::Heat::SoftwareDeployment', deploy_properties)
            
        hot_resources.append(hot_deploy)
        hot_resources.append(hot_config)
            
        return hot_resources
    
    def _software_config_for_interface(self, lifecycle, action):
        config_name = self.name+'_'+lifecycle+'_config'
        config_properties = {'config': self._get_implementation(action)}
        hot_config = HotResource(self.nodetemplate, config_name, 'OS::Heat::SoftwareConfig', config_properties)
        pass
    
    def _get_implementation(self, action):
        if isinstance(action,basestring):
            return {'getfile': action}
        elif isinstance(action,dict):
            return {'getfile': action['implementation']}
        
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
