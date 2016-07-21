test:
	nosetests -s --stop -v ./tests

test-coverage:
	nosetests -s  --stop -v -a '!slow' --with-coverage --cover-erase --cover-branches --cover-html --cover-html-dir=cover ./tests
