import os
from yaml_parser import Parser

relationship_def_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + "relationshiptype_def.yaml"
relationship_def = Parser(relationship_def_file).load()

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

RELATIONSHIP_TYPE = (DEPENDSON, HOSTEDON, CONNECTSTO) = \
           ('dependency', 'host', 'database_endpoint')

class RelatonshipType(object):
    ''''Tosca relationship type'''
    def __init__(self, relationshiptype): 
        super(RelatonshipType, self).__init__()
        if relationshiptype == DEPENDSON:
            self.relationshiptype = 'tosca.relationships.DependsOn'
        if relationshiptype == HOSTEDON:
            self.relationshiptype = 'tosca.relationships.HostedOn'
        if relationshiptype == CONNECTSTO:
            self.relationshiptype = 'tosca.relations.ConnectsTo'

    def name(self):
        return self.relationshiptype
    
    def derivedfrom(self, relationshiptype):
        return self.getKey(relationshiptype, DERIVED_FROM)

    def valid_targets(self, relationshiptype):
        return self.getkey(relationshiptype, VALIDTARGETS)
    
    def getkey(self, nodetype, key):
        nodetype = self.defs[nodetype]
        for name, value in nodetype.iteritems():
            if name == key:
                return value