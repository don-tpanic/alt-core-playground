.PHONY: lint lint-check test test-cov

# Format code and fix linting issues
lint:
	black .
	ruff check --fix .
	mypy src

# Check code without fixing (used in CI)
lint-check:
	black . --check
	ruff check .
	mypy src

# Run tests
test:
	pytest 

# Run tests with coverage report
test-cov:
	pytest --cov=src --cov-report=term-missing --cov-report=xml