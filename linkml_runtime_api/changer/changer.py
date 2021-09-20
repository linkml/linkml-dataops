from dataclasses import dataclass, field

from linkml_runtime.utils.formatutils import underscore

from linkml_runtime_api.apiroot import ApiRoot
from linkml_runtime_api.changer.changes_model import Change, AddObject, RemoveObject
from linkml_runtime.utils.yamlutils import YAMLRoot

@dataclass
class ChangeResult:
    object: YAMLRoot
    modified: bool = field(default_factory=lambda: True)

@dataclass
class Changer(ApiRoot):
    """
    Base class for engines that perform changes on elements

    Currently the most useful subclasses:

    * :class:`ObjectChanger` - operate directly on objects
    * :class:`JsonChanger` - operate via generating JSON Patches
    """

    def apply(self, change: Change, element: YAMLRoot) -> ChangeResult:
        raise Exception(f'Base class')

    def _map_change_object(self, change: YAMLRoot) -> Change:
        if isinstance(change, Change):
            return change
        cn = type(change).class_name
        for prefix, direct_cn in [('Add', AddObject),
                                  ('Remove', RemoveObject)]:
            if cn.startswith(prefix):
                new_change_obj = direct_cn()
                new_change_obj.path = change.path
                new_change_obj.value = change.value
                return new_change_obj
        return None


    def _path_to_jsonpath(self, path: str, element: YAMLRoot) -> str:
        toks = path.split('/')
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
        return '/'.join(nu)

    def _get_jsonpath(self, change: Change, element: YAMLRoot) -> str:
        if change.path is not None:
            return self._path_to_jsonpath(change.path, element)
        else:
            return self._path_to_jsonpath(self._get_path(change, element), element)

    def _get_path(self, change: Change, element: YAMLRoot, strict=True) -> str:
        if change.path is not None:
            return change.path
        else:
            target_cn = type(change.value).class_name
            sv = self.schemaview
            if sv is None:
                raise Exception(f'Must pass path OR schemaview')
            paths = []
            for cn, c in sv.all_class().items():
                for slot in sv.class_induced_slots(cn):
                    if slot.inlined and slot.range == target_cn:
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
                raise Exception(f'No matching top level slot')

    def _locate_object(self, change: Change, element: YAMLRoot) -> YAMLRoot:
        if change.parent is not None:
            return change.parent
        else:
            path = self._get_path(change, element)
            return self.select_path(path, element)

    def _get_primary_key_value(self, change: Change) -> str:
        pk_slot = self._get_primary_key(change)
        return getattr(change.value, pk_slot)

    def _get_primary_key(self, change: Change) -> str:
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
