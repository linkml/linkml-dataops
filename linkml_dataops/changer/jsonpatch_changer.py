import logging
import os
import sys
from collections import defaultdict
from typing import List, Dict, Any, Optional, Union, IO, Type
import json

import click
import yaml
from jsonasobj2 import items, is_list, is_dict, JsonObj
from jsonpatch import JsonPatch

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import ClassDefinitionName
from linkml_runtime.loaders import json_loader, yaml_loader
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.schemaview import SchemaView
from ruamel.yaml import YAML

from linkml_runtime_api.changer.changer import Changer, ChangeResult
from linkml_runtime_api.changer.changes_model import Change, AddObject, RemoveObject, Append, Rename
from linkml_runtime.utils.formatutils import underscore, is_empty
from linkml_runtime.utils.yamlutils import YAMLRoot, as_json_object
from linkml_runtime_api.diffs.yaml_patch import YAMLPatch

OPDICT = Dict[str, Any]
OPS = List[OPDICT]

# this is a copy-and-edit of remove_empty_items in formatutils
# TODO: rewrite this
def to_object(obj: Any, hide_protected_keys: bool = False, inside: bool = False) -> Any:
    """
    Recursively iterate over obj translating to dicts for json


    :param obj: Object to be tweaked
    :param hide_protected_keys: True means remove keys that begin with an underscore
    :param inside: Keep from removing the outermost container
    :return: copy of obj with empty items removed or None if obj itself is "empty"
    """
    #print(f'T {type(obj)} // {obj} // {isinstance(obj, JsonObj)}')
    #print(f'I {items(obj)}')
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

def _element_to_dict(element: YAMLRoot) -> dict:
    #jsonstr = json_dumper.dumps(element, inject_type=False)
    jsonstr = json.dumps(as_json_object(element, None, inject_type=False),
                         default=lambda o: to_object(o, hide_protected_keys=True) if isinstance(o, YAMLRoot) else json.JSONDecoder().decode(o),
                         indent='  ')
    return json.loads(jsonstr)

