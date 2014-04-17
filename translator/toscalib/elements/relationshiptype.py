from translator.toscalib.elements.statefulentitytype import StatefulEntityType

SECTIONS = (DERIVED_FROM, VALIDTARGETS) = \
           ('derived_from', 'valid_targets')


class RelationshipType(StatefulEntityType):
    '''Tosca built-in relationship type'''
    def __init__(self, type, keyword=None):
        super(RelationshipType, self).__init__()
        self.defs = self.TOSCA_DEF[type]
        self.type = type
        self.keyword = keyword

    @property
    def name(self):
        return self.type

    @property
    def derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    @property
    def valid_targets(self):
        return self._get_value(VALIDTARGETS)

    def _get_value(self, rtype):
        if rtype in self.defs:
            return self.defs[rtype]
