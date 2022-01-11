import os
import unittest
import logging

from linkml_dataops.apiroot import ApiRoot
from linkml_dataops.changer.object_changer import ObjectChanger
from linkml_dataops.changer.changes_model import Rename
from linkml_dataops.diffs.differ import DiffEngine
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Dataset, Person, EmploymentEvent, CompanyId
from tests import MODEL_DIR, INPUT_DIR

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')


class PathTestCase(unittest.TestCase):
    """
    Tests path expressions
    """

    def test_paths(self):
        """
        tests ability to perform lookup using paths
        """
        view = SchemaView(SCHEMA)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        api_root = ApiRoot(schemaview=view)
        p = '/persons'
        obj = api_root.select_path('/persons', dataset)
        assert isinstance(obj, list)
        assert isinstance(obj[0], Person)
        p = '/persons/P:002'
        obj = api_root.select_path('/persons/P:002', dataset)
        assert isinstance(obj, Person)
        assert obj.id == 'P:002'
        obj = api_root.select_path('/persons/P:002/has_employment_history', dataset)
        assert isinstance(obj, list)
        assert isinstance(obj[0], EmploymentEvent)
        obj = api_root.select_path('/persons/P:002/has_employment_history/0/employed_at', dataset)
        assert isinstance(obj, CompanyId)
        obj = api_root.select_path('/persons/1', dataset)
        obj = api_root.select_path('/has_employment_history/0', obj)
        assert isinstance(obj, EmploymentEvent)




if __name__ == '__main__':
    unittest.main()
