from rest_framework.decorators import action
from rest_framework.response import Response


class ChoicesMixin:
    """Mixin for DRF viewsets that auto-generates endpoints for model field choices.

    Adds two list-level endpoints to any viewset. By default::

        GET /resource/choices/              — all fields with choices
        GET /resource/choices/{field_name}/ — choices for a single field

    Configuration (class attributes):

        choices_endpoint_name
            URL segment for the endpoints (default: ``"choices"``).
        choices_field_first
            Put field name before the endpoint (default: ``False``).
        choices_fields
            Field names to expose, or ``None`` for all (default: ``None``).
        choices_value_key
            Key for the choice value in responses (default: ``"value"``).
        choices_display_key
            Key for the display text in responses (default: ``"display"``).

    Example::

        class TaskViewSet(ChoicesMixin, ModelViewSet):
            queryset = Task.objects.all()
            serializer_class = TaskSerializer
            choices_endpoint_name = "options"
            choices_field_first = True       # → /tasks/{field}/options/
            choices_fields = ["status"]
            choices_value_key = "id"
            choices_display_key = "label"
    """

    choices_endpoint_name = "choices"
    choices_field_first = False
    choices_fields = None
    choices_value_key = "value"
    choices_display_key = "display"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        endpoint = getattr(cls, "choices_endpoint_name", "choices")
        field_first = getattr(cls, "choices_field_first", False)

        if field_first:
            field_url = rf"(?P<field_name>[^/.]+)/{endpoint}"
        else:
            field_url = rf"{endpoint}/(?P<field_name>[^/.]+)"

        @action(detail=False, url_path=endpoint, url_name=endpoint)
        def choices(self, request):
            """Return choices for every field that defines them."""
            return self._respond_all_choices()

        @action(detail=False, url_path=field_url, url_name=f"field-{endpoint}")
        def field_choices(self, request, field_name=None):
            """Return choices for a single field, or 404 if it has none."""
            return self._respond_field_choices(field_name)

        cls.choices = choices
        cls.field_choices = field_choices

    def _get_choices_model(self):
        """Resolve the model class from the viewset's queryset."""
        if self.queryset is not None:
            return self.queryset.model
        return self.get_queryset().model

    def _get_choices_fields(self):
        """Return filtered ``{field_name: flat_choices}`` mapping."""
        model = self._get_choices_model()
        result = {}
        for field in model._meta.get_fields():
            if not hasattr(field, "choices") or not field.choices:
                continue
            if (
                self.choices_fields is not None
                and field.name not in self.choices_fields
            ):
                continue
            result[field.name] = field.flatchoices
        return result

    def _format_choices(self, choices):
        """Convert a list of ``(value, display)`` tuples into response dicts."""
        return [
            {self.choices_value_key: value, self.choices_display_key: display}
            for value, display in choices
        ]

    def _respond_all_choices(self):
        """Build the response for the all-choices endpoint."""
        return Response(
            {
                name: self._format_choices(field_choices)
                for name, field_choices in self._get_choices_fields().items()
            }
        )

    def _respond_field_choices(self, field_name):
        """Build the response for the single-field endpoint."""
        fields = self._get_choices_fields()
        if field_name not in fields:
            return Response(
                {"detail": f"Field '{field_name}' does not have choices."},
                status=404,
            )
        return Response(self._format_choices(fields[field_name]))