class JsonPatchChanger(Changer):
    """
    A :class:`Patcher` that works by first creating :class:`JsonPath` objects, then applying them
    """

    def apply(self, change: Change, element: YAMLRoot, in_place=True) -> ChangeResult:
        """
        Generates a JsonPatch and then applies it

        See :meth:`.make_patch`

        :param change:
        :param element:
        :param in_place:
        :return:
        """
        change = self._map_change_object(change)
        patch_ops = self.make_patch(change, element)
        patch = JsonPatch(patch_ops)
        logging.info(f'Patch = {patch_ops}')
        element_dict = _element_to_dict(element)
        print(f'DICT={element_dict}')
        result = patch.apply(element_dict)
        typ = type(element)
        jsonstr = json_dumper.dumps(result, inject_type=False)
        result = json_loader.loads(jsonstr, target_class=typ)
        if in_place:
            new_obj = result
            if isinstance(element, dict):
                for k, v in element.items():
                    element[k] = new_obj[k]
            else:
                for k in element.__dict__:
                    setattr(element, k, getattr(new_obj, k))
        return ChangeResult(result)

    def apply_multiple(self, changes: List[Change], element: YAMLRoot) -> List[ChangeResult]:
        """
        Applies multiple changes in place

        :param changes:
        :param element:
        :return:
        """
        results = []
        for change in changes:
            results.append(self.apply(change, element, in_place=True))
        return results

    def _value(self, change: Change):
        # TODO: move this functionality into json_dumper
        return json.loads(json_dumper.dumps(change.value, inject_type=False))

    def make_patch(self, change: Change, element: YAMLRoot) -> OPS:
        """
        Generates a list of JsonPatch objects from a Change

        These can then be directly applied, or applied later out of band,
        e.g. using :meth:`JsonPath.apply`

        :param change:
        :param element:
        :return:
        """
        change = self._map_change_object(change)
        if isinstance(change, AddObject):
            return self.make_add_object_patch(change, element)
        elif isinstance(change, RemoveObject):
            return self.make_remove_object_patch(change, element)
        elif isinstance(change, Append):
            return self.make_append_patch(change, element)
        elif isinstance(change, Rename):
            return self.make_rename_patch(change, element)
        else:
            raise Exception(f'Unknown type {type(change)} for {change}')

    def make_add_object_patch(self, change: AddObject, element: YAMLRoot) -> OPS:
        path = self._get_jsonpath(change, element)
        place = self._locate_object(change, element)
        pk_slot = self._get_primary_key(change)
        pk_val = getattr(change.value, pk_slot)
        v = self._value(change)
        op = dict(op='add', value=v)
        if isinstance(place, dict):
            op['path'] = f'{path}/pk_val'
        elif isinstance(place, list):
            op['path'] = f'{path}/{len(place)}'
        else:
            raise Exception(f'place {place} cannot be added to')
        return [op]

    def make_remove_object_patch(self, change: RemoveObject, element: YAMLRoot) -> OPS:
        place = self._locate_object(change, element)
        path = self._get_jsonpath(change, element)
        op = dict(op='remove')
        if isinstance(change.value, str):
            v = change.value
        else:
            v = self._get_primary_key_value(change)
        if isinstance(place, list):
            ix = None
            if change.value in place:
                ix = place.index(change.value)
            if ix is None:
                pk = self._get_primary_key(change)
                if pk:
                    for i in range(0,len(place)):
                        if getattr(place[i], pk) == v:
                            ix = i
                            break
            if ix is None:
                raise Exception(f'value {v} not in list: {place}')
            op['path'] = f'{path}/{ix}'
        else:
            op['path'] = f'{path}/{v}'
        return [op]

    def make_append_patch(self, change: Append, element: YAMLRoot) -> OPS:
        """
        Apply an :class:`Append` change

        :param change:
        :param element:
        :return:
        """
        path = self._get_jsonpath(change, element)
        place = self._locate_object(change, element)
        if not isinstance(place, list):
            raise Exception(f'Expected list got {place}')
        v = self._value(change)
        n = len(place)
        if n == 0:
            op = dict(op='add', value=[v], path=path)
        else:
            op = dict(op='add', value=v, path=f'{path}/{n}')
        return [op]

    def make_rename_patch(self, change: Rename, element: YAMLRoot) -> OPS:
        """
        Apply a Rename change

        :param change:
        :param element:
        :return:
        """
        path = self._get_path(change, element)
        ops = self._rename(change, element, path)
        return ops


    def _rename(self, change: Rename, element: YAMLRoot, path: str) -> OPS:
        ops = []
        def add_op(op, path_ext):
            op = dict(op=op, path=f'{path}/{path_ext}', value=change.value)
            ops.append(op)
        sv = self.schemaview
        if not isinstance(element, YAMLRoot):
            return []
        cn = type(element).class_name
        if cn == change.target_class:
            pk = sv.get_identifier_slot(change.target_class)
            if pk is not None:
                pk_val = getattr(element, pk.name)
                if pk_val == change.old_value:
                    add_op('replace', pk.name)
        slots = sv.class_induced_slots(cn)
        for k, v in element.__dict__.items():
            next_path = f'{path}/{k}'
            range_matches_target = False
            for s in slots:
                if underscore(k) == underscore(s.name):
                    if s.range == change.target_class:
                        range_matches_target = True
                        break
            if isinstance(v, list):
                if range_matches_target:
                    i = 0
                    for v1 in v:
                        if v1 == change.old_value:
                            add_op('replace', k)
                        i += 1
                i = 0
                for v1 in v:
                    ops += self._rename(change, v1, f'{next_path}/{i}')
                    i += 1
            elif isinstance(v, dict):
                if range_matches_target:
                    if change.old_value in v:
                        op = {"op": 'move',
                              "from": f'{path}/{k}/{change.old_value}',
                              "path": f'{path}/{k}/{change.value}'}
                        ops.append(op)
                for k, v1 in v.items():
                    ops += self._rename(change, v1, next_path)
            elif isinstance(v, str):
                if range_matches_target and v == change.old_value:
                    add_op('replace', k)
            else:
                 ops += self._rename(change, v, next_path)
        return ops

    def patch_file(self, input_file: Union[str, IO[str]], changes: List[Change],
                   target_class: Type[YAMLRoot],
                   format: str = None, out_stream=None):
        if format is None:
            if out_stream is not None:
                if isinstance(out_stream, str) and '.' in out_stream:
                    format = out_stream.split('.')[-1]
        if format is None:
            format = 'yaml'
        if format == 'yaml' or format == 'yml':
            obj = yaml_loader.load(input_file, target_class=target_class)
            patches = []
            for change in changes:
                patches += self.make_patch(change, element=obj)
                self.apply(change, obj, in_place=True)
            # reload with rueaml, preserving comments
            yp = YAMLPatch()
            if out_stream is None:
                out_stream = sys.stdout
            yp.multipatch(input_file, patches, outstream=out_stream)
        elif format == 'json':
            obj = json_loader.load(input_file, target_class=target_class)
            self.apply_multiple(changes, obj)
            json_dumper.dump(obj, out_stream)
        else:
            raise ValueError(f'Unknown format: {format}')


