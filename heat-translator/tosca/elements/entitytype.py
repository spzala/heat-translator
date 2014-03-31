class EntityType(object):
    '''Properties can be used be varios Tosca elements like
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
