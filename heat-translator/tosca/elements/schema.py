from yaml_parser import Parser
import os

schema_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'defs' + os.sep + 'nodetypeschema.yaml'
schema = Parser(schema_file).load()

class Schema(object):
    '''Node type schema'''
    
    TYPES = (
        INTEGER,
        STRING, NUMBER, BOOLEAN,
        LIST
    ) = (
        'integer',
        'string', 'number', 'boolean',
        'list'
    )
    
    KEYS = (
        TYPE, REQUIRED, DESCRIPTION, DEFAULT, CONSTRAINTS,
    ) = (
        'type', 'required', 'description', 'default', 'constraints'
    )
    
    def __init__(self, nodetype): 
        self.nodetype = nodetype
        self.nodes = self._set_nodes()
    
        '''set a list of node names from the schema'''
    def _set_nodes(self):
        sections = []
        if isinstance(schema, dict):
            for key in schema.iterkeys():
                sections.append(key)
        return sections
    
    def _get_section(self, section_name):
        section = {}
        if section_name in self.nodes:
            return schema[section_name]
        return section
    
    ''' return true if property is a required for a given node '''
    def is_required(self, property_name):
        return property_name in self.required()
    
    ''' get schemata for a given node type'''
    def get_schemata(self):
        return self._get_section(self.nodetype)
    
    ''' get schema for a given property'''
    def get_schema(self, property_name):
        schema = {}
        schemata = self.get_schemata()
        for prop_key, prop_vale in schemata.iteritems():
            if prop_key == property_name:
                for attr, value in prop_vale.iteritems():
                    schema[attr] = value
        return schema
    
    def get_type(self, property_name):
        return self.get_schema(property_name)[self.TYPE]
    
    def get_constraints(self, property_name):
        s = self.get_schema(property_name)
        if self.CONSTRAINTS in s:
            return s[self.CONSTRAINTS]
    
    def get_description(self, property_name):
        import pdb
        pdb.set_trace()
        return self.get_schema(property_name)[self.DESCRIPTION]   
    
    def get_greater_or_equal(self, property_name):
        #TODO
        pass
    
    def get_equal(self, property_name):
        #TODO
        pass
                
    ''' list all the requirement for a given node type '''
    def required(self):
        required = []
        schemata = self.get_schemata()
        for prop_key, prop_vale in schemata.iteritems():
            for attr, value in prop_vale.iteritems():
                if attr == self.REQUIRED and value:
                    required.append(prop_key)
        return required