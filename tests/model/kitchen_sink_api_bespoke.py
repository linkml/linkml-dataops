import logging
from dataclasses import dataclass
from linkml_runtime_api.query.query_model import FetchQuery, Constraint, MatchConstraint, OrConstraint, AbstractQuery, \
    FetchById
from linkml_runtime_api.query.queryengine import MatchExpression, QueryEngine

from tests.model.kitchen_sink import *

@dataclass
class KitchenSinkAPI:

    query_engine: QueryEngine = None

    def fetch_Person(self, id_value: str) -> Person:
        """
        Retrieves an instance of `Person` via a primary key

        :param id_value:
        :return: Person with matching ID
        """
        q = FetchById(id=id_value, target_class=Person.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Person(self,
                     id: Union[str, MatchExpression] = None,
                     name: Union[str, MatchExpression] = None,
                     age_in_years: Union[int, MatchExpression] = None) -> List[Person]:
        """
        Queries for instances of `Person`

        :param id:
        :param name:
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Person.class_name,
                                                 id=id,
                                                 name=name,
                                                 age_in_years=age_in_years)
        return results

