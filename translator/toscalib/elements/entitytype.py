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

import logging
import os

import translator.toscalib.utils.yamlparser

log = logging.getLogger('tosca')


class EntityType(object):

    '''TOSCA definition file. '''
    TOSCA_DEF_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "TOSCA_definition.yaml")

    TOSCA_DEF = translator.toscalib.utils.yamlparser.load_yaml(TOSCA_DEF_FILE)

    RELATIONSHIP_TYPE = (DEPENDSON, HOSTEDON, CONNECTSTO) = \
                        ('tosca.relationships.DependsOn',
                         'tosca.relationships.HostedOn',
                         'tosca.relations.ConnectsTo')

    '''Properties can be used by various TOSCA elements like
    node type, relationship type etc. '''
    PROPERTIES_KEYS = (
        TYPE, REQUIRED, DESCRIPTION, DEFAULT, CONSTRAINTS,
    ) = (
        'type', 'required', 'description', 'default', 'constraints'
    )

    PROPERTIES_TYPES = (
        INTEGER,
        STRING, NUMBER, BOOLEAN,
        LIST
    ) = (
        'integer',
        'string', 'number', 'boolean',
        'list'
    )

    def __init__(self):
        pass
