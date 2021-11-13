import os
import unittest
import logging

from linkml_runtime_api.changer.object_changer import ObjectChanger
from linkml_runtime_api.changer.changes_model import Rename
from linkml_runtime_api.diffs.differ import DiffEngine
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Dataset
from tests import MODEL_DIR, INPUT_DIR

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')

class DifferTestCase(unittest.TestCase):
    """
    Note: this test largely subsumed by test_object_changer
    """

    def test_rename(self):
        """
        test renaming objects

        note: here 'name' refers to identifier
        """
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        # rewire existing object from P:001 to P:999 and test changes cascade
        change = Rename(value='P:999', old_value='P:001', target_class='Person')
        result = patcher.apply(change, dataset, in_place=False)
        new_dataset = result.object
        assert dataset.persons[0].id == 'P:001'
        assert new_dataset.persons[0].id == 'P:999'
        # test changes cascade to references
        assert new_dataset.persons[1].has_familial_relationships[0].related_to == 'P:999'
        # person diff
        de = DiffEngine()
        patch = de.diff(dataset, new_dataset)
        for p in patch:
            logging.info(p)
        assert len(list(patch)) > 0





if __name__ == '__main__':
    unittest.main()
