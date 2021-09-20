import logging
import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime_api.generators.apigenerator import ApiGenerator
from linkml_runtime_api.changer.changes_model import AddObject, RemoveObject, Append, Rename
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests.model.kitchen_sink_api import AddPerson
from tests import MODEL_DIR, INPUT_DIR

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
API_SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink_api_test.yaml')



class ApiGeneratorTestCase(unittest.TestCase):
    """
    Tests :class:`ApiGenerator`
    """

    def test_apigen(self):
        """
        Tests :class:`ApiGenerator.serialize`
        :return:
        """
        view = SchemaView(SCHEMA)
        gen = ApiGenerator(schemaview=view)
        logging.info(gen.serialize())
        with open(API_SCHEMA, 'w') as stream:
            stream.write(gen.serialize())
        api_view = SchemaView(API_SCHEMA)
        for cn, c in api_view.all_class().items():
            logging.info(f'C={cn}')
        assert 'AddPerson' in api_view.all_class()


if __name__ == '__main__':
    unittest.main()
