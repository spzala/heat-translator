from capabilitytype import CapabilityType
from properties import Property
from properties import Properties
from relationshiptype import RelatonshipType
from nodetype import NodeType
from node_templates import NodeTemplates
from schema import Schema
from tosca.inputs import InputParameters
from tosca.inputs import Input

class NodeTemplate(object):
    ''' Node template from a Tosca profile.'''
    def __init__(self, name, nodetemplate, tosca):
        self.name = name
        self.nodetemplate = nodetemplate
        self.tosca = tosca
        self.nodetype = NodeType(self.get_type())
        self.nodetype_properties = Properties(self.nodetype.get_properties())
        self.schema = Schema(self.get_type())
        if 'derived_from' in self.nodetemplate:
            self.parentNode = NodeType(self.nodetemplate['derived_from'])
        elif self.nodetype.has_parent():
                self.parentNode = NodeType(self.nodetype.parentNode)
        if self.has_hostedon_relationship():
            self.hosted_on = RelatonshipType(self.get_type())
        if self.has_dependson_relationship():
            self.depends_on = RelatonshipType(self.get_type())
        if self.has_connectto_relationship():
            self.connects_to = RelatonshipType(self.get_type())
        if self.has_capabilities():
            self.nodetype_capabilities = CapabilityType(self.get_type())
        
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.nodetemplate['type']
    
    def get_properties(self):
        if 'properties' in self.nodetemplate:
            return self.nodetemplate['properties']
    
    def get_parent_properties(self, node=None):
        properties = {}
        if node is None:
            node = self.parentNode
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
        required_props = self.schema.required()
        for req in required_props:
            if self.get_properties():
                if req not in self.get_properties():
                    raise ValueError('Missing required property %s' %req)
        if self.get_properties():
            for prop, val in self.get_properties().iteritems():
                if isinstance(val, dict):
                    for key, value in val.iteritems():           
                        if key == "get_input":
                            val = self.get_input_ref(value)
                            break
                        if key == "get_property":
                            val = self.get_property_ref(value, self.tosca)
                if val is not None:
                    Property(prop, self.get_type(), val).validate()
            
    def get_input_ref(self, ref):
        ''' get input reference, for example, get_input: db_user '''
        input_val = self.tosca.get_inputs()[ref]
        if Input(ref, input_val).has_default():
            return Input(ref, input_val).get_default()
    
    @classmethod
    def get_property_ref(cls, ref, t):
        ''' get property reference, for example, get_property: [ mysql, db_user ] '''
        item = ref[0]
        n = t.get_nodetemplates()[item]
        c = cls(item, n, t)
        for val in c.get_properties().itervalues():
            if isinstance(val, dict):
                for key, value in val.iteritems():           
                    if key == "get_input":
                        return c.get_input_ref(value)
    
    def has_relationship(self):
        return 'requirements' in self.nodetemplate
    
    def has_capabilities(self):
        return 'capabilities' in self.nodetemplate
    
    def get_relationship(self):
        if  self.has_relationship():
            return self.nodetemplate['requirements']
    
    def get_hostedOn_relationship(self):
        host = None
        hosted_on = self._get_key('host')
        if hosted_on:
            for r in  self._get_key('host'):
                host = r
        return host
    
    def get_dependsOn_relationship(self):
        return self._get_key('dependency')
    
    def get_connectsTo_relationship(self):
        return self._get_key('database_endpoint')

    def _get_key(self, key):
        rv = []
        if self.has_relationship():
            for r in self.get_relationship():
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