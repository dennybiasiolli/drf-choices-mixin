# drf-choices-mixin

A Django REST Framework mixin that automatically generates API endpoints for
model field choices. Drop `ChoicesMixin` into any DRF viewset and it will
expose every field that defines `choices` through list-level endpoints — no
manual serializer or view code required.

## Features

- **Zero configuration** — add the mixin and endpoints appear automatically.
- **Fully configurable** — customize endpoint names, URL structure, exposed fields, and response format.
- **Works with all choice types** — `TextChoices`, `IntegerChoices`, plain tuples, and grouped choices.
- **Two endpoints per viewset** — one for all choices, one for a specific field.

## How it works

For a viewset registered at `/tasks/`, the mixin adds:

| Endpoint | Description |
|---|---|
| `GET /tasks/choices/` | Returns choices for **every** field that defines them |
| `GET /tasks/choices/{field_name}/` | Returns choices for a **single** field |

Each choice is returned as a dictionary with `value` and `display` keys:

```json
[
  {"value": "active", "display": "Active"},
  {"value": "inactive", "display": "Inactive"}
]
```

Every aspect of this — the URL segments, which fields are exposed, and the
response key names — is configurable through class attributes. See the
[Configuration](configuration.md) page for details.

## Requirements

- Python >= 3.10
- Django >= 4.2
- Django REST Framework >= 3.14