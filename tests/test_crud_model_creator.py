import logging
import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_dataops.creators.crud_model_creator import CRUDModelCreator
from linkml_dataops.changer.changes_model import AddObject, RemoveObject, Append, Rename
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Person, Dataset, FamilialRelationship
from tests.model.kitchen_sink_api import AddPerson
from tests import MODEL_DIR, INPUT_DIR, OUTPUT_DIR

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
API_SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink_api_test.yaml')



class CRUDModelCreatorTestCase(unittest.TestCase):
    """
    Tests :class:`ApiGenerator`
    """

    def test_create_crud(self):
        """
        Tests :class:`ApiGenerator.serialize`
        :return:
        """
        view = SchemaView(SCHEMA)
        gen = CRUDModelCreator(schemaview=view)
        logging.info(gen.serialize())
        with open(API_SCHEMA, 'w') as stream:
            stream.write(gen.serialize())
        api_view = SchemaView(API_SCHEMA)
        for cn, c in api_view.all_classes().items():
            logging.info(f'C={cn}')
        assert 'AddPerson' in api_view.all_classes()


if __name__ == '__main__':
    unittest.main()
