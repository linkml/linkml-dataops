import json
import logging
import os
import unittest

import yaml
from linkml_runtime.loaders import yaml_loader, json_loader
from linkml_runtime.dumpers import yaml_dumper, json_dumper
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml_dataops.changer.jsonpatch_changer import JsonPatchChanger
from linkml_dataops.changer.changes_model import AddObject, RemoveObject, Append, Rename
from linkml_dataops.changer.obj_utils import dicts_to_changes

from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests import MODEL_DIR, INPUT_DIR, OUTPUT_DIR
from tests.model.kitchen_sink_api import AddPerson
import tests.model.kitchen_sink_api
from tests.common_tests import ChangerCommonTests

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')
DATA_AS_JSON = os.path.join(OUTPUT_DIR, 'kitchen_sink_inst_01.json')
OUT = os.path.join(OUTPUT_DIR, 'kitchen_sink_inst_01.patched.yaml')

def _roundtrip(element: YAMLRoot) -> dict:
    typ = type(element)
    jsonstr = json_dumper.dumps(element, inject_type=False)
    return json_loader.loads(jsonstr, target_class=typ)

class JsonPatchMakerCommonTests(unittest.TestCase):
    """
    Tests JsonPatchChanger

    this translates a change object into a JSON Patch.

    This patch can then be converted using any JSON-Patch supporting tool,
    including the Python implementation

    .. note::

       this test also runs all tests in :ref:`ChangerCommonTests`
    """

    def setUp(self):
        view = SchemaView(SCHEMA)
        self.patcher = JsonPatchChanger(schemaview=view)
        self.common = ChangerCommonTests(patcher=self.patcher, parent=self)

    def test_add(self):
        self.common.add_top_level_test()

    def test_remove(self):
        self.common.remove_object_test()
        #TODO
        #self.common.remove_atomic_value()

    @unittest.skip('TODO')
    def test_add_remove(self):
        self.common.add_then_remove_test()

    @unittest.skip('TODO')
    def test_append_value(self):
        self.common.append_scalar_value_test()

    def test_append_object(self):
        self.common.append_object_test()

    def test_rename(self):
        self.common.rename_test()

    def test_from_empty(self):
        self.common.add_from_empty_test()

    def test_domain_api(self):
        self.common.domain_api_test()

    def test_changes_file(self):
        self.common.change_file_test()

    def test_get_json_path(self):
        """
        tests conversion of paths to jsonpath syntax

        See also :ref:`test_paths`
        """
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        patcher = self.patcher
        path = patcher._path_to_jsonpath('/persons', dataset)
        assert path == '/persons'
        path = patcher._path_to_jsonpath('/persons/P:002', dataset)
        assert path == '/persons/1'
        path = patcher._path_to_jsonpath('/persons/P:002/has_employment_history', dataset)
        #print(path)
        assert path == '/persons/1/has_employment_history'
        path = patcher._path_to_jsonpath('/persons/P:002/has_employment_history/0', dataset)
        #print(path)
        assert path == '/persons/1/has_employment_history/0'

    def test_make_jsonpatch(self):
        patcher = self.patcher
        d = Dataset(persons=[Person('foo', name='foo')])
        new_person = Person(id='P1', name='P1')
        # ADD OBJECT
        ch = AddObject(value=new_person)
        p = patcher.make_patch(ch, d)
        logging.info(f'P={p}')
        result = patcher.apply(ch, d, in_place=True)
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


    def test_patch_yaml_file(self):
        view = SchemaView(SCHEMA)
        patcher = JsonPatchChanger(schemaview=view)
        #change = Rename(value='P:999', old_value='P:001', target_class='Person', path='')
        change = AddObject(value=Person(id='P1', name='P1'))
        patcher.patch_file(DATA, [change], out_stream=OUT, target_class=Dataset)

    def test_patch_json_file(self):
        view = SchemaView(SCHEMA)
        patcher = JsonPatchChanger(schemaview=view)
        with open(DATA) as stream:
            obj = yaml.safe_load(stream)
        with open(DATA_AS_JSON, 'w') as stream:
            json.dump(obj, stream, indent=4, sort_keys=True, default=str)
        change = AddObject(value=Person(id='P1', name='P1'))
        patcher.patch_file(DATA_AS_JSON, [change], out_stream=OUT, target_class=Dataset)


    def test_from_dict(self):
        changes = dicts_to_changes([{'type': 'AddPerson', 'value': {'id': 'P1', 'name': 'P1'}}],
                                   tests.model.kitchen_sink_api)
        print(changes)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        patcher = self.patcher
        patcher.apply_multiple(changes, dataset)
        assert any(p.name == 'P1' for p in dataset.persons if p.id == 'P1')

    @unittest.skip("todo")
    def test_append_with_path(self):
        """
        test appending an object to a list
        """
        patcher = self.patcher
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        change = Append(value=FamilialRelationship(related_to='P:4', type='SIBLING_OF'))
        change.path = 'persons/P:001/has_familial_relationships/'
        patcher.apply(change, dataset)
        logging.info(dataset)
        #print(yaml_dumper.dumps(dataset))
        #assert dataset.persons[0].has_familial_relationships[0].related_to == 'P:4'

    def test_schema_changes(self):
        patcher = self.patcher


if __name__ == '__main__':
    unittest.main()
