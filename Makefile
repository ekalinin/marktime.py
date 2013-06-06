
env27:
	@virtualenv env27 --python=python2.7 && . env27/bin/activate && pip install -r requirements.txt

env32:
	@virtualenv env32 --python=python3.2 && . env32/bin/activate && pip install -r requirements.txt

clear-env:
	@rm -rf env27
	@rm -rf env32

test: env27 env32
	@echo 'testing for python2.7'
	@. env27/bin/activate && nosetests --with-coverage --cover-erase --cover-package=marktime
	@echo 'testing for python3.2'
	@. env32/bin/activate && nosetests --with-coverage --cover-erase --cover-package=marktime

clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf marktime.egg-info/

release-github:
	git tag `grep "version =" marktime.py | grep -o -E '[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}'`
	git push --tags origin master

release-pypi:
	python setup.py sdist upload

update-pypi:
	python setup.py register

release: release-github release-pypi
