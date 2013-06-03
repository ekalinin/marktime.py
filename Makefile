
env:
	@rm -rf env && virtualenv env && . env/bin/activate && pip install -r requirements.txt

test:
	@. env/bin/activate && nosetests --with-coverage --cover-erase --cover-package=timerit
