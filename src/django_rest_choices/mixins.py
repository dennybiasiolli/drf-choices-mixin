from rest_framework.decorators import action
from rest_framework.response import Response


class ChoicesMixin:
    """Mixin for DRF viewsets that auto-generates endpoints for model field choices.

    Adds two list-level endpoints to any viewset:

        GET /resource/choices/              — all fields with choices
        GET /resource/choices/{field_name}/ — choices for a single field

    Usage::

        class TaskViewSet(ChoicesMixin, ModelViewSet):
            queryset = Task.objects.all()
            serializer_class = TaskSerializer
    """

    def _get_choices_model(self):
        """Resolve the model class from the viewset's queryset."""
        if self.queryset is not None:
            return self.queryset.model
        return self.get_queryset().model

    def _get_choices_fields(self):
        """Return ``{field_name: flat_choices}`` for every field that has choices."""
        model = self._get_choices_model()
        result = {}
        for field in model._meta.get_fields():
            if hasattr(field, "choices") and field.choices:
                result[field.name] = field.flatchoices
        return result

    @staticmethod
    def _format_choices(choices):
        """Convert a list of ``(value, display)`` tuples into dicts."""
        return [{"value": value, "display": display} for value, display in choices]

    @action(detail=False, url_path="choices", url_name="choices")
    def choices(self, request):
        """Return choices for every field that defines them."""
        return Response(
            {
                name: self._format_choices(choices)
                for name, choices in self._get_choices_fields().items()
            }
        )

    @action(
        detail=False,
        url_path=r"choices/(?P<field_name>[^/.]+)",
        url_name="field-choices",
    )
    def field_choices(self, request, field_name=None):
        """Return choices for a single field, or 404 if it has none."""
        fields = self._get_choices_fields()
        if field_name not in fields:
            return Response(
                {"detail": f"Field '{field_name}' does not have choices."},
                status=404,
            )
        return Response(self._format_choices(fields[field_name]))
