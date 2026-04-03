"""
Calculator API Tests

These tests assert correct addition behavior against the /add endpoint.
With the current app bug (subtraction instead of addition), all math
assertions will fail — triggering the AI remediation agent in Testkube.

Expected failures with bug:
  5  + 3  → app returns  2  (5  - 3),  expected  8   ❌
  0  + 7  → app returns -7  (0  - 7),  expected  7   ❌
  100+ 50 → app returns 50  (100-50),  expected 150  ❌
  4  + 4  → app returns  0  (4  - 4),  expected  8   ❌
"""

import requests
import pytest


class TestHealthCheck:
    def test_health_endpoint_returns_ok(self, base_url):
        """Service is reachable and healthy."""
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestAddEndpoint:
    def test_add_two_positive_numbers(self, base_url):
        """5 + 3 should equal 8."""
        response = requests.post(f"{base_url}/add", json={"a": 5, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8, (
            f"Expected 5 + 3 = 8, but got {data['result']}. "
            f"(Hint: app may be subtracting instead of adding)"
        )

    def test_add_zero_to_number(self, base_url):
        """0 + 7 should equal 7."""
        response = requests.post(f"{base_url}/add", json={"a": 0, "b": 7})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 7, (
            f"Expected 0 + 7 = 7, but got {data['result']}."
        )

    def test_add_larger_numbers(self, base_url):
        """100 + 50 should equal 150."""
        response = requests.post(f"{base_url}/add", json={"a": 100, "b": 50})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 150, (
            f"Expected 100 + 50 = 150, but got {data['result']}."
        )

    def test_add_equal_numbers(self, base_url):
        """4 + 4 should equal 8."""
        response = requests.post(f"{base_url}/add", json={"a": 4, "b": 4})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8, (
            f"Expected 4 + 4 = 8, but got {data['result']}."
        )

    def test_response_includes_operands(self, base_url):
        """Response body should echo back the original operands."""
        response = requests.post(f"{base_url}/add", json={"a": 2, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["a"] == 2
        assert data["b"] == 3
        assert data["operation"] == "add"

    def test_missing_fields_returns_400(self, base_url):
        """Request without required fields should return 400."""
        response = requests.post(f"{base_url}/add", json={"a": 5})
        assert response.status_code == 400
