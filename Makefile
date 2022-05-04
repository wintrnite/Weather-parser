.DEFAULT_GOAL := help
PYTHONPATH = PYTHONPATH=./
TEST = pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg) -k "$(k)"
CODE = weather tests

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Runs pytest with coverage
	$(TEST) --cov

.PHONY: test-fast
test-fast: ## Runs pytest with exitfirst
	$(TEST) --exitfirst

.PHONY: test-failed
test-failed: ## Runs pytest from last-failed
	$(TEST) --last-failed

.PHONY: test-cov
test-cov: ## Runs pytest with coverage report
	$(TEST) --cov --cov-report html

.PHONY: lint
lint: ## Lint code
	flake8 --jobs 4 --statistics --show-source $(CODE)
	pylint --rcfile=setup.cfg $(CODE)
	mypy $(CODE)
	black --line-length 100 --target-version py39 --skip-string-normalization --check $(CODE)
	pytest --dead-fixtures --dup-fixtures
	safety check --full-report

.PHONY: format
format: ## Formats all files
	autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	isort $(CODE)
	black --line-length 100 --target-version py39 --skip-string-normalization $(CODE)
	unify --in-place --recursive $(CODE)

.PHONY: check
check: format lint test ## Format and lint code then run tests

.PHONY: bump-major
bump-major: ## Change version 1.x.x
	poetry version major

.PHONY: bump-minor
bump-minor: ## Change version x.1.x
	poetry version minor

.PHONY: bump-patch
bump-patch: ## Change version x.x.1
	poetry version patch

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-ansi
