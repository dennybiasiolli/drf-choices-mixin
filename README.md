# django-rest-choices

A Django REST Framework mixin that automatically generates API endpoints for
model field choices.

Drop `ChoicesMixin` into any DRF viewset and it will expose every field that
defines `choices` through two list-level endpoints — no manual serializer or
view code required.

## Installation

```bash
pip install django-rest-choices
```

## Quick start

Given a model with choices:

```python
from django.db import models


class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class Task(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices)
```

Add the mixin to your viewset (place it **before** the base viewset class):

```python
from django_rest_choices import ChoicesMixin
from rest_framework.viewsets import ModelViewSet


class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Register the viewset with a router as usual:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tasks", TaskViewSet)
```

Two new endpoints are now available:

| Endpoint | Description |
|---|---|
| `GET /tasks/choices/` | All choices for every field |
| `GET /tasks/choices/{field_name}/` | Choices for a single field |

## Response format

**All choices** — `GET /tasks/choices/`

```json
{
  "status": [
    {"value": "active", "display": "Active"},
    {"value": "inactive", "display": "Inactive"}
  ]
}
```

**Single field** — `GET /tasks/choices/status/`

```json
[
  {"value": "active", "display": "Active"},
  {"value": "inactive", "display": "Inactive"}
]
```

Requesting a field that does not exist or has no choices returns **404**.

## Features

- Works with `TextChoices`, `IntegerChoices`, and plain tuples.
- Grouped choices are automatically flattened.
- Zero configuration — just add the mixin.

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Lint & format
uv run ruff check .
uv run ruff format .
```

## Credits

This project was built with the assistance of [Grok](https://x.ai/grok), an AI model by [xAI](https://x.ai).

## License

MIT