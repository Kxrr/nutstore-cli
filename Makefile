clean:
	rm -rf dist/ build/ nutstore_cli.egg-info/ test_venv/

_bdist:
	python setup.py build sdist bdist_wheel bdist_egg

bdist: clean _bdist

testenv:
	docker-compose run testenv

_testInstallLocal:
	docker-compose run testenv bash -c 'cd /dist && pip install `find . | grep 'tar.gz' | grep -v macos` && bash'

testInstallLocal: clean _bdist _testInstallLocal

testInstallFromTestPypi:
	docker-compose run testenv bash -c 'pip install nutstore-cli -i https://testpypi.python.org/pypi'

releaseToTestPypi:
	python setup.py bdist_wheel upload -r testpypi
