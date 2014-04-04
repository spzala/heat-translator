#!/usr/bin/env python

import os
import sys
from tosca.tosca_tpl import ToscaTpl
#from tosca.validator import ToscaValidator
from test_tpl_graph import TestTPLGraph

'''Entry point into the heat translation.
   Takes two user arguments,
   1. type of translation (e.g. tosca)
   2. Path to the file that needs to be translated.'''


def main():
    sourcetype = sys.argv[1]
    path = sys.argv[2]
    if not sourcetype:
        print("Translation type is needed. For example, 'tosca'")
    if not path.endswith(".yaml"):
        print "Only YAML file is supported at this time."
    if os.path.isdir(path):
        print('Translation of directory is not supported'
              'at this time : %s' % path)
    elif os.path.isfile(path):
        heat_tpl = translate(sourcetype, path)
        if heat_tpl:
            write_output(heat_tpl)
    else:
        print('%s is not a valid file.' % path)


def translate(sourcetype, path):
    output = None
    if sourcetype == "tosca":
        tosca = ToscaTpl(path)
        TestTPLGraph(tosca).test()
    return output


def write_output(output):
    pass


if __name__ == '__main__':
    main()
