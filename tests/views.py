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
