import os
import yaml
import tosca.utils.yamlparser
from hot.hot_resource import HotResource


SECTIONS = (TYPE, PROPERTIES, REQUIREMENTS, INTERFACES, LIFECYCLE, INPUT) = \
           ('type', 'properties', 'requirements',
            'interfaces', 'lifecycle', 'input')

REQUIRES = (CONTAINER, DEPENDENCY, DATABASE_ENDPOINT, CONNECTION, HOST) = \
           ('container', 'dependency', 'database_endpoint',
            'connection', 'host')

INTERFACES_STATE = (CREATE, START, CONFIGURE, START, DELETE) = \
                   ('create', 'stop', 'configure', 'start', 'delete')

TOSCA_TO_HOT_TYPE = {'tosca.basetypes.nodes.Compute': 'OS::Nova::Server'}

TOSCA_TO_HOT_REQUIRES = {'container': 'server', 'host': 'server',
                         'dependency': 'depends_on', "connects": 'depends_on'}

TOSCA_TO_HOT_PROPERTIES = {'properites': 'input'}

resolved = []
order = []
interested_nodes = []


class TranslateNodeTemplates():
    '''Translate TOSCA Nodes to Heat Resources'''

    def __init__(self, nodetemplates, hot_template):
        self.nodetemplates = nodetemplates
        self.hot_template = hot_template
        nodefile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "mappings/tosca_to_heat_node_templates.yaml")
        mappings = tosca.utils.yamlparser.load_yaml(nodefile)
        self.type_translations = mappings['type_translation']
        self.property_translations = mappings['properties_translation']
    
    def translate(self):
        return self._translate_nodetemplates()
    
    @staticmethod
    def _translate(value, mapping, err_msg=None):
        try:
            return mapping[value]
        except KeyError as ke:
            if err_msg:
                raise KeyError(err_msg % value)
            else:
                print("Warning: No translation for '" + value + "' found.")
                raise ke
    
    def _translate_nodetemplates(self):

        hot_resources = []
        for resource in self.nodetemplates:
            hot_type = self._translate(resource.type, self.type_translations)
            hot_properties = resource.translate_HOT_properties()                 
            hot_resources.append(HotResource(resource.name, hot_type, 
                                             hot_properties))
        return hot_resources
