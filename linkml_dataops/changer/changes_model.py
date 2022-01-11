# Auto generated from changes.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-09T21:22:09
# Schema: linkml_changes
#
# id: https://w3id.org/linkml/changes
# description: A generic datamodel for representing changes on objects
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CHANGES = CurieNamespace('changes', 'https://w3id.org/linkml/changes')
JSONPATCH = CurieNamespace('jsonpatch', 'https://w3id.org/linkml/jsonpatch')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CHANGES


# Types
class PathExpression(str):
    """ A path expression conformant to [rfc6901](https://datatracker.ietf.org/doc/html/rfc6901) """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "PathExpression"
    type_model_uri = CHANGES.PathExpression


# Class references



ChangeTarget = Any

@dataclass
class Change(YAMLRoot):
    """
    An abstract class that is the parent of all change objects.

    A change object represents a patch that can be applied to an object
    yielding a modified object
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.Change
    class_class_curie: ClassVar[str] = "changes:Change"
    class_name: ClassVar[str] = "Change"
    class_model_uri: ClassVar[URIRef] = CHANGES.Change

    path: Optional[str] = None
    parent: Optional[Union[dict, ChangeTarget]] = None
    value: Optional[Union[dict, ChangeTarget]] = None
    value_type: Optional[Union[str, URIorCURIE]] = None
    old_value: Optional[Union[dict, ChangeTarget]] = None
    primary_key_slot: Optional[str] = None
    strict: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        if self.value_type is not None and not isinstance(self.value_type, URIorCURIE):
            self.value_type = URIorCURIE(self.value_type)

        if self.primary_key_slot is not None and not isinstance(self.primary_key_slot, str):
            self.primary_key_slot = str(self.primary_key_slot)

        if self.strict is not None and not isinstance(self.strict, Bool):
            self.strict = Bool(self.strict)

        super().__post_init__(**kwargs)


@dataclass
class AddObject(Change):
    """
    A change object that represents the addition of an object to another object
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.AddObject
    class_class_curie: ClassVar[str] = "changes:AddObject"
    class_name: ClassVar[str] = "AddObject"
    class_model_uri: ClassVar[URIRef] = CHANGES.AddObject

    parent: Optional[Union[dict, ChangeTarget]] = None
    value: Optional[Union[dict, ChangeTarget]] = None

@dataclass
class RemoveObject(Change):
    """
    A change object that represents the removal of an object from another object
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.RemoveObject
    class_class_curie: ClassVar[str] = "changes:RemoveObject"
    class_name: ClassVar[str] = "RemoveObject"
    class_model_uri: ClassVar[URIRef] = CHANGES.RemoveObject

    parent: Optional[Union[dict, ChangeTarget]] = None
    value: Optional[Union[dict, ChangeTarget]] = None
    strict: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.strict is not None and not isinstance(self.strict, Bool):
            self.strict = Bool(self.strict)

        super().__post_init__(**kwargs)


@dataclass
class ReplaceObject(Change):
    """
    A change object that represents the removal of an object from another object followed by an add
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.ReplaceObject
    class_class_curie: ClassVar[str] = "changes:ReplaceObject"
    class_name: ClassVar[str] = "ReplaceObject"
    class_model_uri: ClassVar[URIRef] = CHANGES.ReplaceObject

    parent: Optional[Union[dict, ChangeTarget]] = None
    old_value: Optional[Union[dict, ChangeTarget]] = None
    value: Optional[Union[dict, ChangeTarget]] = None

class SetValue(Change):
    """
    A change object that represents setting the value of a slot
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.SetValue
    class_class_curie: ClassVar[str] = "changes:SetValue"
    class_name: ClassVar[str] = "SetValue"
    class_model_uri: ClassVar[URIRef] = CHANGES.SetValue


class Append(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.Append
    class_class_curie: ClassVar[str] = "changes:Append"
    class_name: ClassVar[str] = "Append"
    class_model_uri: ClassVar[URIRef] = CHANGES.Append


@dataclass
class Rename(Change):
    """
    A change object that represents changing the name/identifier of an object,
    together with cascading changes to referencing objects
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHANGES.Rename
    class_class_curie: ClassVar[str] = "changes:Rename"
    class_name: ClassVar[str] = "Rename"
    class_model_uri: ClassVar[URIRef] = CHANGES.Rename

    old_value: Optional[str] = None
    target_class: Optional[str] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.target_class is not None and not isinstance(self.target_class, str):
            self.target_class = str(self.target_class)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.path = Slot(uri=CHANGES.path, name="path", curie=CHANGES.curie('path'),
                   model_uri=CHANGES.path, domain=None, range=Optional[str])

