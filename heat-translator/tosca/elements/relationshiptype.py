import os
from yaml_parser import Parser
from statefulentitytype import StatefulEntityType

relationship_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "relationshiptypedef.yaml"
relationship_def = Parser(relationship_def_file).load()

class RelationshipTypeDef(object):
    '''Load relationship types '''
    def __init__(self):
        self.defs = relationship_def
            
    def __contains__(self, key):
        return key in self.defs

    def __iter__(self):
        return iter(self.defs)

    def __len__(self):
        return len(self.defs)

    def __getitem__(self, key):
        '''Get a section.'''
        return self.defs[key]

SECTIONS = (DERIVED_FROM, VALIDTARGETS) = \
           ('derived_from', 'valid_targets')

RELATIONSHIP_TYPE = (DEPENDSON, HOSTEDON, CONNECTSTO) = \
           ('dependency', 'host', 'database_endpoint')

    
class RelationshipType(StatefulEntityType):
    '''Tosca built-in relationship type'''
    def __init__(self, type):
        super(RelationshipType, self).__init__()
        self.type = type
        self.defs = RelationshipTypeDef()[type]

    def name(self):
        return self.type
    
    def derivedfrom(self):
        return self._get_value(DERIVED_FROM)

    def valid_targets(self):
        return self._get_value(VALIDTARGETS)
    
    def _get_value(self, type):
        if type in self.defs:
            return self.defs[type]
        
class Relationship(object):
    '''node type relationship ''' 
    def __init__(self, type, related_from, related_to): 
        self.type = type
        self.related_from = related_from
        self.related_to = related_to  