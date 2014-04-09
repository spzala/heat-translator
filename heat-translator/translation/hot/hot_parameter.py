
KEYS = (TYPE, DESCRIPTION, DEFAULT, CONSTRAINTS, HIDDEN, LABEL) = \
       ('type', 'description', 'default', 'constraints','hidden', 'label')

class HotParameter(object):

    def __init__(self, name, type, label=None, description=None, default=None, 
                 hidden=None, constraints=None):
        self.name = name
        self.type = type
        self.label = label
        self.description = description
        self.default = default
        self.hidden = hidden
        self.constraints = constraints
    
    def get_dict_output(self):
        param_sections = {TYPE: self.type}
        if self.label:
            param_sections[LABEL] = self.label
        if self.description:
            param_sections[DESCRIPTION] = self.description
        if self.default:
            param_sections[DEFAULT] = self.default
        if self.hidden:
            param_sections[HIDDEN] = self.hidden
        if self.constraints:
            param_sections[CONSTRAINTS] = self.constraints

        return { self.name: param_sections }

   