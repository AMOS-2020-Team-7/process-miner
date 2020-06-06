
.PHONY: all setup-env setup-dev-env test lint security-check check run run-main run-backend

MODULE_DIR=process_miner
TEST_DIR=tests

all: setup-dev-env check run

setup-env:
	pip install pipenv
	pipenv install

setup-dev-env: setup-env
	pipenv install --dev

test:
	pipenv run pytest

lint:
	pipenv run pylint $(MODULE_DIR) $(TEST_DIR)

security-check:
	pipenv run bandit -r $(MODULE_DIR)

check: test lint security-check

run: run-backend

run-main:
	pipenv run python -m process_miner

run-backend:
	FLASK_APP=$(MODULE_DIR) pipenv run flask run
