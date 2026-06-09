import django
from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "rest_framework",
            "tests",
        ],
        ROOT_URLCONF="tests.urls",
        REST_FRAMEWORK={
            "DEFAULT_PERMISSION_CLASSES": [
                "rest_framework.permissions.AllowAny",
            ],
        },
    )
    django.setup()
