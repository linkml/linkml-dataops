import logging
import os
import tempfile
import unittest

from tests import MODEL_DIR, INPUT_DIR
from click.testing import CliRunner
from linkml_dataops.changer.jsonpatch_changer import cli

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
PYMOD = os.path.join(MODEL_DIR, 'kitchen_sink.py')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')
CHANGE_FILE = os.path.join(INPUT_DIR, 'changes_01.yaml')
TMP_FILE = os.path.join(INPUT_DIR, 'TMP.yaml')

xxADD_PERSON = """
path: /persons
value:
  id: P:500
  name: foo bag
  age_in_years: 44
  has_employment_history:
    - employed_at: ROR:1
      started_at_time: 2019-01-01
      is_current: true
"""

ADD_PERSON = """
- type: AddPerson
  path: /persons
  value:
    id: P:500
    name: foo bag
    age_in_years: 44
    has_employment_history:
      - employed_at: ROR:1
        started_at_time: 2019-01-01
        is_current: true
"""


class ApplyCLITestCase(unittest.TestCase):
    def setUp(self) -> None:
        runner = CliRunner(mix_stderr=False)
        self.runner = runner

    def test_main_help(self):
        result = self.runner.invoke(cli, ['--help'])
        out = result.stdout
        err = result.stderr
        self.assertIn('format', out)
        self.assertIn('schema', out)
        self.assertIn('change', out)
        self.assertEqual(0, result.exit_code)

    def test_apply_changefile(self):
        result = self.runner.invoke(cli, ['-S', SCHEMA, '-m', PYMOD,
                                          '-I', CHANGE_FILE,
                                          #'-A', "Person '{id: X, name: Y}'",
                                          DATA])
        out = result.stdout
        err = result.stderr
        print(out)
        print(err)
        self.assertIn('id: P:NEW', out)
        self.assertNotIn('id: 001', out)
        #self.assertIn('schema', out)
        #self.assertIn('change', out)
        self.assertEqual(0, result.exit_code)

    def test_apply(self):
        with open(TMP_FILE, 'w') as tmp:
            tmp.write(ADD_PERSON)
            tmp.close()
            result = self.runner.invoke(cli, ['-S', SCHEMA, '-m', PYMOD,
                                              '-I', TMP_FILE,
                                              #'-A', "Person '{id: X, name: Y}'",
                                              DATA])
            out = result.stdout
            err = result.stderr
            print(out)
            print(err)
            self.assertIn('P:500', out)
            self.assertIn('foo bag', out)
            #self.assertIn('format', out)
            #self.assertIn('schema', out)
            #self.assertIn('change', out)
            self.assertEqual(0, result.exit_code)



if __name__ == '__main__':
    unittest.main()
