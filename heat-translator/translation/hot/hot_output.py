

class HotOutput(object):

    def __init__(self, name, value, description=None):
        self.name = name
        self.value = value
        self.description = description

    def get_dict_output(self):
        return {self.name: {'value': self.value, 'description': self.description}}