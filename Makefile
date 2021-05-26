.PHONY: venv devs deps fmt lint docs

venv:
	python -m venv venv && echo "Remember to activate your virtual environment!!"

devs:
	pip install -r requirements-dev.txt

deps:
	pip install -r requirements.txt

fmt:
	black -v .

lint:
	pylint --generated-members=cv .

docs:
	mkdir -p docs; pdoc3 --force --html -o docs .
