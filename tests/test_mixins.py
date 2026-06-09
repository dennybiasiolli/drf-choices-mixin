import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestChoicesEndpoint:
    """Tests for GET /resource/choices/."""

    def test_returns_all_choices(self, client):
        response = client.get("/tasks/choices/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "priority" in data
        assert len(data) == 2

    def test_status_choices_values(self, client):
        response = client.get("/tasks/choices/")
        status = response.json()["status"]
        assert status == [
            {"value": "active", "display": "Active"},
            {"value": "inactive", "display": "Inactive"},
        ]

    def test_integer_choices_values(self, client):
        response = client.get("/tasks/choices/")
        priority = response.json()["priority"]
        assert priority == [
            {"value": 1, "display": "Low"},
            {"value": 2, "display": "Medium"},
            {"value": 3, "display": "High"},
        ]

    def test_model_without_choices_returns_empty(self, client):
        response = client.get("/articles/choices/")
        assert response.status_code == 200
        assert response.json() == {}

    def test_grouped_choices_are_flattened(self, client):
        response = client.get("/items/choices/")
        colors = response.json()["color"]
        assert colors == [
            {"value": "red", "display": "Red"},
            {"value": "orange", "display": "Orange"},
            {"value": "blue", "display": "Blue"},
            {"value": "green", "display": "Green"},
        ]


@pytest.mark.django_db
class TestFieldChoicesEndpoint:
    """Tests for GET /resource/choices/{field_name}/."""

    def test_returns_choices_for_field(self, client):
        response = client.get("/tasks/choices/status/")
        assert response.status_code == 200
        assert response.json() == [
            {"value": "active", "display": "Active"},
            {"value": "inactive", "display": "Inactive"},
        ]

    def test_field_without_choices_returns_404(self, client):
        response = client.get("/tasks/choices/title/")
        assert response.status_code == 404
        assert "title" in response.json()["detail"]

    def test_nonexistent_field_returns_404(self, client):
        response = client.get("/tasks/choices/nonexistent/")
        assert response.status_code == 404

    def test_integer_field_choices(self, client):
        response = client.get("/tasks/choices/priority/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_grouped_field_choices(self, client):
        response = client.get("/items/choices/color/")
        assert response.status_code == 200
        assert len(response.json()) == 4
