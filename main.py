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
        #translator = TOSCATranslator(tosca)
        #output = translator.translate()
    return output


def write_output(output):
    print(output)


if __name__ == '__main__':
    main()
