# Getting Started

## Installation

```bash
pip install django-rest-choices
```

Or with `uv`:

```bash
uv add django-rest-choices
```

No changes to `INSTALLED_APPS` are needed — the mixin works purely at the
viewset level.

## Basic usage

### 1. Define a model with choices

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

### 2. Add the mixin to your viewset

Place `ChoicesMixin` **before** the base viewset class in the inheritance
list so its methods take priority:

```python
from django_rest_choices import ChoicesMixin
from rest_framework.viewsets import ModelViewSet


class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### 3. Register the viewset with a router

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tasks", TaskViewSet)
```

That's it. Two new endpoints are now available.

## Trying it out

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

Only `status` and `priority` appear — `title` and `description` have no
choices and are excluded automatically.

**Single field** — `GET /tasks/choices/status/`

```json
[
  {"value": "active", "display": "Active"},
  {"value": "inactive", "display": "Inactive"}
]
```

**Field without choices** — `GET /tasks/choices/title/`

```json
{"detail": "Field 'title' does not have choices."}
```

Returns HTTP **404**.

## Supported choice formats

The mixin works with every way Django lets you define choices.

### TextChoices / IntegerChoices enums

```python
class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

status = models.CharField(choices=Status.choices)
```

### Plain tuples

```python
status = models.CharField(
    choices=[("active", "Active"), ("inactive", "Inactive")]
)
```

### Grouped choices

Groups are flattened automatically in the response:

```python
COLOR_CHOICES = [
    ("Warm", [("red", "Red"), ("orange", "Orange")]),
    ("Cool", [("blue", "Blue"), ("green", "Green")]),
]
color = models.CharField(choices=COLOR_CHOICES)
```

```json
[
  {"value": "red", "display": "Red"},
  {"value": "orange", "display": "Orange"},
  {"value": "blue", "display": "Blue"},
  {"value": "green", "display": "Green"}
]
```

## Next steps

See [Configuration](configuration.md) to customize endpoint names, filter
fields, or change the response format.