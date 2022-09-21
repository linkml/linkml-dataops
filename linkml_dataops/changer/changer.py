from copy import deepcopy
from dataclasses import dataclass, field
from typing import List

from linkml_runtime.utils.formatutils import underscore

from linkml_dataops.apiroot import ApiRoot, PATH_EXPRESSION
from linkml_dataops.changer.changes_model import Change, AddObject, RemoveObject, Append
from linkml_runtime.utils.yamlutils import YAMLRoot

@dataclass
class ChangeResult:
    object: YAMLRoot
    modified: bool = field(default_factory=lambda: True)

@dataclass
class Changer(ApiRoot):
    """
    Base class for engines that perform changes on elements

    Implementing classes must implement :ref:`apply`

    Currently the most useful subclasses:

    * :class:`ObjectChanger` - operate directly on objects
    * :class:`JsonChanger` - operate via generating JSON Patches
    """

    def apply(self, change: Change, element: YAMLRoot = None) -> ChangeResult:
        """
        Apply a change object to the change engine

        :param change:
        :param element:
        :return:
        """
        raise NotImplementedError(f'{self} must implement this method')

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

    def _map_change_object(self, change: YAMLRoot) -> Change:
        """
        maps a domain change object to a generic one

        :param change:
        :return:
        """
        if isinstance(change, Change):
            return change
        cn = type(change).class_name
        for prefix, direct_cn in [('Add', AddObject),
                                  ('Append', Append),
                                  ('Remove', RemoveObject)]:
            if cn.startswith(prefix):
                new_change_obj = direct_cn()
                new_change_obj.path = change.path
                new_change_obj.value = change.value
                #TODO: new_change_obj.parent = change.parent
                return new_change_obj
        return None


    def _path_to_jsonpath(self, path: PATH_EXPRESSION, element: YAMLRoot) -> str:
        # TODO: do not repeat code with parent
        toks = path.split('/')
        #if not toks[0]:
        #    toks = toks[1:]
        nu = []
        curr_el = element
        for selector in toks:
            nxt = selector
            if selector == '':
                None
            else:
                new_element = None
                if isinstance(curr_el, dict):
                    new_element = curr_el[selector]
                    nxt = selector
                elif isinstance(curr_el, list):
                    if selector.isdigit():
                        new_element = curr_el[int(selector)]
                    else:
                        i = 0
                        for x in curr_el:
                            x_id = self._get_primary_key_value_for_element(x)
                            if selector == x_id:
                                new_element = x
                                nxt = str(i)
                                break
                            i += 1
                    if new_element is None:
                        raise Exception(f'Could not find {selector} in list {element}')
                else:
                    new_element = getattr(curr_el, selector)
                curr_el = new_element
            nu.append(nxt)
        p = '/'.join(nu)
        if not p.startswith('/'):
            p = f'/{p}'
        return p

    def _get_jsonpath(self, change: Change, element: YAMLRoot) -> str:
        """
        Find the json path for a change object:

        1. if explicitly set, use this
        2. otherwise, find using :ref:`_get_path`
        :param change:
        :param element:
        :return:
        """
        if change.path is not None:
            return self._path_to_jsonpath(change.path, element)
        else:
            return self._path_to_jsonpath(self._get_path(change, element), element)

    def _get_path(self, change: Change, element: YAMLRoot, strict=True) -> PATH_EXPRESSION:
        """
        Get the path for a change object, relative to element

        :param change:
        :param element:
        :param strict:
        :return:
        """
        if change.path is not None:
            return change.path
        else:
            target_cn = type(change.value).class_name
            sv = self.schemaview
            if sv is None:
                raise Exception(f'Must pass path OR schemaview')
            paths = []
            # find potential slots in element
            # TODO: replace this with a SchemaView method
            for cn, c in sv.all_classes().items():
                if cn != type(element).class_name:
                    continue
                for slot in sv.class_induced_slots(cn):
                    #if slot.inlined and slot.range == target_cn:
                    if slot.range == target_cn:
                        k = underscore(slot.name)
                        paths.append(f'/{k}')
            if len(paths) > 1:
                if strict:
                    raise Exception(f'Multiple possible paths: {paths}')
                sorted(paths, key=lambda p: len(p.split('/')))
                return paths[0]
            elif len(paths) == 1:
                return paths[0]
            else:
                raise ValueError(f'No matching slots in element have a range of {target_cn}')

    def _locate_object(self, change: Change, element: YAMLRoot) -> YAMLRoot:
        """
        resolves a change path

        :param change:
        :param element:
        :return:
        """
        if change.parent is not None:
            return change.parent
        else:
            # We need to obtain the path if it is not already given
            # for example, if an append object is applied on object X,
            # to append a Y, we need to know the slot that holds Ys
            path = self._get_path(change, element)
            return self.select_path(path, element)

    def _locate_object_slot(self, change: Change, element: YAMLRoot) -> (YAMLRoot, str):
        change = deepcopy(change)
        path_toks = change.path.split('/')
        change.path = '/'.join(path_toks[:-1])
        place = self._locate_object(change, element)
        return (place, path_toks[-1])

    def _get_primary_key_value(self, change: Change) -> str:
        pk_slot = self._get_primary_key_slot(change)
        return getattr(change.value, pk_slot)

    def _get_primary_key_slot(self, change: Change) -> str:
        """
        Gets the primary key slot for a change.
        If not explicitly set, this is the identifier slot for the valye
        :param change:
        :return:
        """
        if change.primary_key_slot is None:
            sv = self.schemaview
            if sv is None:
                raise Exception(f'Must pass EITHER primary_key_slot in change object OR set schemaview')
            cn = type(change.value).class_name
            if cn is None:
                raise Exception(f'Could not determine LinkML class name from {change.value}')
            pk = sv.get_identifier_slot(cn)
            return pk.name
        else:
            return change.primary_key_slot
