import logging
import os
import unittest
from copy import copy
from dataclasses import dataclass

from linkml_runtime.dumpers import yaml_dumper

from linkml_dataops.changer.changer import Changer
from linkml_dataops.changer.object_changer import ObjectChanger
from linkml_dataops.changer.changes_model import AddObject, RemoveObject, Append, Rename, SetValue
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

@dataclass
class ChangerCommonTests:
    """
    Abstract parent class for changer tests

    See: https://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class
    """
    patcher: Changer = None
    parent: unittest.TestCase = None

    def _test_all(self):
        self.add_top_level_test()

    def add_top_level_test(self):
        """Adds a top level element"""
        patcher = self.patcher
        d = Dataset(persons=[Person('foo', name='foo')])
        new_person = Person(id='P1', name='P1')
        # ADD OBJECT
        obj = AddObject(value=new_person)
        rs = patcher.apply(obj, d)
        logging.info(yaml_dumper.dumps(d))
        assert new_person.id in [p.id for p in d.persons]
        assert new_person in d.persons
        # Redo, with explicit path
        d = Dataset(persons=[Person('foo', name='foo')])
        new_person = Person(id='P1', name='P1')
        obj = AddObject(value=new_person, path='/persons')
        rs = patcher.apply(obj, d)
        logging.info(yaml_dumper.dumps(d))
        assert new_person.id in [p.id for p in d.persons]
        assert new_person in d.persons

    def add_atomic_value_test(self):
        person = Person(id='P1')
        change = AddObject(path='name', value='foo')
        r = self.patcher.apply(change, person)
        assert person.name == 'foo'
        change = SetValue(path='name', value='bar')
        r = self.patcher.apply(change, person)
        assert person.name == 'bar'
        change = SetValue(path='name', value=None)
        r = self.patcher.apply(change, person)
        assert not person.name

    def remove_object_test(self):
        """Removes a top level element"""
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        n_persons = len(dataset.persons)
        change = RemoveObject(value=Person(id='P:002'))
        r = self.patcher.apply(change, dataset)
        #print(yaml_dumper.dumps(dataset))
        self.parent.assertEqual(len(dataset.persons), n_persons-1)
        self.parent.assertEqual(dataset.persons[0].id, 'P:001')

    def remove_atomic_value(self):
        person = Person(id='P1', name='remove me')
        change = RemoveObject(path='name', value=person.name)
        r = self.patcher.apply(change, person)
        assert not person.name


    def add_then_remove_test(self):
        patcher = self.patcher
        d = Dataset(persons=[Person('foo', name='foo')])
        new_person = Person(id='P1', name='foo')
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

    def append_scalar_value_test(self):
        """
        tests appending a scalar value onto a multi-valued object
        """
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        person = dataset.persons[0]
        curr_aliases = copy(person.aliases)
        obj = Append(value='fred', parent=person.aliases)
        self.patcher.apply(obj, person)
        obj = Append(value='freddy', parent=person.aliases)
        self.patcher.apply(obj, person)
        assert len(person.aliases) == len(curr_aliases) + 2


    def append_object_test(self):
        """
        test appending an object to a list
        """
        patcher = self.patcher
        dataset = Dataset()
        change = Append(value=Person('P:1234', name='p1234'))
        patcher.apply(change, dataset)
        logging.info(dataset)
        #print(yaml_dumper.dumps(dataset))
        person = dataset.persons[0]
        assert person.id == 'P:1234'
        change = Append(value=FamilialRelationship(related_to='P:4', type='SIBLING_OF'))
        patcher.apply(change, person)
        logging.info(dataset)
        #print(yaml_dumper.dumps(dataset))
        assert dataset.persons[0].has_familial_relationships[0].related_to == 'P:4'
        # Redo, with parent
        dataset = Dataset()
        change = Append(value=Person('P:1234', name='p1234'), parent=dataset)
        #patcher.apply(change)


    def rename_test(self):
        """
        Tests renaming a top level element (providing new identifier)
        """
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        # TODO: fails unless path provieded
        #change = Rename(value='P:999', old_value='P:001', target_class='Person')
        change = Rename(value='P:999', old_value='P:001', target_class='Person', path='')
        self.patcher.apply(change, dataset)
        logging.info(dataset)
        logging.info(yaml_dumper.dumps(dataset))
        assert dataset.persons[0].id == 'P:999'
        assert dataset.persons[1].has_familial_relationships[0].related_to == 'P:999'

    def add_from_empty_test(self):
        """tests that apply method works from an empty container"""
        dataset = Dataset()
        self.patcher.apply(AddObject(value=Person('P1', 'p1')), dataset)
        assert dataset.persons[0].name == 'p1'

    def domain_api_test(self):
        """tests a domain-specific API created using domain specific ops model maker"""
        patcher = self.patcher
        dataset = yaml_loader.load(DATA, target_class=Dataset)
        dataset: Dataset
        n_persons = len(dataset.persons)
        frel = FamilialRelationship(related_to='P:001', type='SIBLING_OF')
        person = Person(id='P:222', name='foo',
                        has_familial_relationships=[frel])
        change = AddPerson(value=person)
        logging.info(change)
        patcher.apply(change, dataset)
        logging.info(dataset)
        logging.info(yaml_dumper.dumps(dataset))
        assert len(dataset.persons) == n_persons + 1
        ok = False
        for p in dataset.persons:
            if p.id == 'P:222':
                assert p.has_familial_relationships[0].related_to == 'P:001'
                ok = True
        assert ok