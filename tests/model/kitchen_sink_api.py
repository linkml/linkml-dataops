# Auto generated from kitchen_sink_api.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-19 04:09
# Schema: kitchen_sink_api
#
# id: https://w3id.org/linkml/tests/kitchen_sink_api
# description: API for querying and manipulating objects from the kitchen_sink schema
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
from . kitchen_sink import Activity, ActivityId, Any, Company, CompanyId, Person, PersonId
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
KITCHEN_SINK_API = CurieNamespace('kitchen_sink_api', 'https://w3id.org/linkml/tests/kitchen_sink_api/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = KITCHEN_SINK_API


# Types

# Class references



@dataclass
class LocalChange(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.LocalChange
    class_class_curie: ClassVar[str] = "kitchen_sink_api:LocalChange"
    class_name: ClassVar[str] = "LocalChange"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.LocalChange

    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class LocalQuery(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.LocalQuery
    class_class_curie: ClassVar[str] = "kitchen_sink_api:LocalQuery"
    class_name: ClassVar[str] = "LocalQuery"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.LocalQuery

    target_class: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.target_class is not None and not isinstance(self.target_class, str):
            self.target_class = str(self.target_class)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class AddPerson(YAMLRoot):
    """
    A change action that adds a Person to a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.AddPerson
    class_class_curie: ClassVar[str] = "kitchen_sink_api:AddPerson"
    class_name: ClassVar[str] = "AddPerson"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.AddPerson

    value: Optional[Union[dict, Person]] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, Person):
            self.value = Person(**as_dict(self.value))

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class RemovePerson(YAMLRoot):
    """
    A change action that remoaves a Person to a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.RemovePerson
    class_class_curie: ClassVar[str] = "kitchen_sink_api:RemovePerson"
    class_name: ClassVar[str] = "RemovePerson"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.RemovePerson

    value: Optional[Union[dict, Person]] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, Person):
            self.value = Person(**as_dict(self.value))

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class PersonQuery(YAMLRoot):
    """
    A query object for instances of Person from a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.PersonQuery
    class_class_curie: ClassVar[str] = "kitchen_sink_api:PersonQuery"
    class_name: ClassVar[str] = "PersonQuery"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.PersonQuery

    constraints: Optional[Union[dict, Any]] = None
    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class PersonFetchById(YAMLRoot):
    """
    A query object for fetching an instance of Person from a database by id
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.PersonFetchById
    class_class_curie: ClassVar[str] = "kitchen_sink_api:PersonFetchById"
    class_name: ClassVar[str] = "PersonFetchById"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.PersonFetchById

    id_value: Optional[str] = None
    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id_value is not None and not isinstance(self.id_value, str):
            self.id_value = str(self.id_value)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class AddCompany(YAMLRoot):
    """
    A change action that adds a Company to a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.AddCompany
    class_class_curie: ClassVar[str] = "kitchen_sink_api:AddCompany"
    class_name: ClassVar[str] = "AddCompany"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.AddCompany

    value: Optional[Union[dict, Company]] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, Company):
            self.value = Company(**as_dict(self.value))

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class RemoveCompany(YAMLRoot):
    """
    A change action that remoaves a Company to a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.RemoveCompany
    class_class_curie: ClassVar[str] = "kitchen_sink_api:RemoveCompany"
    class_name: ClassVar[str] = "RemoveCompany"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.RemoveCompany

    value: Optional[Union[dict, Company]] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, Company):
            self.value = Company(**as_dict(self.value))

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class CompanyQuery(YAMLRoot):
    """
    A query object for instances of Company from a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.CompanyQuery
    class_class_curie: ClassVar[str] = "kitchen_sink_api:CompanyQuery"
    class_name: ClassVar[str] = "CompanyQuery"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.CompanyQuery

    constraints: Optional[Union[dict, Any]] = None
    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class CompanyFetchById(YAMLRoot):
    """
    A query object for fetching an instance of Company from a database by id
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.CompanyFetchById
    class_class_curie: ClassVar[str] = "kitchen_sink_api:CompanyFetchById"
    class_name: ClassVar[str] = "CompanyFetchById"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.CompanyFetchById

    id_value: Optional[str] = None
    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id_value is not None and not isinstance(self.id_value, str):
            self.id_value = str(self.id_value)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class AddActivity(YAMLRoot):
    """
    A change action that adds a Activity to a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.AddActivity
    class_class_curie: ClassVar[str] = "kitchen_sink_api:AddActivity"
    class_name: ClassVar[str] = "AddActivity"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.AddActivity

    value: Optional[Union[dict, Activity]] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, Activity):
            self.value = Activity(**as_dict(self.value))

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class RemoveActivity(YAMLRoot):
    """
    A change action that remoaves a Activity to a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.RemoveActivity
    class_class_curie: ClassVar[str] = "kitchen_sink_api:RemoveActivity"
    class_name: ClassVar[str] = "RemoveActivity"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.RemoveActivity

    value: Optional[Union[dict, Activity]] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, Activity):
            self.value = Activity(**as_dict(self.value))

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class ActivityQuery(YAMLRoot):
    """
    A query object for instances of Activity from a database
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.ActivityQuery
    class_class_curie: ClassVar[str] = "kitchen_sink_api:ActivityQuery"
    class_name: ClassVar[str] = "ActivityQuery"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.ActivityQuery

    constraints: Optional[Union[dict, Any]] = None
    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


@dataclass
class ActivityFetchById(YAMLRoot):
    """
    A query object for fetching an instance of Activity from a database by id
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = KITCHEN_SINK_API.ActivityFetchById
    class_class_curie: ClassVar[str] = "kitchen_sink_api:ActivityFetchById"
    class_name: ClassVar[str] = "ActivityFetchById"
    class_model_uri: ClassVar[URIRef] = KITCHEN_SINK_API.ActivityFetchById

    id_value: Optional[str] = None
    value: Optional[str] = None
    path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id_value is not None and not isinstance(self.id_value, str):
            self.id_value = str(self.id_value)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)


# Enumerations


# Slots

