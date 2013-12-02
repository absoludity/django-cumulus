PWD := $(shell pwd)
TEST_SETTINGS := example.settings.test


install-dependencies: dev-virtualenv
	$(PWD)/dev-virtualenv/bin/pip install --requirement requirements.txt


dev-virtualenv:
	/usr/bin/virtualenv dev-virtualenv


test:
	DJANGO_SETTINGS_MODULE=$(TEST_SETTINGS) $(PWD)/dev-virtualenv/bin/nosetests cumulus.tests.test_utils


.PHONY: dependencies
