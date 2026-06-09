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


@pytest.mark.django_db
class TestCustomEndpointName:
    """Tests for choices_endpoint_name configuration."""

    def test_all_choices_at_custom_url(self, client):
        response = client.get("/custom-endpoint/options/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "priority" in data

    def test_field_choices_at_custom_url(self, client):
        response = client.get("/custom-endpoint/options/status/")
        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.django_db
class TestFieldFirstUrl:
    """Tests for choices_field_first = True."""

    def test_all_choices_endpoint_unchanged(self, client):
        response = client.get("/field-first/choices/")
        assert response.status_code == 200
        assert "status" in response.json()

    def test_field_name_before_endpoint(self, client):
        response = client.get("/field-first/status/choices/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_nonexistent_field_returns_404(self, client):
        response = client.get("/field-first/nonexistent/choices/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestFieldFirstCustomEndpoint:
    """Tests for choices_field_first + choices_endpoint_name combined."""

    def test_all_choices_at_custom_url(self, client):
        response = client.get("/field-first-custom/options/")
        assert response.status_code == 200
        assert "status" in response.json()

    def test_field_name_before_custom_endpoint(self, client):
        response = client.get("/field-first-custom/status/options/")
        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.django_db
class TestFilteredFields:
    """Tests for choices_fields configuration."""

    def test_only_specified_fields_included(self, client):
        response = client.get("/filtered/choices/")
        data = response.json()
        assert "status" in data
        assert "priority" not in data
        assert len(data) == 1

    def test_excluded_field_returns_404(self, client):
        response = client.get("/filtered/choices/priority/")
        assert response.status_code == 404

    def test_included_field_works(self, client):
        response = client.get("/filtered/choices/status/")
        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.django_db
class TestCustomKeys:
    """Tests for choices_value_key and choices_display_key configuration."""

    def test_all_choices_uses_custom_keys(self, client):
        response = client.get("/custom-keys/choices/")
        first_choice = response.json()["status"][0]
        assert "key" in first_choice
        assert "label" in first_choice
        assert "value" not in first_choice
        assert "display" not in first_choice

    def test_field_choices_uses_custom_keys(self, client):
        response = client.get("/custom-keys/choices/status/")
        first_choice = response.json()[0]
        assert first_choice == {"key": "active", "label": "Active"}
