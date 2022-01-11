import logging
import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.compile_python import compile_python

from linkml_dataops import ObjectQueryEngine
from linkml_dataops.creators import PythonDomainApiCreator
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView

from linkml_dataops.query.queryengine import Database, MatchExpression
from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests import MODEL_DIR, INPUT_DIR, OUTPUT_DIR

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
API_CODE = os.path.join(OUTPUT_DIR, 'kitchen_sink_api_generated_test.py')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')



class PythonApiGeneratorTestCase(unittest.TestCase):

    def test_pyapigen(self):
        view = SchemaView(SCHEMA)
        gen = PythonDomainApiCreator(schemaview=view)
        code = gen.serialize(python_path='tests.model')
        with open(API_CODE, 'w') as stream:
            stream.write(code)
        mod = compile_python(code)

        view = SchemaView(SCHEMA)
        qe = ObjectQueryEngine(schemaview=view)
        api = mod.KitchenSinkAPI(query_engine=qe)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        qe.database = Database(data=dataset)
        person = api.fetch_Person('P:001')
        #print(f'PERSON={person}')
        self.assertEqual(person.id, 'P:001')

        results = api.query_Person(name='fred bloggs')
        self.assertEqual(len(results), 1)
        person = results[0]
        self.assertEqual(person.id, 'P:001')

        results = api.query_Person(name=MatchExpression('like', 'fred%'))
        self.assertEqual(len(results), 1)
        person = results[0]
        self.assertEqual(person.id, 'P:001')


if __name__ == '__main__':
    unittest.main()
