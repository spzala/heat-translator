#!/usr/bin/env python

import os
import sys
from source import Source
from translation.translate import TOSCATranslator
from tosca.tosca_profile import Tosca
from tosca.validator import ToscaValidator

'''Entry point into the heat translation.
   Takes two user arguments, 1. type of translation (e.g. tosca) 2. Path to the file that needs to be translated.'''

def main():
    #sourcetype = sys.argv[1]
    #path = sys.argv[2]
    sourcetype = 'tosca'
    path = '/home/openstack/toscacode/heat-translator/heat-translator/tosca/tests/tosca_single_instance_wordpress.yaml'
    if not sourcetype:
        print("Translation type is needed. For example, 'tosca'")
    if not path.endswith(".yaml"):
        print "Only YAML file is supported at this time."
        
    if os.path.isdir(path):
        print('Translation of directory is not supported at this time : %s' % path)
    elif os.path.isfile(path):
        heat_tpl = translate(sourcetype, path)
        if heat_tpl:
            self.write_output(heat_tpl)
    else:
        print('%s is not a valid file.' % path)

def translate(sourcetype, path):
    tpl = Source(path)
    output = None
    if sourcetype == "tosca":
        pass
    return output
        
def write_output(output):
    pass

if __name__ == '__main__':
    main()
