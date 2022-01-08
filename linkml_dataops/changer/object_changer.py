from copy import copy, deepcopy

from linkml_dataops.changer.changer import Changer, ChangeResult
from linkml_dataops.changer.changes_model import Change, AddObject, RemoveObject, Append, Rename
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.yamlutils import YAMLRoot



class ObjectChanger(Changer):
    """
    A :class:`Changer` that operates over an in-memory object tree
    """

    def apply(self, change: Change, element: YAMLRoot, in_place=True) -> ChangeResult:
        """
        Apply a change directly to an element in an in-memory object tree

        change objects must be generic change objects

        :param change: any subtype of Change
        :param element: where the change is being applied
        :param in_place: if true, modify element directly
        :return:
        """
        change = self._map_change_object(change)
        if not in_place:
            element = deepcopy(element)
        if isinstance(change, AddObject):
            return self.add_object(change, element)
        elif isinstance(change, RemoveObject):
            return self.remove_object(change, element)
        elif isinstance(change, Append):
            return self.append_value(change, element)
        elif isinstance(change, Rename):
            return self.rename(change, element)
        else:
            raise Exception(f'Unknown type {type(change)} for {change}')

    # NOTE: changes in place
    def add_object(self, change: AddObject, element: YAMLRoot) -> ChangeResult:
        place = self._locate_object(change, element)
        pk_slot = self._get_primary_key(change)
        pk_val = getattr(change.value, pk_slot)
        if isinstance(place, dict):
            place[pk_val] = change.value
        elif isinstance(place, list):
            place.append(change.value)
        else:
            raise Exception(f'place {place} cannot be added to')
        return ChangeResult(object=element)


    # NOTE: changes in place
    def remove_object(self, change: RemoveObject, element: YAMLRoot) -> ChangeResult:
        place = self._locate_object(change, element)
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
            del place[ix]
            #if change.value not in place:
            #    raise Exception(f'value {v} not in list: {place}')
            #place.remove(change.value)
        else:
            del place[v]
        return ChangeResult(object=element)

    # NOTE: changes in place
    def append_value(self, change: Append, element: YAMLRoot) -> ChangeResult:
        place = self._locate_object(change, element)
        place.append(change.value)
        return ChangeResult(object=element)

    # NOTE: changes in place
    def rename(self, change: Rename, element: YAMLRoot) -> ChangeResult:
        element = self._rename(change, element)
        return ChangeResult(object=element)

    def _rename(self, change: Rename, element: YAMLRoot) -> YAMLRoot:
        sv = self.schemaview
        if not isinstance(element, YAMLRoot):
            return element
        cn = type(element).class_name
        #print(f'CN={cn}')
        if cn == change.target_class:
            pk = sv.get_identifier_slot(change.target_class)
            if pk is not None:
                pk_val = getattr(element, pk.name)
                if pk_val == change.old_value:
                    setattr(element, pk.name, change.value)
        slots = sv.class_induced_slots(cn)
        for k, v in element.__dict__.items():
            is_replace = False
            for s in slots:
                #print(f'Testing slot {s.name} --  {k} == {s.name}')
                if underscore(k) == underscore(s.name):
                    #print(f'  xxTesting slot {s.name} -- {change.target_class} == {s.range} // {cn}')
                    if s.range == change.target_class:
                        is_replace = True
                        #print(f'    REPLACE!!')
                        break
            def replace(v):
                if v == change.old_value:
                    return change.value
                else:
                    return v
            if isinstance(v, list):
                if is_replace:
                    v = [replace(v1) for v1 in v]
                v = [self._rename(change, v1) for v1 in v]
            elif isinstance(v, dict):
                if is_replace:
                    if change.old_value in v:
                        v[change.value] = v[change.old_value]
                        del v[change.old_value]
                v = {k: self._rename(change, v1) for k, v1 in v.items()}
            elif isinstance(v, str):
                if is_replace:
                    v = replace(v)
            else:
                v = self._rename(change, v)
            setattr(element, k, v)
        return element







