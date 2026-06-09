# Contributing to drf-choices-mixin

Thank you for your interest in contributing! This guide will help you get
started, whether you're reporting a bug, suggesting a feature, or submitting
code.

## Code of conduct

Be respectful and constructive. We are committed to providing a welcoming and
inclusive experience for everyone. Harassment, discrimination, and
disrespectful behavior will not be tolerated. In short: be kind, assume good
intent, and focus on the work.

## Reporting bugs

Open a [GitHub issue](https://github.com/dennybiasiolli/drf-choices-mixin/issues/new) with:

1. A clear, descriptive title.
2. Steps to reproduce the problem.
3. What you expected to happen vs. what actually happened.
4. Your environment — Python version, Django version, DRF version.

A minimal code snippet that reproduces the issue is extremely helpful.

## Suggesting features

Open a [GitHub issue](https://github.com/dennybiasiolli/drf-choices-mixin/issues/new) describing:

1. The problem you're trying to solve.
2. Your proposed solution (if you have one).
3. Any alternatives you considered.

We value simple, focused features that benefit the majority of users.

## Development setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Getting started

```bash
# Clone the repository
git clone https://github.com/dennybiasiolli/drf-choices-mixin.git
cd drf-choices-mixin

# Install all dependencies (dev + docs)
uv sync --group dev --group docs

# Verify everything works
uv run pytest
uv run ruff check .
```

### Project layout

```
src/drf_choices_mixin/     # Package source
    __init__.py             # Public API (exports ChoicesMixin)
    mixins.py               # Mixin implementation
tests/                      # Test suite
    conftest.py             # Django/DRF test configuration
    models.py               # Test models
    serializers.py          # Test serializers
    views.py                # Test viewsets
    urls.py                 # Test URL routing
    test_mixins.py          # Tests
docs/                       # MkDocs documentation source
```

## Submitting a pull request

### 1. Create a branch

```bash
git checkout -b your-branch-name
```

Use a descriptive branch name like `fix/404-response-format` or
`feature/exclude-fields`.

### 2. Make your changes

- Keep changes focused — one logical change per PR.
- Follow the coding standards described below.
- Add or update tests to cover your changes.
- Update documentation if you changed behavior or added features.

### 3. Validate locally

Every PR must pass these checks:

```bash
# Run the test suite
uv run pytest

# Lint
uv run ruff check .

# Format check
uv run ruff format --check .
```

Fix any formatting issues automatically with:

```bash
uv run ruff format .
```

### 4. Write a clear commit message

Use a short, imperative subject line followed by a blank line and an
optional body explaining *why* (not *what*):

```
Add choices_exclude_fields configuration option

Allows users to exclude specific fields from the choices endpoints
without having to list every included field explicitly.
```

### 5. Open the pull request

- Fill in the PR description with what changed and why.
- Link any related issues (e.g. "Closes #12").
- Keep the PR small and reviewable — large PRs are harder to review and
  more likely to need rework.

## Coding standards

### Style

- **Formatter/linter:** [Ruff](https://docs.astral.sh/ruff/) with a
  line length of 88 characters.
- **Lint rules:** `E`, `F`, `I`, `W` (pycodestyle, pyflakes, isort,
  warnings).
- **Imports:** sorted by isort rules (handled by Ruff).

### Code guidelines

- Write simple, readable code. Clarity over cleverness.
- Use docstrings for public methods and classes.
- Use comments sparingly — only for non-obvious logic.
- Choose descriptive variable and function names.
- Prefer early returns over nested conditions.
- Don't add abstractions for things that are only used once.

### Tests

- Every new feature or bug fix must include tests.
- Tests live in `tests/test_mixins.py`.
- Use `pytest` with `@pytest.mark.django_db` for tests that hit the
  database.
- Test both the happy path and error cases (e.g. 404 responses).
- Keep tests focused — one assertion per concept.

### Documentation

- Update the README if you add or change public configuration options.
- Update the MkDocs pages under `docs/` for detailed documentation.
- Build the docs locally to verify they render correctly:

```bash
uv run mkdocs serve
```

## License

By contributing, you agree that your contributions will be licensed under
the project's [MIT License](LICENSE).