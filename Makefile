VENV = venv/bin

.DEFAULT_GOAL := help

.PHONY: clean
clean: ## Remove Python file artifacts and virtualenv
	@echo "+ $@"
	@rm -rf venv

venv: ## Creates the virtualenv and installs requirements
	python -m venv venv
	$(VENV)/pip install tox

test:venv ## Run tests
	@echo "+ $@"
	$(VENV)/tox -e py37

style:venv ## Style source
	@echo "+ $@"
	$(VENV)/tox -e style

lint:venv ## Lint source
	@echo "+ $@"
	$(VENV)/tox -e lint

ci:test lint ## Continuous Integration Commands

.PHONY: docs
docs: ## Generate documentation site
	@echo "+ $@"
	@$(MAKE) -C docs clean
	@$(MAKE) -C docs singlehtml
	@echo "> Documentation generated in docs/_build/singlehtml/index.html"

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
