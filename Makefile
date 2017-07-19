clean:
	rm -rf dist/ build/ nutstore_cli.egg-info/ test_venv/

bdist:
	python setup.py build sdist bdist_wheel bdist_egg

testenv:
	docker-compose run testenv

testinstall-local:
	docker-compose run testenv bash -c 'cd /dist && pip install `find . | grep 'tar.gz' | grep -v macos` --process-dependency-links && bash'



test-install: clean bdist create-test-venv install-from-source execute
