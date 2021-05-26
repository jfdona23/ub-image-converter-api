PKG := "ub-image-converter-api"

venv:
	python -m venv venv && echo "Remember to activate your virtual environment!!"

devs:
	pip install -r requirements-dev.txt

deps:
	pip install -r requirements.txt

fmt:
	black -v $(PKG)

lint:
	pylint --generated-members=cv $(PKG)

docs:
	mkdir -p docs; pdoc3 --force --html -o docs .
