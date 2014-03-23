from capabilitytype import CapabilityType
from properties import Property
from properties import Properties
from relationshiptype import RelatonshipType
from tosca.inputs import Input
from tosca.inputs import InputParameters
import nodetype

class NodeTemplate(nodetype.NodeType):
    ''' Node template from a Tosca profile.'''
    
    '''relationship variable holds relevant relationship type objects '''
    hostedon = []
    dependson = []
    connectsto = []
    def __init__(self, name, nodetemplate):
        super(NodeTemplate, self).__init__(nodetemplate['type'])
        self.name = name
        self.nodetemplate = nodetemplate
        if 'properties' in self.nodetemplate:
            self.profile_properties = Properties(self.nodetemplate['properties'])
        if self.has_capabilities():
            for capability in self.capabilities_type():
                self.nodetype_capabilities = []
                self.nodetype_capabilities.append(CapabilityType(capability))
        self.relationship()
        
    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.nodetemplate
    
    def get_type(self):
        return self.nodetemplate['type']
    
    def get_properties(self):
        if 'properties' in self.nodetemplate:
            return self.nodetemplate['properties']

    def get_interfaces(self):
        return self.nodetemplate['interfaces']
    
    def is_computeNode(self):
        return self.nodetemplate['type'] == 'tosca.nodes.Compute'
    
    def get_host(self):
        if "requirements" in self.nodetemplate:
            requirements = self.nodetemplate['requirements']
            for r in requirements:
                for key, value in r.iteritems():
                    if key == 'host':
                        return value
                
    def validate(self):
        self.validate_properties()
        self.validate_type()
        
    #TODO
    def validate_type(self):
        pass
    
    #TODO
    def validate_relationship(self):
        pass
    
    def validate_properties(self):
        '''validate that required properties for a particular nodetype is provided and matches constraints'''
        if self.get_properties():
            required_props = self.schema().required()
            for req in required_props:
                if req not in self.get_properties():
                    raise ValueError('Missing required property %s' %req)
            
            pp = Properties(self.get_properties())
            for property in pp:
                val = pp[property]
                if isinstance(val, dict):
                    for key, value in val.iteritems(): 
                        if key == "get_input": 
                            if self.get_input_ref(value) is not None:
                                val = value
                            #TODO: can't do data type validation because user input is not provided until runtime
                            #val = self.get_input_ref(val)
                Property(property, self.get_type(), val).validate()  
    
    def get_input_ref(self, ref):
        #get input reference, for example, get_input: db_user should return default value of db_user
        pass
    
    '''
    @classmethod
    def get_property_ref(cls, ref, t):
        #get property reference, for example, get_property: [ mysql, db_user ]
        item = ref[0]
        n = t._get_nodetemplates()[item]
        c = cls(item, n, t)
        for val in c.get_properties().itervalues():
            if isinstance(val, dict):
                for key, value in val.iteritems():           
                    if key == "get_input":
                        return c.get_input_ref(value)
    '''
    
    def has_relationship(self):
        return 'requirements' in self.nodetemplate
    
    def has_capabilities(self):
        return 'capabilities' in self.nodetemplate
    
    def capabilities_type(self):
        if self.has_capabilities():
            caps = []
            capabilities = self.nodetemplate['capabilities']
            for key in capabilities.iterkeys():
                caps.append(key)
            return caps

    def implicit_relationship(self):
        pass
    
    def relationship(self, key):
        ''' Relationship can be found in a two ways:
        1. explicit: Under the 'requirement' relationship is defined using a 
           - keyword (e.g. dependsOn) 
             find the keyword under the nodetype definition requirement section. Look into the capability 
             of the nodetype provided as value. Find the capability type for the keyword and use that to define
             relationship.
           - with a list (e.g. 
                            node: server 
                            relationship_type: hostedOn)
        2. implicit: no 'requirement' is provided then relationship need to be defined using the nodetype definition.
        '''
        pass

    
    def relationship(self):
        pass

    def get_capabilities(self):
        if  self.has_capabilities():
            return self.nodetemplate['capabilities']