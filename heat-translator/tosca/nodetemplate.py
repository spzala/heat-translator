import logging
from tosca.elements.nodetype import NodeType
from tosca.elements.capabilitytype import CapabilityTypeDef
from tosca.elements.interfacestype import InterfacesTypeDef
from tosca.elements.properties import PropertyDef

SECTIONS = (DERIVED_FROM, PROPERTIES, REQUIREMENTS,
            INTERFACES, CAPABILITIES) = \
           ('derived_from', 'properties', 'requirements', 'interfaces',
            'capabilities')

log = logging.getLogger('tosca')

# hardcode here for type server for now, to be reorganized later in type specific node
FLAVORS = {'m1.xlarge':{'mem_size': 16384, 'disk_size': 160, 'num_cpus': 8},
           'm1.large': {'mem_size': 8192, 'disk_size': 80, 'num_cpus': 4},
           'm1.medium': {'mem_size': 4096, 'disk_size': 40, 'num_cpus': 2},    
           'm1.small': {'mem_size': 2048, 'disk_size': 20, 'num_cpus': 1},   
           'm1.tiny': {'mem_size': 512, 'disk_size': 1, 'num_cpus': 1},  
           'm1.micro': {'mem_size': 128, 'disk_size': 0, 'num_cpus': 1},   
           'm1.nano': {'mem_size': 64, 'disk_size': 0, 'num_cpus': 1}}

IMAGES = {'F18-x86_64-cfntools':  {'os_arch': 'x86_64', 'os_type': 'Linux ', 'os_distribution': 'Fedora ', 'os_version': '18'},
          'Fedora-x86_64-20-20131211.1-sda':  {'os_arch': 'x86_64', 'os_type': 'Linux ', 'os_distribution': 'Fedora ', 'os_version': '20'},
          'cirros-0.3.1-x86_64-uec': {'os_arch': 'x86_64', 'os_type': 'Linux', 'os_distribution': 'CirrOS', 'os_version': '0.3.1'},
          'fedora-amd64-heat-config': {'os_arch': 'x86_64', 'os_type': 'Linux', 'os_distribution': 'Fedora', 'os_version': '18'}}

