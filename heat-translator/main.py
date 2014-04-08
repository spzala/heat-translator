#!/usr/bin/env python
import logging
import os
import sys
from tosca.tosca_tpl import ToscaTpl
#from tosca.validator import ToscaValidator
from test_tpl_graph import TestTPLGraph

'''Entry point into the heat translation.
   Takes two user arguments,
   1. type of translation (e.g. tosca)
   2. Path to the file that needs to be translated.'''

log = logging.getLogger("heat-translator.log")


def main():
    sourcetype = sys.argv[1]
    path = sys.argv[2]
    if not sourcetype:
        raise ValueError("Translation type is needed. For example, 'tosca'")
    if os.path.isdir(path):
        raise ValueError("Translation of a directory is not support "
                         "at this time, %(dir)s" % {'dir': path})
    if not path.endswith(".yaml"):
        raise ValueError("Only YAML file is supported at this time.")
    elif os.path.isfile(path):
        heat_tpl = translate(sourcetype, path)
        if heat_tpl:
            write_output(heat_tpl)
    else:
        raise ValueError(("%(path)s is not a valid file.") % {'path': path})


def translate(sourcetype, path):
    output = None
    if sourcetype == "tosca":
        tosca = ToscaTpl(path)
    return output


def write_output(output):
    pass


if __name__ == '__main__':
    main()
