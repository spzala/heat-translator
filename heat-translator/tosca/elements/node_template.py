from capabilitytype import CapabilityType
from properties import Property
from properties import Properties
from relationshiptype import RelatonshipType
from nodetype import NodeType
from tosca.inputs import InputParameters
from tosca.inputs import Input

class NodeTemplate(NodeType):
    ''' Node template from a Tosca profile.'''
    def __init__(self, name, nodetemplate):
        super(NodeTemplate, self).__init__(nodetemplate['type'])
        self.name = name
        self.nodetemplate = nodetemplate
        if self.has_hostedon_relationship():
            self.hosted_on = RelatonshipType('host')
        if self.has_dependson_relationship():
            self.depends_on = RelatonshipType('dependency')
        if self.has_connectto_relationship():
            self.connects_to = RelatonshipType('database_endpoint')
        if self.has_capabilities():
            for capability in self.capabilities_type():
                self.nodetype_capabilities = []
                self.nodetype_capabilities.append(CapabilityType(capability))
        
    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.nodetemplate
    
    def get_type(self):
        return self.nodetemplate['type']
    
    def get_properties(self):
        if 'properties' in self.nodetemplate:
            return self.nodetemplate['properties']
    
    def get_parent_properties(self, node=None):
        properties = {}
        if node is None:
            node = self.parentNode()
            properties = self.node.get_properties()
        parent_node = node.parent_node()
        if parent_node():
            node = NodeType(parent_node)
            self.get_parent_properties(parent_node)

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
        nodetype = self.get_type()
        required_props = self.schema().required()
        for req in required_props:
            if self.get_properties():
                if req not in self.get_properties():
                    raise ValueError('Missing required property %s' %req)
        if self.get_properties():
            for prop, val in self.get_properties().iteritems():
                if isinstance(val, dict):
                    for key, value in val.iteritems():           
                        if key == "get_input":
                            #TODO 
                            #val = self.get_input_ref(value)
                            #break
                            pass
                        if key == "get_property":
                            pass
                            #TODO val = self.get_property_ref(value, self.tosca)
                if val is not None:
                    Property(prop, self.get_type(), val).validate()
    
    ''' 
    def get_input_ref(self, ref):
        #get input reference, for example, get_input: db_user
        input_val = self.tosca.get_inputs()[ref]
        if Input(ref, input_val).has_default():
            return Input(ref, input_val).get_default()
    
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
    
    def relationship(self):
        relationship = []
        relationship.append(self.get_hostedOn_relationship())
        relationship.append(self.get_dependsOn_relationship())
        relationship.append(self.get_connectsTo_relationship())
    
    def get_hostedOn_relationship(self):
        host = None
        hosted_on = self._get_relationship('host')
        if hosted_on:
            for r in  self._get_relationship('host'):
                host = r
        return host
    
    def get_dependsOn_relationship(self):
        return self._get_relationship('dependency')
    
    def get_connectsTo_relationship(self):
        return self._get_relationship('database_endpoint')

    def _get_relationship(self, key):
        rv = []
        if 'requirements' in self.nodetemplate:
            rship =self.nodetemplate['requirements']
            if self.has_relationship():
                for r in rship:
                    for name, value in r.iteritems():
                        if name == key:
                            rv.append(value)
        return rv
    
    def has_hostedon_relationship(self):
        return self.get_hostedOn_relationship() is not None
    
    def has_dependson_relationship(self):
        return self.get_dependsOn_relationship() is not None
    
    def has_connectto_relationship(self):
        return self.get_connectsTo_relationship() is not None

    def get_capabilities(self):
        if  self.has_capabilities():
            return self.nodetemplate['capabilities']