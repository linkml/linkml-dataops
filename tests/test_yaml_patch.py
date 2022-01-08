import os
import sys
import unittest
import logging
from ruamel.yaml import YAML

from jsonpatch import JsonPatch

from linkml_dataops.diffs.yaml_patch import YAMLPatch

inp = """\
# example
name:
  # details
  family: Smith   # very common
  given: Alice    # one of the siblings
"""

yaml_patch = YAMLPatch()

class YamlPatchTestCase(unittest.TestCase):
    """
    Tests yaml patching
    """

    def test_patch(self):
        """
        test patch works, preserving comments
        """
        patch = JsonPatch([
            {'op': 'add', 'path': '/foo', 'value': {'bar': 'baz'}},
            {'op': 'remove', 'path': '/name/family'}
        ])
        nu = yaml_patch.patchs(inp, patch)
        assert '# example' in nu
        assert '# details' in nu
        assert '# one of the siblings' in nu
        yaml=YAML()
        obj = yaml.load(nu)
        self.assertEqual(obj, {"name": {"given": "Alice"},
                               "foo": {"bar": "baz"}})






if __name__ == '__main__':
    unittest.main()