slots.value = Slot(uri=CHANGES.value, name="value", curie=CHANGES.curie('value'),
                   model_uri=CHANGES.value, domain=None, range=Optional[Union[dict, ChangeTarget]])

slots.old_value = Slot(uri=CHANGES.old_value, name="old_value", curie=CHANGES.curie('old_value'),
                   model_uri=CHANGES.old_value, domain=None, range=Optional[Union[dict, ChangeTarget]])

slots.value_type = Slot(uri=CHANGES.value_type, name="value_type", curie=CHANGES.curie('value_type'),
                   model_uri=CHANGES.value_type, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.parent = Slot(uri=CHANGES.parent, name="parent", curie=CHANGES.curie('parent'),
                   model_uri=CHANGES.parent, domain=None, range=Optional[Union[dict, ChangeTarget]])

slots.primary_key_slot = Slot(uri=CHANGES.primary_key_slot, name="primary_key_slot", curie=CHANGES.curie('primary_key_slot'),
                   model_uri=CHANGES.primary_key_slot, domain=None, range=Optional[str])

slots.has_part = Slot(uri=CHANGES.has_part, name="has_part", curie=CHANGES.curie('has_part'),
                   model_uri=CHANGES.has_part, domain=None, range=Optional[Union[Union[dict, Change], List[Union[dict, Change]]]])

slots.strict = Slot(uri=CHANGES.strict, name="strict", curie=CHANGES.curie('strict'),
                   model_uri=CHANGES.strict, domain=None, range=Optional[Union[bool, Bool]])

slots.rename__old_value = Slot(uri=CHANGES.old_value, name="rename__old_value", curie=CHANGES.curie('old_value'),
                   model_uri=CHANGES.rename__old_value, domain=None, range=Optional[str])

slots.rename__target_class = Slot(uri=CHANGES.target_class, name="rename__target_class", curie=CHANGES.curie('target_class'),
                   model_uri=CHANGES.rename__target_class, domain=None, range=Optional[str])

slots.AddObject_parent = Slot(uri=CHANGES.parent, name="AddObject_parent", curie=CHANGES.curie('parent'),
                   model_uri=CHANGES.AddObject_parent, domain=AddObject, range=Optional[Union[dict, ChangeTarget]])

slots.AddObject_value = Slot(uri=CHANGES.value, name="AddObject_value", curie=CHANGES.curie('value'),
                   model_uri=CHANGES.AddObject_value, domain=AddObject, range=Optional[Union[dict, ChangeTarget]])

slots.RemoveObject_parent = Slot(uri=CHANGES.parent, name="RemoveObject_parent", curie=CHANGES.curie('parent'),
                   model_uri=CHANGES.RemoveObject_parent, domain=RemoveObject, range=Optional[Union[dict, ChangeTarget]])

slots.RemoveObject_value = Slot(uri=CHANGES.value, name="RemoveObject_value", curie=CHANGES.curie('value'),
                   model_uri=CHANGES.RemoveObject_value, domain=RemoveObject, range=Optional[Union[dict, ChangeTarget]])

slots.RemoveObject_strict = Slot(uri=CHANGES.strict, name="RemoveObject_strict", curie=CHANGES.curie('strict'),
                   model_uri=CHANGES.RemoveObject_strict, domain=RemoveObject, range=Optional[Union[bool, Bool]])

slots.ReplaceObject_parent = Slot(uri=CHANGES.parent, name="ReplaceObject_parent", curie=CHANGES.curie('parent'),
                   model_uri=CHANGES.ReplaceObject_parent, domain=ReplaceObject, range=Optional[Union[dict, ChangeTarget]])

slots.ReplaceObject_old_value = Slot(uri=CHANGES.old_value, name="ReplaceObject_old_value", curie=CHANGES.curie('old_value'),
                   model_uri=CHANGES.ReplaceObject_old_value, domain=ReplaceObject, range=Optional[Union[dict, ChangeTarget]])

slots.ReplaceObject_value = Slot(uri=CHANGES.value, name="ReplaceObject_value", curie=CHANGES.curie('value'),
                   model_uri=CHANGES.ReplaceObject_value, domain=ReplaceObject, range=Optional[Union[dict, ChangeTarget]])

slots.Rename_value = Slot(uri=CHANGES.value, name="Rename_value", curie=CHANGES.curie('value'),
                   model_uri=CHANGES.Rename_value, domain=Rename, range=Optional[str])
