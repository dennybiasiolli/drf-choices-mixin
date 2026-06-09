from rest_framework.serializers import ModelSerializer

from .models import Article, Item, Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
