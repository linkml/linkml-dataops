import logging
import os
import unittest

from linkml_runtime.loaders import yaml_loader, json_loader
from linkml_runtime.dumpers import yaml_dumper, json_dumper
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml_runtime_api.changer.jsonpatch_changer import JsonPatchChanger
from linkml_runtime_api.changer.changes_model import AddObject, RemoveObject, Append, Rename

from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests import MODEL_DIR, INPUT_DIR
from tests.model.kitchen_sink_api import AddPerson

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')

def _roundtrip(element: YAMLRoot) -> dict:
    typ = type(element)
    jsonstr = json_dumper.dumps(element, inject_type=False)
    return json_loader.loads(jsonstr, target_class=typ)

class JsonPatchMakerTestCase(unittest.TestCase):
    """
    Tests JsonPatchChanger

    this translates a change object into a JSON Patch.

    This patch can then be converted using any JSON-Patch supporting tool,
    including the Python implementation
    """

    def test_make_jsonpatch(self):
        view = SchemaView(SCHEMA)
        patcher = JsonPatchChanger(schemaview=view)
        d = Dataset(persons=[Person('foo', name='foo')])
        new_person = Person(id='P1', name='P1')
        # ADD OBJECT
        obj = AddObject(value=new_person)
        result = patcher.apply(obj, d, in_place=True)
        #d = result.object
        logging.info(d)
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
        obj = Append(value='fred', path='/persons/P1/aliases')
        #person = next(p for p in d.persons if p.id == 'P1')
        #print(person)
        #print(f'ALIASES={person.aliases}')
        #obj = Append(value='fred', parent=person.aliases)
        rs = patcher.apply(obj, d)
        logging.info(yaml_dumper.dumps(d))
        assert next(p for p in d.persons if p.id == 'P1').aliases == ['fred']

    def test_rename(self):
        view = SchemaView(SCHEMA)
        patcher = JsonPatchChanger(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        change = Rename(value='P:999', old_value='P:001', target_class='Person', path='')
        d2 = _roundtrip(dataset)
        logging.info(f'CHANGE = {change}')
        r = patcher.apply(change, dataset)
        dataset = r.object
        logging.info(dataset)
        logging.info(f'RESULTS:')
        logging.info(yaml_dumper.dumps(dataset))
        assert dataset.persons[0].id == 'P:999'
        assert dataset.persons[1].has_familial_relationships[0].related_to == 'P:999'

    def test_generated_api(self):
        view = SchemaView(SCHEMA)
        patcher = JsonPatchChanger(schemaview=view)
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


if __name__ == '__main__':
    unittest.main()
