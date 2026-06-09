# Configuration

All configuration is done through class attributes on the viewset. Every
option has a sensible default, so none of them are required.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `choices_endpoint_name` | `str` | `"choices"` | URL segment used for both endpoints |
| `choices_field_first` | `bool` | `False` | Put the field name before the endpoint segment in URLs |
| `choices_fields` | `list[str] \| None` | `None` | Restrict which fields are exposed (`None` = all) |
| `choices_value_key` | `str` | `"value"` | Key name for the choice value in the response |
| `choices_display_key` | `str` | `"display"` | Key name for the display text in the response |

---

## `choices_endpoint_name`

**Default:** `"choices"`

Changes the URL segment for both endpoints. Useful for avoiding conflicts
with other custom actions or for matching your API naming conventions.

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"
```

**Resulting endpoints:**

| Before | After |
|---|---|
| `GET /tasks/choices/` | `GET /tasks/options/` |
| `GET /tasks/choices/status/` | `GET /tasks/options/status/` |

---

## `choices_field_first`

**Default:** `False`

Controls the order of the URL segments for the single-field endpoint. When
set to `True`, the field name comes before the endpoint name. This can read
more naturally in some APIs.

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_field_first = True
```

**Resulting endpoints:**

| Default (`False`) | Field-first (`True`) |
|---|---|
| `GET /tasks/choices/` | `GET /tasks/choices/` |
| `GET /tasks/choices/status/` | `GET /tasks/status/choices/` |

!!! note
    The all-choices endpoint is always just the endpoint name — only the
    per-field endpoint changes order.

### Combining with a custom endpoint name

Both options work together:

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
| `GET /tasks/priority/options/` | Choices for the `priority` field |

---

## `choices_fields`

**Default:** `None` (expose all fields that have choices)

A list of field names to include. Fields not in the list are hidden from
both the all-choices endpoint and the per-field endpoint.

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_fields = ["status"]
```

**`GET /tasks/choices/`** now returns only `status`:

```json
{
  "status": [
    {"value": "active", "display": "Active"},
    {"value": "inactive", "display": "Inactive"}
  ]
}
```

**`GET /tasks/choices/priority/`** returns **404**:

```json
{"detail": "Field 'priority' does not have choices."}
```

!!! tip
    Use this when your model has many choice fields but you only want to
    expose a subset through the API.

---

## `choices_value_key` / `choices_display_key`

**Defaults:** `"value"` and `"display"`

Override the dictionary key names in the response to match what your frontend
expects.

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_value_key = "key"
    choices_display_key = "label"
```

**`GET /tasks/choices/status/`** now returns:

```json
[
  {"key": "active", "label": "Active"},
  {"key": "inactive", "label": "Inactive"}
]
```

The all-choices endpoint uses the same keys:

```json
{
  "status": [
    {"key": "active", "label": "Active"},
    {"key": "inactive", "label": "Inactive"}
  ],
  "priority": [
    {"key": 1, "label": "Low"},
    {"key": 2, "label": "Medium"},
    {"key": 3, "label": "High"}
  ]
}
```

---

## Full example

All options used together:

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
| `GET /tasks/status/options/` | `[{"id": "active", "text": "Active"}, {"id": "inactive", "text": "Inactive"}]` |
| `GET /tasks/description/options/` | 404 — `description` has no choices |
| `GET /tasks/title/options/` | 404 — `title` not in `choices_fields` |

## Per-viewset configuration

Each viewset is configured independently. Different viewsets in the same
project can use different settings:

```python
class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"

class OrderViewSet(ChoicesMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    choices_endpoint_name = "enums"
    choices_value_key = "code"
    choices_display_key = "name"
```

- `GET /tasks/options/` uses `value` / `display` keys.
- `GET /orders/enums/` uses `code` / `name` keys.