test:
	tox

package:
	python setup.py bdist_wheel --universal

publish:
	bumpversion patch
	rm -rf dist
	python setup.py bdist_wheel --universal
	twine upload dist/*
