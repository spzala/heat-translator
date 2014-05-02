#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os
import sys

from translator.hot.translate import TOSCATranslator
from translator.toscalib.tosca_tpl import ToscaTpl
from translator.test_tpl_graph import TestTPLGraph

'''Entry point into the heat translation.
   Takes two user arguments,
   1. type of translation (e.g. tosca)
   2. Path to the file that needs to be translated.'''

log = logging.getLogger("heat-translator.log")



def main():
    sourcetype = sys.argv[1]
    path = sys.argv[2]
    parsed_params = {}
    
    if len(sys.argv)>3:
        parsed_params = parse_parameters(sys.argv[3])    
    if not sourcetype:
        raise ValueError("Translation type is needed. For example, 'tosca'")
    if os.path.isdir(path):
        raise ValueError("Translation of a directory is not support "
                         "at this time, %(dir)s" % {'dir': path})
    if not path.endswith(".yaml"):
        raise ValueError("Only YAML file is supported at this time.")
    elif os.path.isfile(path):
        heat_tpl = translate(sourcetype, path, parsed_params)
        if heat_tpl:
            write_output(heat_tpl)
    else:
        raise ValueError(("%(path)s is not a valid file.") % {'path': path})
    
    
def parse_parameters(parameter_list):
    parsed_inputs = {}
    if parameter_list.startswith('--parameters'):
        inputs = parameter_list.split('--parameters=')[1].replace('"','').split(';')   # todo:  add more error handling for the expected format
        for param in inputs:
            keyvalue = param.split('=')
            parsed_inputs[keyvalue[0]] = keyvalue[1]
    else:
        raise ValueError("%(param) is not a valid parameter" % parameter_list)
    return parsed_inputs

def translate(sourcetype, path, parsed_params):
    output = None
    if sourcetype == "tosca":
        tosca = ToscaTpl(path)
        #TestTPLGraph(tosca).show_properties()
        translator = TOSCATranslator(tosca, parsed_params)
        output = translator.translate()
    return output


def write_output(output):
    print(output)


if __name__ == '__main__':
    main()
