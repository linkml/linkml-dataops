import logging
import re
import operator as op
from dataclasses import dataclass
from typing import Any

from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml_runtime_api.query.query_model import FetchQuery, Constraint, MatchConstraint, OrConstraint, AbstractQuery, \
    FetchById
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml_runtime_api.query.queryengine import QueryEngine, create_match_constraint


def like(x: Any, y: Any) -> bool:
    y = str(y).replace('%', '.*')
    return re.match(f'^{y}$', str(x))

OPMAP = {'<': op.lt,
         '<=': op.le,
         '==': op.eq,
         '=': op.eq,
         '>=': op.ge,
         '>': op.gt,
         'like': like}


@dataclass
class ObjectQueryEngine(QueryEngine):
    """
    Engine for executing queries over an object tree

    """


    def fetch(self, query: AbstractQuery, element: YAMLRoot):
        if not isinstance(query, AbstractQuery):
            cn = type(query).class_name
            if cn.endswith('Query'):
                target_class = cn.replace('Query', '')
                query = FetchQuery(target_class=target_class,
                                   path=query.path,
                                   constraints=query.constraints)
            elif cn.endswith('FetchById'):
                target_class = cn.replace('FetchById', '')
                query = FetchById(target_class=target_class,
                                  path=query.path,
                                  id=query.id_value)
            else:
                raise Exception(f'Not supported: {cn}')
        if isinstance(query, FetchQuery):
            return self.fetch_by_query(query, element)
        elif isinstance(query, FetchById):
            return self.fetch_by_id(query, element)
        else:
            raise Exception(f'Unknown query type: {type(query)} for {query}')

    def fetch_by_id(self, query: FetchById, element: YAMLRoot = None):
        if element is None:
            element = self.database.document
        pk = None
        tc = query.target_class
        for cn, c in self.schemaview.all_class().items():
            if camelcase(cn) == camelcase(tc):
                pk = self.schemaview.get_identifier_slot(cn)
                break
        if pk is None:
            raise Exception(f'No primary key {cn}')
        c = MatchConstraint(op='=', left=pk.name, right=query.id)
        return self.fetch_by_query(FetchQuery(target_class=query.target_class,
                                              constraints=[c]),
                                   element)

    def fetch_by_query(self, query: FetchQuery, element: YAMLRoot = None):
        if element is None:
            element = self.database.document
        path = self._get_path(query)
        place = self.select_path(path, element)
        if isinstance(place, list):
            elts = place
        else:
            elts = place.values()
        results = []
        for e in elts:
            if self._satisfies(e, query):
                results.append(e)
        return results

    def simple_query(self, target_class: str, element: YAMLRoot = None, **kwargs):
        """
        Wrapper for `fetch_by_query`

        :param target_class:
        :param kwargs:
        :return:
        """
        constraints = [create_match_constraint(k, v) for k, v in kwargs.items()]
        q = FetchQuery(target_class=target_class, constraints=constraints)
        logging.info(f'Q={q}')
        return self.fetch_by_query(q, element=element)

    def _satisfies(self, element: YAMLRoot, query: FetchQuery):
        for c in query.constraints:
            if not self._satisfies_constraint(element, c):
                return False
        return True

    def _satisfies_constraint(self, element: YAMLRoot, constraint: Constraint):
        sat = self._satisfies_constraint_pos(element, constraint)
        if constraint.negated:
            return not sat
        else:
            return sat

    def _satisfies_constraint_pos(self, element: YAMLRoot, constraint: Constraint):
        if isinstance(constraint, MatchConstraint):
            constraint: MatchConstraint
            if constraint.right is None:
                # unspecified always matches
                return True
            for v in self._yield_path(constraint.left, element):
                py_op = OPMAP[constraint.op]
                sat = py_op(v, constraint.right)
                if sat:
                    return True
            return False
        elif isinstance(constraint, OrConstraint):
            constraint: OrConstraint
            for subc in constraint.subconstraints:
                if self._satisfies_constraint(element, subc):
                    return True
            return False
        else:
            raise Exception(f'Cannot handle {type(constraint)} yet')

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



