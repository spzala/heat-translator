===============================
heat-translator
===============================

Tool to translate non-heat templates to Heat Orchestration Template (HOT)

* Free software: Apache license

Features
--------

The heat-translator tool is currently divided into two parts - TOSCA 
library and translator to HOT. 
TOSCA library is developed to create a TOSCA memory model from TOSCA type definition and TOSCA template.
The translator is primarly developed to have a memory model (i.e. TOSCA for now but it's designed in such a way that it can easily be extended to support any format in futrue) as an input and produce HOT as an output.

Running heat-translator
-----------------------
Currently, while the project is still in development, use the following command from the project root to run the translator:

    ``python -m translator.main <source-type> <path-to-file>``

The only supported source-type right now is 'tosca'.

Note that you must have PyYAML installed:

    ``sudo pip install pyyaml``