PKG := "ub_image_converter_api"

.PHONY: venv devs deps fmt lint docs

venv:
	python -m venv venv && echo "Remember to activate your virtual environment!!"

devs:
	pip install -r requirements-dev.txt

deps:
	pip install -r requirements.txt

chkfmt:
	black --diff -l 100 -v $(PKG)

fmt:
	black -l 100 -v $(PKG)

lint:
	pylint --generated-members=cv $(PKG)

docs:
	mkdir -p docs; pdoc3 --force --html -o docs $(PKG)

test:
	python -m pytest
