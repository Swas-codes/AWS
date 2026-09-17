"""Tests for the Products CRUD API."""


def test_create_product(client):
    """POST /api/products should create a product and return 201."""
    response = client.post(
        "/api/products/",
        json={
            "name": "LaunchLens",
            "description": "AI-powered pre-launch customer discovery",
            "target_users": "Startup founders",
            "problem": "Finding early customers before launch",
        },
    )
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "LaunchLens"
    assert data["description"] == "AI-powered pre-launch customer discovery"
    assert data["id"] is not None
    assert "created_at" in data


def test_create_product_minimal(client):
    """POST /api/products with only name should work."""
    response = client.post("/api/products/", json={"name": "TestProduct"})
    assert response.status_code == 201
    assert response.json()["name"] == "TestProduct"


def test_create_product_empty_name_fails(client):
    """POST /api/products with empty name should fail validation."""
    response = client.post("/api/products/", json={"name": ""})
    assert response.status_code == 422


def test_list_products(client):
    """GET /api/products should return a list."""
    # Create two products
    client.post("/api/products/", json={"name": "Product A"})
    client.post("/api/products/", json={"name": "Product B"})

    response = client.get("/api/products/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_product(client):
    """GET /api/products/{id} should return the product."""
    create_resp = client.post("/api/products/", json={"name": "GetMe"})
    product_id = create_resp.json()["id"]

    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "GetMe"


def test_get_product_not_found(client):
    """GET /api/products/999 should return 404."""
    response = client.get("/api/products/99999")
    assert response.status_code == 404


def test_update_product(client):
    """PUT /api/products/{id} should update fields."""
    create_resp = client.post(
        "/api/products/",
        json={"name": "OldName", "description": "Old desc"},
    )
    product_id = create_resp.json()["id"]

    response = client.put(
        f"/api/products/{product_id}",
        json={"name": "NewName"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "NewName"
    # description should remain unchanged since we used exclude_unset
    assert data["description"] == "Old desc"


def test_delete_product(client):
    """DELETE /api/products/{id} should return 204 and remove the product."""
    create_resp = client.post("/api/products/", json={"name": "DeleteMe"})
    product_id = create_resp.json()["id"]

    response = client.delete(f"/api/products/{product_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_resp = client.get(f"/api/products/{product_id}")
    assert get_resp.status_code == 404
