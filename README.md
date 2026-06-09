# django-rest-choices

A Django REST Framework mixin that automatically generates API endpoints for
model field choices. Drop `ChoicesMixin` into any DRF viewset and it will
expose every field that defines `choices` through list-level endpoints — no
manual serializer or view code required.

## Features

- **Zero configuration** — add the mixin and endpoints appear automatically.
- **Fully configurable** — customize endpoint names, URL structure, exposed fields, and response format.
- **Works with all choice types** — `TextChoices`, `IntegerChoices`, plain tuples, and grouped choices.
- **Two endpoints per viewset** — one for all choices, one for a specific field.

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


class Priority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"


class Task(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices)
    priority = models.IntegerField(choices=Priority.choices)
    description = models.TextField()
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
| `GET /tasks/choices/{field_name}/` | Choices for a specific field |

### Response examples

**All choices** — `GET /tasks/choices/`

```json
{
  "status": [
    {"value": "active", "display": "Active"},
    {"value": "inactive", "display": "Inactive"}
  ],
  "priority": [
    {"value": 1, "display": "Low"},
    {"value": 2, "display": "Medium"},
    {"value": 3, "display": "High"}
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

Requesting a field that has no choices or does not exist returns a **404**:

```json
{"detail": "Field 'title' does not have choices."}
```

## Configuration

All configuration is done through class attributes on the viewset. Every
option has a sensible default, so none of them are required.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `choices_endpoint_name` | `str` | `"choices"` | URL segment used for both endpoints |
| `choices_field_first` | `bool` | `False` | Put the field name before the endpoint segment in URLs |
| `choices_fields` | `list[str] \| None` | `None` | Restrict which fields are exposed (`None` = all) |
| `choices_value_key` | `str` | `"value"` | Key name for the choice value in the response |
| `choices_display_key` | `str` | `"display"` | Key name for the display text in the response |

### Custom endpoint name

Rename the URL segment to avoid conflicts with other actions or to match your
API conventions:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"
```

This changes the endpoints to:

| Before | After |
|---|---|
| `GET /tasks/choices/` | `GET /tasks/options/` |
| `GET /tasks/choices/status/` | `GET /tasks/options/status/` |

### URL order — field-first mode

By default the endpoint name comes first (`/choices/status/`). Set
`choices_field_first = True` to invert the order, which can read more
naturally in some APIs:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_field_first = True
```

| Default | Field-first |
|---|---|
| `GET /tasks/choices/status/` | `GET /tasks/status/choices/` |

The all-choices endpoint stays the same (`GET /tasks/choices/`).

Both options can be combined:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"
    choices_field_first = True
```

| Endpoint | Description |
|---|---|
| `GET /tasks/options/` | All choices |
| `GET /tasks/status/options/` | Choices for the `status` field |

### Field filtering

By default every field with choices is exposed. Use `choices_fields` to
restrict the output to a specific subset:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_fields = ["status"]
```

`GET /tasks/choices/` now returns only the `status` field:

```json
{
  "status": [
    {"value": "active", "display": "Active"},
    {"value": "inactive", "display": "Inactive"}
  ]
}
```

Fields not in the list return **404** when accessed directly
(`GET /tasks/choices/priority/` → 404).

### Custom response keys

If your frontend expects different key names, override `choices_value_key`
and `choices_display_key`:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_value_key = "key"
    choices_display_key = "label"
```

`GET /tasks/choices/status/` now returns:

```json
[
  {"key": "active", "label": "Active"},
  {"key": "inactive", "label": "Inactive"}
]
```

### Full example

All options together:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"
    choices_field_first = True
    choices_fields = ["status", "priority"]
    choices_value_key = "id"
    choices_display_key = "text"
```

| Endpoint | Response |
|---|---|
| `GET /tasks/options/` | `{"status": [{"id": "active", "text": "Active"}, ...], "priority": [...]}` |
| `GET /tasks/status/options/` | `[{"id": "active", "text": "Active"}, ...]` |
| `GET /tasks/description/options/` | `404` |

## Supported choice formats

The mixin works with every way Django lets you define choices:

**`TextChoices` / `IntegerChoices` enums** (Django 3.0+):

```python
class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

status = models.CharField(choices=Status.choices)
```

**Plain tuples**:

```python
status = models.CharField(choices=[("active", "Active"), ("inactive", "Inactive")])
```

**Grouped choices** (automatically flattened):

```python
COLOR_CHOICES = [
    ("Warm", [("red", "Red"), ("orange", "Orange")]),
    ("Cool", [("blue", "Blue"), ("green", "Green")]),
]
color = models.CharField(choices=COLOR_CHOICES)
```

Response for grouped choices:

```json
[
  {"value": "red", "display": "Red"},
  {"value": "orange", "display": "Orange"},
  {"value": "blue", "display": "Blue"},
  {"value": "green", "display": "Green"}
]
```

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Lint & format
uv run ruff check .
uv run ruff format .

# Build documentation locally
uv sync --group docs
uv run mkdocs serve
```

## Credits

This project was built with the assistance of [Grok](https://x.ai/grok), an AI model by [xAI](https://x.ai).

## License

MIT