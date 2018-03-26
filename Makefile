test:
	tox

package:
	python setup.py bdist_wheel --universal

publish:
	bumpversion patch
	python setup.py bdist_wheel --universal
	twine upload dist/*
