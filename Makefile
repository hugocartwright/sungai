clean:
	rm -rf .tox sungai.egg-info .coverage dist build
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

install:
	pip install -r requirements-dev.txt --no-cache-dir
	pre-commit install

lint:
	pre-commit run --all-files

test:
	coverage run -m unittest discover
	coverage report -m
	tox -e py

build:
	python setup.py sdist bdist_wheel

deploy_pypi:
	twine upload dist/*

bump_version:
	bumpver update --patch