class NodeTemplate(NodeType):
    ''' Node template from a Tosca profile.'''
    def __init__(self, name, nodetemplates):
        super(NodeTemplate, self).__init__(nodetemplates[name]['type'])
        self.name = name
        self.nodetemplates = nodetemplates
        self.nodetemplate = nodetemplates[self.name]
        self.type = self.nodetemplate['type']
        self.type_properties = self.properties
        self.type_capabilities = self.capabilities
        self.type_lifecycle_ops = self.lifecycle_operations
        self.type_relationship = self.relationship
        self.related = {}
        self.actual_properties = nodetemplates[name]['properties']

    @property
    def value(self):
        return self.nodetemplate

    @property
    def tpl_requirements(self):
        return self._get_value(REQUIREMENTS, self.nodetemplate)

    @property
    def tpl_relationship(self):
        tpl_relation = {}
        requirs = self.tpl_requirements
        if requirs:
            for r in requirs:
                for x, y in r.iteritems():
                    for i, j in self.type_relationship.iteritems():
                        if x == i.keyword:
                            rtpl = NodeTemplate(y, self.nodetemplates)
                            tpl_relation[i] = rtpl
        return tpl_relation

    @property
    def tpl_capabilities(self):
        '''returns a list of capability objects '''
        tpl_cap = []
        prop_name = None
        prop_val = None
        cap_type = None
        caps = self._get_value(CAPABILITIES, self.nodetemplate)
        if caps:
            for name, value in caps.iteritems():
                for prop, val in value.iteritems():
                    for p, v in val.iteritems():
                        prop_name = p
                        prop_val = v
                for c in self.type_capabilities:
                    if c.name == name:
                        cap_type = c.type
                cap = CapabilityTypeDef(name, cap_type,
                                        self.name, prop_name, prop_val)
                tpl_cap.append(cap)
        return tpl_cap

    @property
    def tpl_interfaces(self):
        tpl_ifaces = []
        ifaces = self._get_value(INTERFACES, self.nodetemplate)
        if ifaces:
            for i in ifaces:
                for name, value in ifaces.iteritems():
                    for ops, val in value.iteritems():
                        iface = InterfacesTypeDef(None, name, self.name,
                                                  ops, val)
                        tpl_ifaces.append(iface)
        return tpl_ifaces

    @property
    def tpl_properties(self):
        tpl_props = []
        properties = self._get_value(PROPERTIES, self.nodetemplate)
        requiredprop = []
        for p in self.type_properties:
            if p.required:
                requiredprop.append(p.name)
        if properties:
            #make sure it's not missing any property required by a node type
            missingprop = []
            for r in requiredprop:
                if r not in properties.keys():
                    missingprop.append(r)
            if missingprop:
                raise ValueError(("Node template %(tpl)s is missing "
                                  "one or more required properties %(prop)s")
                                 % {'tpl': self.name, 'prop': missingprop})
            for name, value in properties.iteritems():
                prop = PropertyDef(name, self.type, value, self.name)
                tpl_props.append(prop)
        else:
            if requiredprop:
                raise ValueError(("Node template %(tpl)s is missing"
                                  "one or more required properties %(prop)s")
                                 % {'tpl': self.name, 'prop': requiredprop})
        return tpl_props

    def _add_next(self, nodetpl, relationship):
        self.related[nodetpl] = relationship

    @property
    def relatednodes(self):
        return self.related.keys()

    def tpl_relation(self, nodetpl):
        if nodetpl in self.related:
            return self.related[nodetpl]

    def ref_property(self, cap, cap_name, property):
        requirs = self.tpl_requirements
        tpl_name = None
        if requirs:
            for r in requirs:
                for i, j in r.iteritems():
                    if i == cap:
                        tpl_name = j
                        break
            if tpl_name:
                tpl = NodeTemplate(tpl_name, self.nodetemplates)
                caps = tpl.tpl_capabilities
                for c in caps:
                    if c.name == cap_name:
                        if c.property == property:
                            return c.property_value

    def validate(self):
        for prop in self.tpl_properties:
            prop.validate()

    # hardcode here for now for type server , to be reorganized later in type specific node
    def translate_HOT_properties(self):
        hot_properties = {}
        if self.type=='tosca.nodes.Compute':
            cpu = self.actual_properties['num_cpus']
            disk = self.actual_properties['disk_size']
            mem = self.actual_properties['mem_size']
            flavor = self._bestflavor(cpu,disk,mem)
            hot_properties['flavor'] = flavor
            os_arch = self.actual_properties['os_arch']
            os_type = self.actual_properties['os_type'] 
            os_distribution = self.actual_properties['os_distribution'] 
            os_version = self.actual_properties['os_version']
            image = self._bestimage(os_arch, os_type, os_distribution, os_version)
            hot_properties['image'] = image
    
        return hot_properties
        
        
    def _bestflavor(self,cpu,disk,mem):
        match_all = FLAVORS.keys()                             # start with all flavors
        match_cpu = self._match(match_all, FLAVORS, 'num_cpus', cpu)     # flavors that fit the CPU count
        match_cpu_mem = self._match(match_cpu, FLAVORS, 'mem_size', mem)             # flavors that fit the mem size
        match_cpu_mem_disk = self._match(match_cpu_mem, FLAVORS, 'disk_size', disk)                # flavors that fit the disk size
        # for now just pick the first flavor, later try to pick one with the least resource
        #print 'Found %s matches' % len(match_cpu_mem_disk)
        if len(match_cpu_mem_disk):
            return match_cpu_mem_disk[0]

        
    def _bestimage(self,os_arch, os_type, os_distribution, os_version):     
        match_all = IMAGES.keys()
        match_arch = self._match(match_all, IMAGES, 'os_arch', os_arch)
        match_type = self._match(match_arch, IMAGES, 'os_type', os_type)
        match_distribution = self._match(match_type, IMAGES, 'os_distribution', os_distribution)
        match_version = self._match(match_distribution, IMAGES, 'os_version', os_version)
        #print 'Found %s matches' % len(match_version)
        if len(match_version):
            return match_version[0]


    def _match(self, this_list, this_dict, attr, size):
        matching_flavors=[]
        for flavor in this_list:
            if this_dict[flavor][attr] >= size:
                matching_flavors.append(flavor)
        return matching_flavors
