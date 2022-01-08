# Auto generated from changes.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-19 00:49
# Schema: changes
#
# id: https://w3id.org/linkml/changes
# description: A generic datamodel for representing changes
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
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
JSONPATCH = CurieNamespace('jsonpatch', 'https://w3id.org/linkml/jsonpatch')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = JSONPATCH


# Types
class PathExpression(str):
    """ A path expression conformant to [rfc6901](https://datatracker.ietf.org/doc/html/rfc6901) """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "PathExpression"
    type_model_uri = JSONPATCH.PathExpression


# Class references



ChangeTarget = Any

@dataclass
class Change(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.Change
    class_class_curie: ClassVar[str] = "jsonpatch:Change"
    class_name: ClassVar[str] = "Change"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.Change

    path: Optional[str] = None
    parent: Optional[Union[dict, ChangeTarget]] = None
    value: Optional[Union[dict, ChangeTarget]] = None
    primary_key_slot: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        if self.primary_key_slot is not None and not isinstance(self.primary_key_slot, str):
            self.primary_key_slot = str(self.primary_key_slot)

        super().__post_init__(**kwargs)


class AddObject(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.AddObject
    class_class_curie: ClassVar[str] = "jsonpatch:AddObject"
    class_name: ClassVar[str] = "AddObject"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.AddObject


class RemoveObject(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.RemoveObject
    class_class_curie: ClassVar[str] = "jsonpatch:RemoveObject"
    class_name: ClassVar[str] = "RemoveObject"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.RemoveObject


@dataclass
class Rename(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.Rename
    class_class_curie: ClassVar[str] = "jsonpatch:Rename"
    class_name: ClassVar[str] = "Rename"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.Rename

    old_value: Optional[str] = None
    target_class: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.old_value is not None and not isinstance(self.old_value, str):
            self.old_value = str(self.old_value)

        if self.target_class is not None and not isinstance(self.target_class, str):
            self.target_class = str(self.target_class)

        super().__post_init__(**kwargs)


class SetValue(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.SetValue
    class_class_curie: ClassVar[str] = "jsonpatch:SetValue"
    class_name: ClassVar[str] = "SetValue"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.SetValue


class SetAtomicValue(SetValue):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.SetAtomicValue
    class_class_curie: ClassVar[str] = "jsonpatch:SetAtomicValue"
    class_name: ClassVar[str] = "SetAtomicValue"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.SetAtomicValue


class SetComplexValue(SetValue):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.SetComplexValue
    class_class_curie: ClassVar[str] = "jsonpatch:SetComplexValue"
    class_name: ClassVar[str] = "SetComplexValue"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.SetComplexValue


class Append(Change):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONPATCH.Append
    class_class_curie: ClassVar[str] = "jsonpatch:Append"
    class_name: ClassVar[str] = "Append"
    class_model_uri: ClassVar[URIRef] = JSONPATCH.Append


# Enumerations


# Slots

