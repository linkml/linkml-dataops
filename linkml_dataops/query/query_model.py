# Auto generated from query.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-19 01:06
# Schema: query
#
# id: https://w3id.org/linkml/query
# description: A generic datamodel for representing query
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
from linkml_runtime.linkml_model.types import Boolean, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
QUERY = CurieNamespace('query', 'https://w3id.org/linkml/query')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
STRING = CurieNamespace('string', 'http://example.org/UNKNOWN/string/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = QUERY


# Types
class PathExpression(str):
    """ A path expression conformant to [rfc6901](https://datatracker.ietf.org/doc/html/rfc6901) """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "PathExpression"
    type_model_uri = QUERY.PathExpression


# Class references



MyAny = Any

class AbstractQuery(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUERY.AbstractQuery
    class_class_curie: ClassVar[str] = "query:AbstractQuery"
    class_name: ClassVar[str] = "AbstractQuery"
    class_model_uri: ClassVar[URIRef] = QUERY.AbstractQuery


@dataclass
class FetchById(AbstractQuery):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUERY.FetchById
    class_class_curie: ClassVar[str] = "query:FetchById"
    class_name: ClassVar[str] = "FetchById"
    class_model_uri: ClassVar[URIRef] = QUERY.FetchById

    id: Optional[str] = None
    path: Optional[str] = None
    target_class: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        if self.target_class is not None and not isinstance(self.target_class, str):
            self.target_class = str(self.target_class)

        super().__post_init__(**kwargs)


@dataclass
class FetchQuery(AbstractQuery):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUERY.FetchQuery
    class_class_curie: ClassVar[str] = "query:FetchQuery"
    class_name: ClassVar[str] = "FetchQuery"
    class_model_uri: ClassVar[URIRef] = QUERY.FetchQuery

    constraints: Optional[Union[Union[dict, "Constraint"], List[Union[dict, "Constraint"]]]] = empty_list()
    path: Optional[str] = None
    target_class: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, Constraint) else Constraint(**as_dict(v)) for v in self.constraints]

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        if self.target_class is not None and not isinstance(self.target_class, str):
            self.target_class = str(self.target_class)

        super().__post_init__(**kwargs)


@dataclass
class Constraint(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUERY.Constraint
    class_class_curie: ClassVar[str] = "query:Constraint"
    class_name: ClassVar[str] = "Constraint"
    class_model_uri: ClassVar[URIRef] = QUERY.Constraint

    negated: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        super().__post_init__(**kwargs)


@dataclass
class MatchConstraint(Constraint):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUERY.MatchConstraint
    class_class_curie: ClassVar[str] = "query:MatchConstraint"
    class_name: ClassVar[str] = "MatchConstraint"
    class_model_uri: ClassVar[URIRef] = QUERY.MatchConstraint

    op: Optional[str] = None
    left: Optional[str] = None
    right: Optional[Union[dict, MyAny]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.op is not None and not isinstance(self.op, str):
            self.op = str(self.op)

        if self.left is not None and not isinstance(self.left, str):
            self.left = str(self.left)

        super().__post_init__(**kwargs)


@dataclass
class OrConstraint(Constraint):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = QUERY.OrConstraint
    class_class_curie: ClassVar[str] = "query:OrConstraint"
    class_name: ClassVar[str] = "OrConstraint"
    class_model_uri: ClassVar[URIRef] = QUERY.OrConstraint

    subconstraints: Optional[Union[Union[dict, Constraint], List[Union[dict, Constraint]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.subconstraints, list):
            self.subconstraints = [self.subconstraints] if self.subconstraints is not None else []
        self.subconstraints = [v if isinstance(v, Constraint) else Constraint(**as_dict(v)) for v in self.subconstraints]

        super().__post_init__(**kwargs)


# Enumerations


# Slots

