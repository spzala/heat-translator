import os
import logging
import toscalib.utils.yamlparser

log = logging.getLogger('tosca')


class EntityType(object):

    '''TOSCA definition file. '''
    TOSCA_DEF_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "TOSCA_definition.yaml")

    TOSCA_DEF = toscalib.utils.yamlparser.load_yaml(TOSCA_DEF_FILE)

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
