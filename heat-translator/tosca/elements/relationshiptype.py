from statefulentitytype import StatefulEntityType

SECTIONS = (DERIVED_FROM, VALIDTARGETS) = \
           ('derived_from', 'valid_targets')


class RelationshipType(StatefulEntityType):
    '''Tosca built-in relationship type'''
    def __init__(self, type):
        super(RelationshipType, self).__init__()
        self.defs = self.TOSCA_DEF[type]
        self.type = type

    def name(self):
        return self.type

    def derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    def valid_targets(self):
        return self._get_value(VALIDTARGETS)

    def _get_value(self, rtype):
        if rtype in self.defs:
            return self.defs[rtype]
