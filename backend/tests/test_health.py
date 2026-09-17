"""Tests for the health check endpoint."""


def test_health_endpoint(client):
    """GET /health should return 200 with status info."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert data["service"] == "LaunchLens Backend"
    assert "database" in data
    assert "redis" in data


def test_root_endpoint(client):
    """GET / should return service info."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == "LaunchLens API"
    assert "docs" in data
