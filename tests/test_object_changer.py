import logging
import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_dataops.changer.object_changer import ObjectChanger
from linkml_dataops.changer.changes_model import AddObject, RemoveObject, Append, Rename
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests.model.kitchen_sink_api import AddPerson
from tests import MODEL_DIR, INPUT_DIR
from tests.test_changer_common import ChangerCommonTests

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')

ADD_PERSON = """
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

class ObjectChangerTestCase(unittest.TestCase, ChangerCommonTests):
    """
    Tests in-memory object changer
    """

    def setUp(self):
        view = SchemaView(SCHEMA)
        self.patcher = ObjectChanger(schemaview=view)


    def test_add(self):
        self._test_add()

    @unittest.skip
    def test_set_value(self):
        assert True  # TODO: implement this


    def test_remove_by_identifier(self):
        """test removal of object by primary key"""
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        n_persons = len(dataset.persons)
        dataset: Dataset
        change = RemoveObject(value=Person(id='P:002'))
        r = patcher.apply(change, dataset)
        print(yaml_dumper.dumps(dataset))
        self.assertEqual(len(dataset.persons), n_persons-1)
        self.assertEqual(dataset.persons[0].id, 'P:001')

    def test_duplicate_primary_key(self):
        """
        currently duplicates are allowed
        """
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = Dataset()
        patcher.apply(AddObject(value=Person(id='P1', name='p1')), dataset)
        patcher.apply(AddObject(value=Person(id='P1', name='p2')), dataset)
        assert dataset.persons[0].id == 'P1'
        self.assertEqual(len(dataset.persons), 2)
        print(dataset.persons[0])
        print(dataset.persons[1])
        patcher.apply(RemoveObject(value=Person(id='P1')), dataset)
        self.assertEqual(len(dataset.persons), 1)


    def test_get_path(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        person = Person('P:1')
        app = Append(value=FamilialRelationship(related_to='P:4', type='SIBLING_OF'))
        path = patcher._get_path(app, person)
        #print(f'PATH={path}')
        self.assertEqual(path, '/has_familial_relationships')
        loc = patcher._locate_object(app, person)
        #print(f'LOC={loc}')
        self.assertEqual(loc, [])
        dataset = Dataset()
        patcher.apply(AddObject(value=person), dataset)
        # TODO: paths of length > 1
        #path = patcher._get_path(app, dataset)



    @unittest.skip
    def test_from_json(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        change = yaml_loader.loads(ADD_PERSON, target_class=AddObject)
        logging.info(change)
        patcher.apply(change, dataset)
        logging.info(dataset)
        logger.info(yaml_dumper.dumps(dataset))
        assert len(dataset.persons) == 3
        #assert dataset.persons[0].id == 'P:999'
        #assert dataset.persons[1].has_familial_relationships[0].related_to == 'P:999'





if __name__ == '__main__':
    unittest.main()
