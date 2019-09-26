build:
	python setup.py sdist bdist_wheel

.PHONY: sdist

upload:
	twine upload --skip-existing dist/*

.PHONY: upload

update:
	pip install pip-tools
	pip-compile -o requirements.txt requirements.in

.PHONY: update
