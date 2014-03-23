from entitytype import EntityType

class StatefulEntityType(EntityType):

    interfaces_node_lifecycle_operations = ['create', 'configure', 'start', 'stop', 'delete']
    
    interfaces_relationship_confiure_operations = ['post_configure_source', 'post_configure_target', 'add_target', 'remove_target']
    
    def __init__(self): 
        pass
