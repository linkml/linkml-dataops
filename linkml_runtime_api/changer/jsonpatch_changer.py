import logging
from typing import List, Dict, Any
import json

from jsonpatch import JsonPatch

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import json_loader
from linkml_runtime_api.changer.changer import Changer, ChangeResult
from linkml_runtime_api.changer.changes_model import Change, AddObject, RemoveObject, Append, Rename
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.yamlutils import YAMLRoot

OPDICT = Dict[str, Any]
OPS = List[OPDICT]

def _element_to_dict(element: YAMLRoot) -> dict:
    jsonstr = json_dumper.dumps(element, inject_type=False)
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
            if change.value not in place:
                raise Exception(f'value {v} not in list: {place}')
            op['path'] = f'{path}/{place.index(change.value)}'
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

