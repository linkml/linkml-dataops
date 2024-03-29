import json
import logging
from copy import copy
from types import ModuleType
from typing import Any, List, Dict

from jsonasobj2 import is_list, is_dict, items
from linkml_runtime.utils.formatutils import is_empty

# this is a copy-and-edit of remove_empty_items in formatutils
# TODO: rewrite this
from linkml_runtime.utils.yamlutils import YAMLRoot, as_json_object

from linkml_dataops.changer.changes_model import AddObject, RemoveObject, Change, Rename, Append


def to_object(obj: Any, hide_protected_keys: bool = False, inside: bool = False) -> Any:
    """
    Recursively iterate over obj translating to dicts for json


    :param obj: Object to be tweaked
    :param hide_protected_keys: True means remove keys that begin with an underscore
    :param inside: Keep from removing the outermost container
    :return: copy of obj with empty items removed or None if obj itself is "empty"
    """
    if is_list(obj):
        # for discussion of logic, see: https://github.com/linkml/linkml-runtime/issues/42
        obj_list = [e for e in [to_object(l, hide_protected_keys=hide_protected_keys, inside=True)
                                for l in obj if l != '_root']]
        return obj_list if not inside or not is_empty(obj_list) else []
    elif is_dict(obj):
        obj_dict = {k: v for k, v in [(k2, to_object(v2, hide_protected_keys=hide_protected_keys, inside=True))
                                      for k2, v2 in items(obj)]}

        # https://github.com/linkml/linkml/issues/119
        # Remove the additional level of nesting with enums
        if len(obj_dict) == 1 and list(obj_dict.keys())[0] == '_code':
            enum_text = list(obj_dict.values())[0].get('text', None)
            if enum_text is not None:
                return enum_text
        if hide_protected_keys and len(obj_dict) == 1 and str(list(obj_dict.keys())[0]).startswith('_'):
            inner_element = list(obj_dict.values())[0]
            if isinstance(inner_element, dict):
                obj_dict = inner_element
        return obj_dict if not inside or not is_empty(obj_dict) else None
    #elif is_empty(obj):
    #    return None
    else:
        return obj


def element_to_dict(element: YAMLRoot) -> dict:
    jsonstr = json.dumps(as_json_object(element, None, inject_type=False),
                         default=lambda o: to_object(o, hide_protected_keys=True) if isinstance(o, YAMLRoot) else json.JSONDecoder().decode(o),
                         indent='  ')
    return json.loads(jsonstr)

OP_PREFIX_DICT = {
    'Add': AddObject,
    'Remove': RemoveObject,
    'Rename': Rename,
    'AddTo': Append,
}

def dicts_to_changes(objs: List[Dict], python_module: ModuleType) -> List[Change]:
    changes = []
    for obj in objs:
        obj = copy(obj)
        t = obj['type']
        del obj['type']
        if t.startswith('Add'):
            cc = AddObject
            t = t.replace('Add', '', 1)
        elif t.startswith('Remove'):
            cc = RemoveObject
            t = t.replace('Remove', '', 1)
        elif t.startswith('Rename'):
            cc = Rename
            t = t.replace('Rename', '', 1)
        elif t.startswith('AppendIn'):
            cc = Append
            t = t.replace('AppendIn', '', 1)
        else:
            raise ValueError(f'Unknown type: {t}')
        typ_cls = python_module.__dict__[t]
        v_dict = obj['value']
        del obj['value']
        if cc == Rename:
            change = Rename(value=v_dict, target_class=typ_cls.class_name, **obj)
        else:
            if isinstance(v_dict, dict):
                v = typ_cls(**v_dict)
            else:
                v = typ_cls(v_dict)
            change = cc(value=v, **obj)
        logging.debug(f'Created change object: {change}')
        changes.append(change)
    return changes

