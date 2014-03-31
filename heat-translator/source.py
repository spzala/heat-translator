from yaml_parser import Parser


class Source(object):
    '''
    Load the source data.
    '''
    def __init__(self, path):
        self.profile = Parser(path).load()

    def __contains__(self, key):
        return key in self.profile

    def __iter__(self):
        return iter(self.profile)

    def __len__(self):
        return len(self.profile)

    def __getitem__(self, key):
        '''Get a section.'''
        return self.profile[key]
