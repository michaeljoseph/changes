VENV = venv/bin

.DEFAULT_GOAL := help

.PHONY: clean venv help
clean: ## Remove Python file artifacts and virtualenv
	@rm -rf venv

venv: ## Creates the virtualenv and installs requirements
	python -m venv venv
	$(VENV)/pip install tox

test:venv ## Run tests
	$(VENV)/tox -qe test

lint:venv ## Lint source
	$(VENV)/tox -qe lint

ci:test lint ## Continuous Integration Commands

docs:venv ## Generate documentation site
	$(VENV)/tox -qe docs

serve:venv ## Serve documentation site
	@cp test-reports/test-report.html site/
	@cp -R test-reports/coverage_html site/coverage
	$(VENV)/tox -qe docs -- serve

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
