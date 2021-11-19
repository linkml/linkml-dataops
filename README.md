# linkml-runtime-api

An extension to linkml-runtime to provide an API over runtime data objects.

Documentation will later be added in the main [linkml](https://linkml.io/linkml/) repo

This provides:

* The ability to *query* objects that instantiate linkml classes
* The ability to *change/patch* (apply changes to) objects that instantiate linkml classes

Additionally this provides hooks to allow both sets of operations over different *engines*

Current engines:

* in-memory object tree engine
* json-patcher engine

See [tests/](https://github.com/linkml/linkml-runtime-api/tree/main/tests) for examples

## Changes API

See linkml_runtime_api.changes

The ObjectChanger class provides an engine for applying generic changes to
linkml object trees loaded into memory.

Changes include:

* AddObject
* RemoveObject
* Append to a list of values  
* Rename (i.e. change the value of an identifier)

Example:

```python
# your datamodel here:
from kitchen_sink import Dataset, Person, FamilialRelationship

# setup - load schema
schemaview = SchemaView('kitchen_sink.yaml')

dataset = yaml_loader.load('my_dataset.yaml', target_class=Dataset)

# first create classes using your normal LinkML datamodel
person = Person(id='P:222',
                name='foo',
                has_familial_relationships=[FamilialRelationship(related_to='P:001',
                                                                 type='SIBLING_OF')])

changer = ObjectChanger(schemaview=schemaview)
change = AddObject(value=person)
changer.apply(change, dataset)
```

Currently there are two changer implementations:

* ObjectChanger
* JsonPatchChanger

Both operate on in-memory object trees. JsonPatchChanger uses JsonPatch objects as intermediates: these can be exposed and used on your source data documents in JSON

In future there will be other datastores

## Query API

See linkml_runtime_api.query

ObjectQueryEngine provides an engine for executing generic queries on in-memory object trees

Example:

```python
# your datamodel here:
from kitchen_sink import Dataset, Person, FamilialRelationship

# setup - load schema
schemaview = SchemaView('kitchen_sink.yaml')

dataset = yaml_loader.load('my_dataset.yaml', target_class=Dataset)


q = FetchQuery(target_class=Person.class_name,
                       constraints=[MatchConstraint(op='=',
                                                    left='has_medical_history/*/diagnosis/name',
                                                    right='headache')])
qe = ObjectQueryEngine(schemaview=schemaview)
persons = qe.fetch(q, dataset)
for person in persons:
  print(f'{person.id} {person.name}')
```

Currently there is only one Query api implemntation

* ObjectQuery

This operates on in-memory object trees.

In future there will be other datastores implemented (SQL, SPARQL, ...)

## Generating Domain APIs

The above examples use *generic* APIs that can be used with any data models. You can also generate *specific APIs* for your datamodel.

```
gen-python-api kitchen_sink.yaml > kitchen_sink_api.py
```

This will generate a query API:

```python
    # --
    # Person methods
    # --
    def fetch_Person(self, id_value: str) -> Person:
        """
        Retrieves an instance of `Person` via a primary key

        :param id_value:
        :return: Person with matching ID
        """
        ...

    def query_Person(self,
             has_employment_history: Union[str, MatchExpression] = None,
             has_familial_relationships: Union[str, MatchExpression] = None,
             has_medical_history: Union[str, MatchExpression] = None,
             age_in_years: Union[str, MatchExpression] = None,
             addresses: Union[str, MatchExpression] = None,
             has_birth_event: Union[str, MatchExpression] = None,
             metadata: Union[str, MatchExpression] = None,
             aliases: Union[str, MatchExpression] = None,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Person]:
        """
        ...
        """
        ...
```             

In future, change APIs will also be generated

The API is neutral with respect to the underlying datastore - each method is a wrapper for the generic runtime API

```python

# create query engine object
schemaview = SchemaView(MY_SCHEMA)
my_data = json_loader.load(MY_DATA, target_class=...)
engine = ObjectQueryEngine(schemaview=schemaview,
                           database=Database(my_data))

# create an API instance
ks_api = KitchenSinkAPI(engine)

# API calls below
...
```

