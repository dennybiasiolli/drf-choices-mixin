.PHONY: install test lint format docs docs-serve build publish publish-test clean

install:
	uv sync --group dev

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

docs:
	uv run --group docs mkdocs build --strict

docs-serve:
	uv run --group docs mkdocs serve

clean:
	rm -rf dist/ site/

build: clean
	uv build

publish: build
	uv publish

publish-test: build
	uv publish --publish-url https://test.pypi.org/simple/