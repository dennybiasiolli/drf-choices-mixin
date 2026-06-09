from rest_framework.viewsets import ModelViewSet

from django_rest_choices import ChoicesMixin

from .models import Article, Item, Task
from .serializers import ArticleSerializer, ItemSerializer, TaskSerializer


class TaskViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ItemViewSet(ChoicesMixin, ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ArticleViewSet(ChoicesMixin, ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CustomEndpointViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"


class FieldFirstViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_field_first = True


class FieldFirstCustomViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_endpoint_name = "options"
    choices_field_first = True


class FilteredFieldsViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_fields = ["status"]


class CustomKeysViewSet(ChoicesMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    choices_value_key = "key"
    choices_display_key = "label"
