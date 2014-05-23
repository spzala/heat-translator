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

from translator.hot.tosca.tosca_server import ToscaServer
from translator.hot.tosca.tosca_webserver import ToscaWebserver
from translator.hot.tosca.tosca_mysql_dbms import ToscaMysqlDbms
from translator.hot.tosca.tosca_mysql_database import ToscaMysqlDatabase
from translator.hot.tosca.tosca_wordpress import ToscaWordpress

SECTIONS = (TYPE, PROPERTIES, REQUIREMENTS, INTERFACES, LIFECYCLE, INPUT) = \
           ('type', 'properties', 'requirements',
            'interfaces', 'lifecycle', 'input')

REQUIRES = (CONTAINER, DEPENDENCY, DATABASE_ENDPOINT, CONNECTION, HOST) = \
           ('container', 'dependency', 'database_endpoint',
            'connection', 'host')

INTERFACES_STATE = (CREATE, START, CONFIGURE, START, DELETE) = \
                   ('create', 'stop', 'configure', 'start', 'delete')

# dict to look up HOT translation class, can be replaced later by function
# to scan the classes in translator.hot.tosca
TOSCA_TO_HOT_TYPE = {'tosca.nodes.Compute': ToscaServer,
                     'tosca.nodes.WebServer': ToscaWebserver,
                     'tosca.nodes.DBMS': ToscaMysqlDbms,
                     'tosca.nodes.Database': ToscaMysqlDatabase,
                     'tosca.nodes.WebApplication.WordPress': ToscaWordpress}

TOSCA_TO_HOT_REQUIRES = {'container': 'server', 'host': 'server',
                         'dependency': 'depends_on', "connects": 'depends_on'}

TOSCA_TO_HOT_PROPERTIES = {'properties': 'input'}


class TranslateNodeTemplates():
    '''Translate TOSCA NodeTemplates to Heat Resources.'''

    def __init__(self, nodetemplates, hot_template):
        self.nodetemplates = nodetemplates
        self.hot_template = hot_template

    def translate(self):
        return self._translate_nodetemplates()

    def _translate_nodetemplates(self):
        hot_resources = []
        hot_lookup = {}

        # Copy the TOSCA graph: nodetemplate
        for node in self.nodetemplates:
            hot_node = TOSCA_TO_HOT_TYPE[node.type](node)
            hot_resources.append(hot_node)
            hot_lookup[node] = hot_node

        # Handle life cycle operations: this may expand each node into
        # multiple HOT resources and may change their name
        lifecycle_resources = []
        for resource in hot_resources:
            expanded = resource.handle_life_cycle()
            lifecycle_resources += expanded
        hot_resources += lifecycle_resources

        # Copy the initial dependencies based on the relationship in
        # the TOSCA template
        for node in self.nodetemplates:
            for node_depend in node.relatednodes:
                # if the source of dependency is a server, add dependency
                # as properties.get_resource
                if node_depend.type == 'tosca.nodes.Compute':
                    hot_lookup[node].properties['server'] = \
                        {'get_resource': hot_lookup[node_depend].name}
                # for all others, add dependency as depends_on
                else:
                    hot_lookup[node].depends_on.append(hot_lookup[node_depend].
                                                       top_of_chain())

        # handle hosting relationship
        for resource in hot_resources:
            resource.handle_hosting()

        # Handle properties
        for resource in hot_resources:
            resource.handle_properties()

        return hot_resources