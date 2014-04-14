SECTIONS = (TYPE, PROPERTIES, MEDADATA, DEPENDS_ON, UPDATE_POLICY, 
            DELETION_POLICY) = \
           ('type', 'properties', 'metadata',
            'depends_on', 'update_policy', 'deletion_policy')

class HotResource(object):


    def __init__(self, name, type, properties=None, metadata=None, depends_on=None, 
                 update_policy=None, deletion_policy=None):
        self.name = name
        self.type = type
        self.properties = properties
        self.metadata = metadata
        self.depends_on = depends_on
        self.update_policy = update_policy
        self.deletion_policy = deletion_policy

    def get_dict_output(self):
        resource_sections = {TYPE: self.type}
        if self.properties:
            resource_sections[PROPERTIES] = self.properties
        if self.metadata:
            resource_sections[MEDADATA] = self.metadata
        if self.depends_on:
            resource_sections[DEPENDS_ON] = self.depends_on
        if self.update_policy:
            resource_sections[UPDATE_POLICY] = self.update_policy
        if self.deletion_policy:
            resource_sections[DELETION_POLICY] = self.deletion_policy

        return { self.name: resource_sections }
