import re
import operator as op
from dataclasses import dataclass
from typing import Any

from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml_runtime_api.apiroot import ApiRoot
from linkml_runtime_api.query.query_model import FetchQuery, Constraint, MatchConstraint, OrConstraint, AbstractQuery, \
    FetchById
from linkml_runtime.utils.yamlutils import YAMLRoot


@dataclass
class MatchExpression:
    """
    A simple expression to be used in a constaint, e.g

    * `== 5`
    * `like "foo%"`
    """
    op: str
    right: Any

def create_match_constraint(left: str, right: Any, op: str = "==") -> MatchConstraint:
    if isinstance(right, MatchExpression):
        return MatchConstraint(left=left, op=right.op, right=right.right)
    else:
        return MatchConstraint(op=op, left=left, right=right)

@dataclass
class Database:
    """
    Abstraction over different datastores

    Currently only one supported
    """
    document: YAMLRoot = None

@dataclass
class QueryEngine(ApiRoot):
    """
    Abstract base class for QueryEngine objects for querying over a database

    Here a ref:`Database` can refer to:
    * in-memory object tree or JSON document
    * external database (SQL, Solr, Triplestore) -- to be implemented in future

    Currently one one implementation:
    * ref:`ObjectQueryEngine` -- query over in-memory objects

    future versions may include other implementations
    """

    database: Database = None

    # TODO: avoid repetion with same method
    def _get_path(self, query: AbstractQuery, strict=True) -> str:
        if query.path is not None:
            return query.path
        else:
            target_cn = query.target_class
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



