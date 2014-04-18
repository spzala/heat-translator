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

from translator.hot import translate_inputs
from translator.tests.base import TestCase


class TestToscaInputTranslation(TestCase):

    def test_translate_constraints(self):
        translator = translate_inputs.TranslateInputs(inputs=None)

        # The tuples in this list each contain a tuple containing the TOSCA
        # constraint name and value along with another tuple containing
        # the corresponding HOT constraint name and value.
        constraint_mappings = \
            [(("equal", 3), ("allowed_values", [3])),
             (("greater_than", 3), ("range", {"min": 4})),
             (("greater_or_equal", 3), ("range", {"min": 3})),
             (("less_than", 3), ("range", {"max": 2})),
             (("less_or_equal", 3), ("range", {"max": 3})),
             # PyYAML parses a set {3, 5} into a dict like below.
             (("in_range", {3: None, 5: None}), ("range",
                                                 {"min": 3, "max": 5})),
             (("valid_values", [1, 2, 3]), ("allowed_values", [1, 2, 3])),
             (("length", 3), ("length", {"min": 3, "max": 3})),
             (("min_length", 3), ("length", {"min": 3})),
             (("max_length", 3), ("length", {"max": 3})),
             (("pattern", "[a-zA-Z]*"), ("allowed_pattern", "[a-zA-Z]*"))]

        for constraint_pair in constraint_mappings:
            tosca_input, hot_output = constraint_pair
            tosca_name, tosca_value = tosca_input
            hot_name, hot_value = hot_output
            hname, hvalue = translator._translate_constraints(tosca_name,
                                                              tosca_value)
            self.assertEqual(hot_name, hname)
            self.assertEqual(hot_value, hvalue)
