# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.1] - 2025-06-10

### Added

- `__version__` attribute for programmatic version access.
- Python 3.14 to CI test matrix and package classifiers.
- Expanded ruff lint rules: bugbear (`B`), bandit (`S`), pyupgrade (`UP`),
  simplify (`SIM`), and ruff-specific (`RUF`).
- `SECRET_KEY` in test Django settings to prevent future
  `ImproperlyConfigured` errors.

### Changed

- Use `status.HTTP_404_NOT_FOUND` constant instead of bare `404` integer.
- Docs workflow now uses `uv sync --group docs` instead of unpinned
  `pip install`, matching the CI workflow and respecting the lockfile.
- Docs `conf.py` reads version from package metadata instead of hardcoding
  it, keeping `pyproject.toml` as the single source of truth.
- Dependabot ecosystem changed from `pip` to `uv`.

### Security

- CI workflow restricted to `permissions: contents: read`.
- Docs workflow pinned to lockfile, eliminating supply-chain risk from
  unpinned `pip install`.

## [0.1.0] - 2025-06-09

### Added

- Initial release of `drf-choices-mixin`.
- `ChoicesMixin` for DRF viewsets with automatic choices endpoints.
- Support for `TextChoices`, `IntegerChoices`, plain tuples, and grouped
  choices.
- Configurable endpoint names (`choices_endpoint_name`).
- Field-first URL mode (`choices_field_first`).
- Field filtering (`choices_fields`).
- Custom response keys (`choices_value_key`, `choices_display_key`).
- Sphinx documentation with furo theme.
- CI with GitHub Actions (lint + test matrix for Python 3.10–3.13).
- Dependabot for dependency updates.

[0.1.1]: https://github.com/dennybiasiolli/drf-choices-mixin/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dennybiasiolli/drf-choices-mixin/releases/tag/v0.1.0