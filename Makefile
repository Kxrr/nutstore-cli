clean:
	rm -rf dist/ build/ nutstore_cli.egg-info/ test_venv/

bdist:
	python setup.py build sdist bdist_wheel bdist_egg

install-from-source:
	pip install `find dist | grep tar\.gz` --process-dependency-links

create-test-venv:
	virtualenv test_venv

test-install: clean bdist create-test-venv install-from-source execute
