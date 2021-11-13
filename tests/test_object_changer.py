import logging
import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime_api.changer.object_changer import ObjectChanger
from linkml_runtime_api.changer.changes_model import AddObject, RemoveObject, Append, Rename
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests.model.kitchen_sink_api import AddPerson
from tests import MODEL_DIR, INPUT_DIR

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

class ObjectChangerTestCase(unittest.TestCase):
    """
    Tests in-memory object changer
    """

    def test_add_remove(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        d = Dataset(persons=[Person('foo')])
        new_person = Person(id='P1')
        # ADD OBJECT
        #obj = AddObject(value=new_person, path='/persons')
        obj = AddObject(value=new_person)
        rs = patcher.apply(obj, d)
        logging.info(yaml_dumper.dumps(d))
        assert new_person.id in [p.id for p in d.persons]
        assert new_person in d.persons

        obj = RemoveObject(value=new_person)
        rs = patcher.apply(obj, d)
        logging.info(yaml_dumper.dumps(d))
        assert new_person.id not in [p.id for p in d.persons]
        assert new_person not in d.persons

        # add back
        patcher.apply(AddObject(value=new_person), d)

        # add to list
        #obj = Append(value='fred', path='/persons/P1/aliases')
        person = next(p for p in d.persons if p.id == 'P1')
        logging.info(person)
        obj = Append(value='fred', parent=person.aliases)
        rs = patcher.apply(obj, d)
        logging.info(yaml_dumper.dumps(d))
        assert next(p for p in d.persons if p.id == 'P1').aliases == ['fred']

    def test_rename(self):
        """
        Tests renaming (providing new identifier)
        """
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        change = Rename(value='P:999', old_value='P:001', target_class='Person')
        patcher.apply(change, dataset)
        logging.info(dataset)
        logging.info(yaml_dumper.dumps(dataset))
        assert dataset.persons[0].id == 'P:999'
        assert dataset.persons[1].has_familial_relationships[0].related_to == 'P:999'

    @unittest.skip
    def test_set_value(self):
        assert True  # TODO: implement this

    def test_append(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = Dataset()
        change = Append(value=Person('P:1234'))
        patcher.apply(change, dataset)
        logging.info(dataset)
        #print(yaml_dumper.dumps(dataset))
        person = dataset.persons[0]
        assert person.id == 'P:1234'
        change = Append(value=FamilialRelationship(related_to='P:4', type='SIBLING_OF'),
                        path='has_familial_relationships')
        patcher.apply(change, person)
        logging.info(dataset)
        #print(yaml_dumper.dumps(dataset))
        assert dataset.persons[0].has_familial_relationships[0].related_to == 'P:4'

    #@unittest.skip
    def test_get_path(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        person = Person('P:1')
        change = Append(value=FamilialRelationship(related_to='P:4', type='SIBLING_OF'))
        patcher._locate_object(change, person)


    def test_generated_api(self):
        view = SchemaView(SCHEMA)
        patcher = ObjectChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        frel = FamilialRelationship(related_to='P:001', type='SIBLING_OF')
        person = Person(id='P:222', name='foo',
                        has_familial_relationships=[frel])
        change = AddPerson(value=person)
        logging.info(change)
        patcher.apply(change, dataset)
        logging.info(dataset)
        logging.info(yaml_dumper.dumps(dataset))
        assert len(dataset.persons) == 3
        assert dataset.persons[2].id == 'P:222'
        assert dataset.persons[2].has_familial_relationships[0].related_to == 'P:001'

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
