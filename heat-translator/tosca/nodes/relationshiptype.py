import os
from yaml_loader import Loader
from roottype import RootRelationshipType

relationship_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + "relationshiptype_def.yaml"
relationship_def = Loader(relationship_def_file).load()

class RelationshipType_Def(object):
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

class RelatonshipType(RootRelationshipType):
    ''''Tosca relationship type'''
    def __init__(self, relationshiptype): 
        super(RelatonshipType, self).__init__()
        self.relationshiptype = relationshiptype

    def derivedfrom(self, relationshiptype):
        return self.getKey(relationshiptype, DERIVED_FROM)

    def validtargets(self, relationshiptype):
        return self.getkey(relationshiptype, VALIDTARGETS)
    
    def getkey(self, nodetype, key):
        nodetype = self.defs[nodetype]
        for name, value in nodetype.iteritems():
            if name == key:
                return value
        