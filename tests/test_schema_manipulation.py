import logging
import unittest

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, SlotDefinition
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime_api.changer.object_changer import ObjectChanger
from linkml_runtime_api.changer.changes_model import AddObject, RemoveObject, Append

class ObjectPatcherTestCase(unittest.TestCase):

    def test_object_patcher(self):
        patcher = ObjectChanger()

        s = SchemaDefinition(id='test', name='test')
        new_class = ClassDefinition('c1',
                                    slot_usage={'s1': SlotDefinition('s1', range='d')},
                                    slots=['s1', 's2'])

        # ADD OBJECT
        obj = AddObject(value=new_class, path='/classes', primary_key_slot='name')
        rs = patcher.apply(obj, s)
        logging.info(rs)
        logging.info(yaml_dumper.dumps(s))
        assert new_class.name in s.classes

        # ADD SUB-OBJECT
        sd = SlotDefinition('s2', range='e')
        obj = AddObject(value=sd, path='/classes/c1/slot_usage', primary_key_slot='name')
        patcher.apply(obj, s)
        assert new_class.slot_usage['s2'].range == 'e'

        # REMOVE OBJECT (inlined)
        obj = RemoveObject(value=new_class, path='/classes', primary_key_slot='name')
        patcher.apply(obj, s)
        assert new_class.name not in s.classes
        logging.info(yaml_dumper.dumps(s))

        # place class back
        patcher.apply(AddObject(value=new_class, path='/classes', primary_key_slot='name'), s)

        # REMOVE OBJECT (by key)
        obj = RemoveObject(value=new_class.name, path='/classes')
        patcher.apply(obj, s)
        assert new_class.name not in s.classes
        logging.info(yaml_dumper.dumps(s))

        # place class back
        patcher.apply(AddObject(value=new_class, path='/classes', primary_key_slot='name'), s)

        # APPEND
        obj = Append(value='new_slot', path='/classes/c1/slots')
        patcher.apply(obj, s)
        assert 'new_slot' in new_class.slots
        logging.info(yaml_dumper.dumps(s))

        # REMOVE ATOMIC FROM LIST
        obj = RemoveObject(value='new_slot', path='/classes/c1/slots')
        patcher.apply(obj, s)
        assert 'new_slot' not in s.classes['c1'].slots
        logging.info(yaml_dumper.dumps(s))





if __name__ == '__main__':
    unittest.main()
