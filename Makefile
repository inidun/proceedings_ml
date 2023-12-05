SHELL := /bin/bash

SOURCE_FOLDERS := proceedings_ml tests

NLP := "en_core_web_lg"
DATASET := "proceedings_spans"
WORKDIR := $(shell pwd)/data/proceedings
MODELDIR := $(shell pwd)/models
TRAINDIR := $(shell pwd)/training
SOURCE := $(WORKDIR)/proceedings.jsonl
PATTERN_FILE := $(WORKDIR)/patterns.jsonl
LABELS := "NAME,HEADER,PARAGRAPH_NUMBER,ROLE,TITLE,COUNTRY,TRANSLATED_NOTE"

clean:
	@rm -rf .coverage coverage.xml htmlcov .nox
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@rm -rf tests/output
.PHONY: clean

isort:
	@poetry run isort $(SOURCE_FOLDERS)
.PHONY: isort

black:
	@poetry run black $(SOURCE_FOLDERS) -q
.PHONY: black

tidy: isort black
.PHONY: tidy

pylint:
	@poetry run pylint $(SOURCE_FOLDERS)
.PHONY: pylint

notes:
	@poetry run pylint --notes=FIXME,XXX,TODO --disable=all --enable=W0511 -f colorized $(SOURCE_FOLDERS)
.PHONY: notes

mypy:
	@poetry run mypy $(SOURCE_FOLDERS)
.PHONY: mypy

lint: tidy pylint
.PHONY: lint

typing: lint mypy
.PHONY: typing

test:
	@pytest tests
.PHONY: test

spacy-model:
	@poetry run python -m spacy download $(NLP)
	@poetry run python -m spacy validate

setup: spacy-model
.PHONY: setup

spans.manual:
	@( cd $(WORKDIR); poetry run prodigy spans.manual $(DATASET) $(NLP) $(SOURCE) --label $(LABELS) --patterns $(PATTERN_FILE) )
.PHONY: spans.manual

export_annotations:
	@( cd $(WORKDIR); poetry run prodigy db-out $(DATASET) > $(WORKDIR)/$(DATASET)_annotations.jsonl )
.PHONY: export_annotations

training_dir:
	@mkdir -p $(TRAINDIR)

train_spancat: training_dir
	@( cd $(WORKDIR); poetry run prodigy train $(TRAINDIR) --spancat $(DATASET) --eval-split 0.2 --lang en --label-stats )
.PHONY: train_spancat

prodigy_help:
	@poetry run prodigy $(RECIPE) --help
.PHONY: prodigy_help

prodigy_info:
	@poetry run prodigy stats $(DATASET)
.PHONY: prodigy_info
