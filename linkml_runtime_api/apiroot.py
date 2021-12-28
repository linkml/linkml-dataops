from abc import ABC
from dataclasses import dataclass
from typing import Any

from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

PATH_EXPRESSION = str

@dataclass
class Database:
    """
    Abstraction over different datastores

    Currently only one supported
    """
    name: str = None
    #document: YAMLRoot = None
    data: Any = None

@dataclass
class ApiRoot(ABC):
    """
    Base class for runtime API

    This class only contains base methods and cannot be used directly. Instead use:

    * :ref:`changer` -- for update operations on instances of a LinkML model
    * :ref:`queryengine` -- for query operations on instances of a LinkML model
    """


    schemaview: SchemaView = None

    def select_path(self, path: PATH_EXPRESSION, element: YAMLRoot) -> YAMLRoot:
        """
        Return the sub-element matching the path expression

        The query path is a slash-delimited list of slot names, indicating
        a path from the element to the return value

        For example, calling with path='a/b/c' to element=x yields
        x.a.b.c

        :param path: query path
        :param element: object to be queried
        :return: matching sub-element
        """
        parts = path.split('/')
        if parts[0] == '':
            parts = parts[1:]
        if parts == []:
            return element
        #nxt = parts[0]
        new_path = '/'.join(parts[1:])
        selector = parts[0]
        new_element = None
        if isinstance(element, dict):
            new_element = element[selector]
        elif isinstance(element, list):
            for x in element:
                x_id = self._get_primary_key_value_for_element(x)
                if selector == x_id:
                    new_element = x
                    break
            if new_element is None:
                raise Exception(f'Could not find {selector} in list {element}')
        else:
            new_element = getattr(element, selector)
        return self.select_path(new_path, new_element)

    def _yield_path(self, path: str, element: YAMLRoot) -> YAMLRoot:
        """
        As `select_path`, but accepts '*' in paths and may yield multiple objects

        :param path:
        :param element:
        :return:
        """
        parts = path.split('/')
        if parts[0] == '':
            parts = parts[1:]
        if len(parts) == 0:
            yield element
            return
        if parts == ['.']:
            yield element
            return
        new_path = '/'.join(parts[1:])
        selector = parts[0]
        new_element = None
        if isinstance(element, dict):
            new_element = element[selector]
        elif isinstance(element, list):
            if selector == '*':
                for x in element:
                    for p in self._yield_path(new_path, x):
                        yield p
                return
            for x in element:
                x_id = self._get_primary_key_value_for_element(x)
                if selector == x_id:
                    new_element = x
                    break
            if new_element is None:
                raise Exception(f'Could not find {selector} in list {element}')
        else:
            new_element = getattr(element, selector)
        for p in self._yield_path(new_path, new_element):
            yield p

    def _get_primary_key_value_for_element(self, element: YAMLRoot) -> str:
        """
        value of the slot that is assigned as identifier for the class that element instantiates

        :param element:
        :return:
        """
        cn = type(element).class_name
        if cn is None:
            raise Exception(f'Could not determine LinkML class name from {change.value}')
        pk = self.schemaview.get_identifier_slot(cn)
        return getattr(element, pk.name)

    def _get_top_level_classes(self, container_class=None):
        sv = self.schemaview
        cns = []
        for slot in sv.class_induced_slots(container_class):
            if slot.range in sv.all_class():
                cns.append(slot.range)
        return cns
