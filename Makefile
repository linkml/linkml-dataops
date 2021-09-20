test:
	pipenv run python -m unittest discover -p 'test_*.py'

prep_tests: tests/model/kitchen_sink_api.yaml

%_api.yaml: %.yaml
	pipenv run gen-api --container-class Dataset $< > $@.tmp && mv $@.tmp $@