# TODO: move to schemaview
def infer_root_class(sv: SchemaView) -> Optional[ClassDefinitionName]:
    """
    Infer the class that should be at the root of the object tree

    (Note this is distinct from the root of the class hierarchy)

    If a class is explicitly designated with tree_root, use this.
    Otherwise use the class that is not referenced as a range in any other class.
    """
    for c in sv.all_class().values():
        if c.tree_root:
            return c.name
    refs = defaultdict(int)
    for cn in sv.all_class().keys():
        for sn in sv.class_slots(cn):
            slot = sv.induced_slot(sn, cn)
            r = slot.range
            if r in sv.all_class():
                for a in sv.class_ancestors(r):
                    refs[a] += 1
    candidates = [cn for cn in sv.all_class().keys() if cn not in refs]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return None

# TODO: move this
aliases = {'yml': 'yaml'}
def _get_format(path: str, specified_format: str =None, default=None):
    if specified_format is None:
        if path is None:
            if default is None:
                raise Exception(f'Must pass format option OR pass a filename with known file suffix')
            else:
                specified_format = default
        else:
            _, ext = os.path.splitext(path)
            if ext is not None:
                specified_format = ext.replace('.', '')
            else:
                raise Exception(f'Must pass format option OR use known file suffix: {path}')
    specified_format = specified_format.lower()
    if specified_format in aliases:
        specified_format = aliases[specified_format]
    return specified_format

@click.command()
@click.option("--format", "-f", help="Input format")
@click.option("--schema", "-S", help="Path to schema file")
@click.option("--change-file", "-D", help="File containing yaml of changes")
@click.option("--add", "-A", type=(str, str),
              multiple=True,
              help="add objects. List of ClassName, InitArgs dicts")
@click.option("--remove", "-D", type=(str, str),
              multiple=True,
              help="delete objects")
@click.option("--output", "-o", help="Output file")
@click.option("--module", "-m",
              required=True,
              help="Path to python datamodel module")
@click.option("--target-class", "-C",
              help="name of class in datamodel that the root node instantiates")
@click.argument('inputfile')
def cli(inputfile, format: str, module, schema: str, change_file: str, add: List[str], remove: List[str], target_class: str, output):
    """
    Apply changes

    linkml-apply -m kitchen_sink.py -S kitchen_sink.yaml -A Person '{id: X, name: Y}' kitchen_sink_inst_01.yaml
    """
    python_module = compile_python(module)
    view = SchemaView(schema)
    if target_class is None:
        target_class = infer_root_class(view)
    py_target_class = python_module.__dict__[target_class]
    patcher = JsonPatchChanger(schemaview=view)
    format = _get_format(inputfile, format)
    if format == 'json':
        obj = json_loader.load(inputfile, target_class=py_target_class)
    elif format == 'yaml':
        obj = yaml_loader.load(inputfile, target_class=py_target_class)
    else:
        raise ValueError(f'Cannot handle format {format}')
    changes = []
    if change_file:
        with open(change_file) as stream:
            changes = yaml.load(stream)
    for (typ, ystr) in add:
        init_dict = yaml.safe_load(ystr)
        typ_cls = python_module.__dict__[typ]
        change = AddObject(value=typ_cls(**init_dict))
        changes.append(change)
    for (typ, ystr) in remove:
        init_dict = yaml.safe_load(ystr)
        typ_cls = python_module.__dict__[typ]
        if isinstance(init_dict, dict):
            x_obj = typ_cls(**init_dict)
        else:
            x_obj = typ_cls(init_dict)
        change = RemoveObject(value=x_obj)
        changes.append(change)
    #append_change('RemoveObject', remove)
    logging.info(f'CHANGES: {changes}')
    print(f'CHANGES: {changes}')
    patcher.patch_file(inputfile, changes, target_class=py_target_class, format=format, out_stream=output)


if __name__ == '__main__':
    cli()


