import os

METAMODEL_CONTEXT_URI = "https://w3id.org/linkml/meta.context.jsonld"
META_BASE_URI = "https://w3id.org/linkml/"

TESTING_DIR = os.path.abspath(os.path.dirname(__file__))

INPUT_DIR = os.path.join(TESTING_DIR, 'input')
MODEL_DIR = os.path.join(TESTING_DIR, 'model')
OUTPUT_DIR = os.path.join(TESTING_DIR, 'output')
