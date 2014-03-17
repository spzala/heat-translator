
SECTIONS = (TYPE, PROPERTIES, REQUIREMENTS, INTERFACES, LIFECYCLE, INPUT) = \
           ('type', 'properties', 'requirements', 'interfaces', 'lifecycle', 'input')
          
REQUIRES = (CONTAINER, DEPENDENCY, DATABASE_ENDPOINT, CONNECTION, HOST) = \
           ('container', 'dependency', 'database_endpoint', 'connection', 'host')
       
INTERFACES_STATE = (CREATE, START, CONFIGURE, START, DELETE) = \
           ('create', 'stop', 'configure', 'start','delete')

TOSCA_TO_HOT_TYPE = {'tosca.basetypes.nodes.Compute': 'OS::Nova::Server'}

TOSCA_TO_HOT_REQUIRES = {'container': 'server', 'host': 'server', 'dependency': 'depends_on', "connects": 'depends_on'}

TOSCA_TO_HOT_PROPERTIES = {'properites': 'input'}

resolved = []
order = []
interested_nodes = []

class TranslateNodeTemplates():
    '''Translate TOSCA Inputs to Heat Parameters'''
    
    def __init__(self, nodetemplates, tosca):
        self.nodetemplates = nodetemplates
        self.tosca = tosca
        #TODO
 