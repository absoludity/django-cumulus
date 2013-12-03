PWD := $(shell pwd)
VENV_BIN := $(PWD)/virtualenv-dev/bin
PIP := $(VENV_BIN)/pip
PYTHON := $(VENV_BIN)/python
NOSETESTS := $(VENV_BIN)/nosetests
TEST_SETTINGS := example.settings.common
INTEGRATION_SETTINGS := example.settings.test

all: dev-dependencies test


dev-dependencies: virtualenv-dev
	$(PIP) install --requirement requirements-dev.txt


virtualenv-dev:
	/usr/bin/virtualenv virtualenv-dev


test:
	@DJANGO_SETTINGS_MODULE=$(TEST_SETTINGS) \
		PYTHONPATH=$(PWD) \
		$(NOSETESTS) --ignore-files=".*integration.*"


integration-dependencies: dev-dependencies
	@echo Installing additional dependencies to virtualenv-dev...
	@$(PIP) install --requirement requirements-integration.txt
	@echo Synching test database...
	@DJANGO_SETTINGS_MODULE=$(INTEGRATION_SETTINGS) \
		PYTHONPATH=$(PWD) \
		$(PYTHON) $(PWD)/example/manage_1_6.py syncdb --noinput


integration-test:
	@DJANGO_SETTINGS_MODULE=$(INTEGRATION_SETTINGS) \
		PYTHONPATH=$(PWD) \
		$(PWD)/virtualenv-dev/bin/nosetests --quiet --pdb \
		cumulus.tests.test_integration


.PHONY: dependencies
