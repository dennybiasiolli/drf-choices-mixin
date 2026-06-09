from django.db import models


class Status(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class Priority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"


class Task(models.Model):
    """Test model with multiple choices fields."""

    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices)
    priority = models.IntegerField(choices=Priority.choices)
    description = models.TextField()

    class Meta:
        app_label = "tests"


GROUPED_CHOICES = [
    (
        "Warm",
        [
            ("red", "Red"),
            ("orange", "Orange"),
        ],
    ),
    (
        "Cool",
        [
            ("blue", "Blue"),
            ("green", "Green"),
        ],
    ),
]


class Item(models.Model):
    """Test model with grouped choices."""

    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=GROUPED_CHOICES)

    class Meta:
        app_label = "tests"


class Article(models.Model):
    """Test model with no choices fields."""

    title = models.CharField(max_length=100)
    body = models.TextField()

    class Meta:
        app_label = "tests"
