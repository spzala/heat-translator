# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from translator.toscalib.elements.statefulentitytype import StatefulEntityType

SECTIONS = (LIFECYCLE, CONFIGURE) = \
           ('tosca.interfaces.node.Lifecycle',
            'tosca.interfaces.relationship.Configure')


class InterfacesTypeDef(StatefulEntityType):
    '''Tosca built-in interfaces type'''
    def __init__(self, ntype, interfacetype,
                 tpl_name=None, name=None, value=None):
        if ntype:
            self.defs = self.TOSCA_DEF[interfacetype]
        self.nodetype = ntype
        self.tpl_name = tpl_name
        self.type = interfacetype
        self.name = name
        self.value = value
        self.implementation = None
        self.input = None
        if value:
            if isinstance(self.value, dict):
                for i, j in self.value.iteritems():
                    if i == 'implementation':
                        self.implementation = j
                    if i == 'input':
                        self.input = j
            else:
                self.implementation = value

    @property
    def lifecycle_ops(self):
        if self.defs:
            if self.type == LIFECYCLE:
                ops = []
                for name, value in self.defs.iteritems():
                    ops.append(name)
                return ops

    @property
    def configure_ops(self):
        if self.defs:
            if self.type == CONFIGURE:
                ops = []
                for name, value in self.defs.iteritems():
                    ops.append(name)
                return ops
