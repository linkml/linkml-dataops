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

class ObjectPatcherTestCase(unittest.TestCase):

    def test_rename(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        change = Rename(value='P:999', old_value='P:001', target_class='Person')
        result = patcher.apply(change, dataset, in_place=False)
        new_dataset = result.object
        assert dataset.persons[0].id == 'P:001'
        assert new_dataset.persons[0].id == 'P:999'
        assert new_dataset.persons[1].has_familial_relationships[0].related_to == 'P:999'
        de = DiffEngine()
        patch = de.diff(dataset, new_dataset)
        for p in patch:
            logging.info(p)
        assert len(list(patch)) > 0





if __name__ == '__main__':
    unittest.main()
