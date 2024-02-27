RUN = poetry run

test:
	$(RUN) python -m unittest discover -p 'test_*.py'

prep_tests: tests/model/kitchen_sink_api.yaml

%_api.yaml: %.yaml
	$(RUN) gen-api-datamodel --container-class Dataset $< > $@.tmp && mv $@.tmp $@

# requires dev
%_api.py: %_api.yaml
	gen-python --no-mergeimports $< > $@.tmp && mv $@.tmp $@

%_model.py: %.yaml
	$(RUN) gen-python --no-mergeimports $< > $@.tmp && mv $@.tmp $@

