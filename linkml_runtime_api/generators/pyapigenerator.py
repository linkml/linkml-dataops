import logging
import re
import operator as op
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from typing import Any

import click
import yaml
from jinja2 import Template

from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime_api.apiroot import ApiRoot

jinja2_template = """
import logging
from dataclasses import dataclass
from linkml_runtime_api.query.queryengine import QueryEngine
from linkml_runtime_api.query.query_model import FetchQuery, Constraint, MatchConstraint, OrConstraint, AbstractQuery, \
    FetchById
from linkml_runtime_api.query.queryengine import MatchExpression

from {{ datamodel_package_full}} import *

@dataclass
class {{ api_name }}:

    # attributes
    query_engine: QueryEngine = None

    {% for cn in classes %}
    # --
    # {{cn}} methods
    # --
    def fetch_{{cn}}(self, id_value: str) -> {{cn}}:
        \"""
        Retrieves an instance of `{{cn}}` via a primary key

        :param id_value:
        :return: {{cn}} with matching ID
        \"""
        q = FetchById(id=id_value, target_class={{cn}}.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_{{cn}}(self,
             {% for s in slots[cn] -%}
             {{s.name}}: Union[{{s.range}}, MatchExpression] = None,
             {% endfor %}
             _extra: Any = None) -> List[{{cn}}]:
        \"""
        Queries for instances of `{{cn}}`

        {% for s in slots[cn] -%}
        :param {{s.name}}: {{s.description}}
        {% endfor %}
        :return: Person list matching constraints
        \"""
        results = self.query_engine.simple_query({{cn}}.class_name,
                                                 {% for s in slots[cn] %}
                                                 {{s.name}}={{s.name}},
                                                 {% endfor %}
                                                 _extra=_extra)
        return results
    {% endfor %}

"""

@dataclass
class PythonApiGenerator(ApiRoot):
    """
    Generates source for a Python API

    Implements the `Gateway <https://martinfowler.com/eaaCatalog/tableDataGateway.html>`_
    pattern.

    For example, given a schema KitchenSink, which includes a class Person,
    the generated API will be of the form

    .. code block:: python

      class KitchenSinkAPI:

        def fetch_Person(id_value: str) -> Person:
          ...
        def query_Person(id: str, name: str, ...) -> List[Person]:
          ...
    """

    def serialize(self, container_class=None, python_path=''):
        sv = self.schemaview
        cns = sv.all_class(imports=False).keys()
        if container_class != None:
            cns = self._get_top_level_classes(container_class)
        template_obj = Template(jinja2_template)
        datamodel_package_full = f'{python_path}.{sv.schema.name}'
        slots = defaultdict(list)
        classes = []
        for cn in cns:
            cn_cc = camelcase(cn)
            classes.append(cn_cc)
            islots = sv.class_induced_slots(cn)
            for s in islots:
                s.range = 'str' # TODO
                slots[cn_cc].append(s)
                s.name = underscore(s.name)
                logging.info(f'# Slot: {cn}.{s.name}')

        logging.info(f'# Classes: {list(classes)}')

        code = template_obj.render(datamodel_package_full=datamodel_package_full,
                                   api_name=f'{camelcase(sv.schema.name)}API',
                                   classes=classes,
                                   slots=slots
                                   )
        return str(code)

@click.command()
@click.option('-R', '--container-class', help="name of class that contains top level objects")
@click.argument('schema')
def cli(schema,  **args):
    """ Generate API """
    sv = SchemaView(schema)
    gen = PythonApiGenerator(schemaview=sv)
    print(gen.serialize(**args))


if __name__ == '__main__':
    cli()
