# Check if poetry is available
ifeq (,$(shell which poetry))
$(error "please install poetry")
endif


ROOT := $(shell pwd)
VENV_ROOT := $(ROOT)/.venv
BIN := $(VENV_ROOT)/bin
py := $(BIN)/python
flake8 := $(BIN)/flake8
black := $(BIN)/black
isort := $(BIN)/isort
pytest := $(BIN)/pytest



all-tests: lint tests
	@echo "===================="
	@echo All Good
	@echo "===================="


poetry:
	poetry config virtualenvs.create true --local
	poetry config virtualenvs.in-project true --local
	VIRTUAL_ENV=$(VENV_ROOT) poetry install --no-root -vv

$(py): poetry

$(flake8): poetry

$(isort): poetry

$(black): poetry

$(pytest): poetry

flake8-checks: $(flake8)
	$(flake8) --count --statistics

black-checks: $(black)
	$(black) --check src

isort-checks: $(isort)
	$(isort) --check --diff src

tests: $(pytest)
	ENVIRONMENT=testing $(pytest) --cache-clear

lint: black-checks isort-checks flake8-checks




