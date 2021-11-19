import logging
import os
import unittest
from typing import List

from linkml_runtime.loaders import yaml_loader
from linkml_runtime_api.query.object_queryengine import ObjectQueryEngine
from linkml_runtime_api.query.queryengine import Database, MatchExpression
from linkml_runtime_api.query.query_model import FetchQuery, MatchConstraint, OrConstraint, FetchById
from linkml_runtime.utils.schemaview import SchemaView
from tests.model.kitchen_sink import Person, Dataset
from tests.model.kitchen_sink_api import PersonQuery, PersonFetchById
from tests.model.kitchen_sink_api_bespoke import KitchenSinkAPI

from tests import MODEL_DIR, INPUT_DIR

SCHEMA = os.path.join(MODEL_DIR, 'kitchen_sink.yaml')
DATA = os.path.join(INPUT_DIR, 'kitchen_sink_inst_01.yaml')

class ObjectQueryEngineTestCase(unittest.TestCase):
    """
    Tests ObjectQueryEngine, all of

    - generic API, generic query objects
    - generic API, bespoke query objects
    - bespoke API
    """

    def test_query(self):
        """
        tests ObjectQueryEngine
        """
        view = SchemaView(SCHEMA)
        qe = ObjectQueryEngine(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(op='=', left='id', right='P:001')])
        logging.info(q)
        results = qe.fetch(q, dataset)
        results: List[Person]
        assert len(results) == 1
        #for r in results:
        #    print(r)
        self.assertEqual(results[0].id, 'P:001')

        # negated queries
        q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(negated=True, op='=', left='id', right='P:001')])
        results = qe.fetch(q, dataset)
        self.assertEqual(results[0].id, 'P:002')

        # path queries
        q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(op='=',
                                                    left='has_medical_history/*/diagnosis/name',
                                                    right='headache')])
        results = qe.fetch(q, dataset)
        self.assertEqual(results[0].id, 'P:002')

        # union queries
        def id_constraint(v):
            return MatchConstraint(op='=', left='id', right=v)
        q = FetchQuery(target_class=Person.class_name,
                       constraints=[OrConstraint(subconstraints=[id_constraint('P:001'),
                                                                 id_constraint('P:002')])])
        results = qe.fetch(q, dataset)
        assert len(results) == 2

        # Like queries
        q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(op='like', left='name', right='joe%')])
        results = qe.fetch(q, dataset)
        assert len(results) == 1

        q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(op='like', left='name', right='joe')])
        results = qe.fetch(q, dataset)
        assert len(results) == 0

        q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(op='like', left='name', right='%')])
        results = qe.fetch(q, dataset)
        assert len(results) == 2

        # by ID
        q = FetchById(id='P:001',
                      target_class=Person.class_name)
        results = qe.fetch(q, dataset)
        assert len(results) == 1
        self.assertEqual(results[0].id, 'P:001')

    def test_query_with_domain_change_objects(self):
        """
        Tests generic ObjectQueryEngine using domain-specific change objects

        """
        view = SchemaView(SCHEMA)
        qe = ObjectQueryEngine(schemaview=view)
        dataset = yaml_loader.load(DATA, target_class=Dataset)


        q = PersonQuery(constraints=[MatchConstraint(op='=', left='id', right='P:001')])
        logging.info(q)
        results = qe.fetch(q, dataset)
        results: List[Person]
        assert len(results) == 1
        #for r in results:
        #    print(r)
        self.assertEqual(results[0].id, 'P:001')

        q = PersonFetchById(id_value='P:001')
        logging.info(q)
        results = qe.fetch(q, dataset)
        results: List[Person]
        assert len(results) == 1
        self.assertEqual(results[0].id, 'P:001')

    def test_bespoke_api(self):
        """
        Tests a bespoke generated domain API

        Generated API  here: tests.model.kitchen_sink_api
        note: if you need to change the datamodel, regenerate using gen-oython-api
        """
        view = SchemaView(SCHEMA)
        qe = ObjectQueryEngine(schemaview=view)
        api = KitchenSinkAPI(query_engine=qe)
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        qe.database = Database(document=dataset)
        person = api.fetch_Person('P:001')
        logging.info(f'PERSON={person}')
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
