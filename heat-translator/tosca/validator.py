from tosca.inputs import Input
##from tosca.elements.nodetemplate import NodeTemplate

class ToscaValidator():
    ''' Validates inputs and node templates.'''
    def __init__(self, Tosca):
        self.inputs = Tosca.inputs
        self.nodetemplates = Tosca.nodetemplates
        self.tosca = Tosca
        
    def validate(self):
        #validate inputs
        for input in self.inputs:
            if not isinstance(input.schema, dict):
                print ("The input %s has no attributes", name)
            input.validate() 

        #validate node templates
        for ntpl in self.nodetemplates:
            ntpl.validate()
    