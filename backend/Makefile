
.PHONY: all setup-env setup-dev-env test lint security-check check run run-main run-backend run-dev-backend

MODULE_DIR=process_miner
TEST_DIR=tests
SOURCES = $(shell find $(TEST_DIR) $(MODULE_DIR) -name '*.py')

all: setup-dev-env check run

setup-env:
	pip install pipenv
	pipenv install

setup-dev-env: setup-env
	pipenv install --dev

test:
	pipenv run pytest --cov=$(MODULE_DIR) --cov-fail-under=50 --cov-report term-missing

lint:
	pipenv run pylint $(SOURCES)

security-check:
	pipenv run bandit -r $(MODULE_DIR)

check: test lint security-check

run: run-backend

run-main:
	pipenv run python -m $(MODULE_DIR)

run-backend:
	FLASK_APP=$(MODULE_DIR) pipenv run flask run

run-dev-backend:
	FLASK_APP=$(MODULE_DIR) FLASK_ENV=development pipenv run flask run
