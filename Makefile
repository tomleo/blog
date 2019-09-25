sdist:
	python setup.py sdist bdist_wheel

.PHONY: sdist

upload:
	twine upload --skip-existing dist/*

.PHONY: upload
