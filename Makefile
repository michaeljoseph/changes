.DEFAULT_GOAL := help

.PHONY: test
test: ## Run tests
	@echo "+ $@"
	pytest

.PHONY: lint
lint: ## Lint source
	@echo "+ $@"
	flake8 --ignore=E501 changes tests setup.py

.PHONY: ci
ci: test lint ## Continuous Integration Commands

.PHONY: docs
docs: ## Generate documentation site
	@echo "+ $@"
	@$(MAKE) -C docs clean
	@$(MAKE) -C docs singlehtml
	@echo "> Documentation generated in docs/_build/singlehtml/index.html"

.PHONY: watch
watch: ## Run tests continuously on filesystem changes
	@echo "+ $@"
	ptw

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
