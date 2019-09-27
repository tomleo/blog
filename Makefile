build:
	python setup.py sdist bdist_wheel

.PHONY: build

upload:
	twine upload --skip-existing -s -i tomjleo@gmail.com dist/*

.PHONY: upload

update:
	pip install pip-tools
	pip-compile -o requirements.txt requirements.in

.PHONY: update

test:
	pytest --cov=blog tests/
	coverage html

.PHONY: test
