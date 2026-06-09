# API Reference

## Endpoints

The mixin adds two list-level (non-detail) endpoints to the viewset. Both
are `GET`-only and require no authentication by default (they inherit the
viewset's permission classes).

### All choices

```
GET /{prefix}/{endpoint}/
```

Returns a JSON object where each key is a field name and the value is a list
of choice dictionaries.

**Default URL:** `GET /tasks/choices/`

**Response** — `200 OK`:

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

If the model has no fields with choices (or all are filtered out by
`choices_fields`), the response is an empty object:

```json
{}
```

### Single field choices

```
GET /{prefix}/{endpoint}/{field_name}/
GET /{prefix}/{field_name}/{endpoint}/    (when choices_field_first = True)
```

Returns a JSON array of choice dictionaries for a single field.

**Default URL:** `GET /tasks/choices/status/`

**Response** — `200 OK`:

```json
[
  {"value": "active", "display": "Active"},
  {"value": "inactive", "display": "Inactive"}
]
```

**Error** — `404 Not Found`:

Returned when `field_name` does not exist on the model, the field has no
choices, or the field is excluded by `choices_fields`.

```json
{"detail": "Field 'title' does not have choices."}
```

---

## ChoicesMixin class

```python
from drf_choices_mixin import ChoicesMixin
```

### Class attributes

| Attribute | Type | Default |
|---|---|---|
| `choices_endpoint_name` | `str` | `"choices"` |
| `choices_field_first` | `bool` | `False` |
| `choices_fields` | `list[str] \| None` | `None` |
| `choices_value_key` | `str` | `"value"` |
| `choices_display_key` | `str` | `"display"` |

See [Configuration](configuration.md) for detailed descriptions and examples.

### Internal methods

These methods can be overridden for advanced customization:

#### `_get_choices_model()`

Returns the Django model class from the viewset's `queryset`. Override this
if your viewset resolves the model in a non-standard way.

#### `_get_choices_fields()`

Returns a `dict[str, list[tuple]]` mapping field names to their flat
choices. Respects the `choices_fields` filter.

#### `_format_choices(choices)`

Converts a list of `(value, display)` tuples into response dictionaries
using `choices_value_key` and `choices_display_key`.

#### `_respond_all_choices()`

Builds the `Response` for the all-choices endpoint. Override for fully
custom response formatting.

#### `_respond_field_choices(field_name)`

Builds the `Response` for the single-field endpoint, including the 404
handling. Override for fully custom response formatting.

---

## URL names

The mixin registers URL names that can be used with Django's `reverse()`:

| URL name | Pattern |
|---|---|
| `{basename}-{endpoint}` | All choices (e.g. `task-choices`) |
| `{basename}-field-{endpoint}` | Single field (e.g. `task-field-choices`) |

When using a custom `choices_endpoint_name = "options"`, the URL names
become `task-options` and `task-field-options`.