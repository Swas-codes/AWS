"""Tests for Customer Segments API."""


def _setup_product_and_run(client):
    """Helper to create a product and a research run."""
    prod_resp = client.post("/api/products/", json={"name": "Segment Test Product"})
    product_id = prod_resp.json()["id"]

    run_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = run_resp.json()["id"]
    return product_id, run_id


def test_create_segment(client):
    """POST /api/segments should create a segment."""
    _, run_id = _setup_product_and_run(client)

    response = client.post(
        "/api/segments/",
        json={
            "research_run_id": run_id,
            "name": "Solo Founders",
            "description": "Early stage solo founders building SaaS",
            "estimated_size": 1500,
            "priority_level": "high",
            "market_language": "Automate early user discovery",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Solo Founders"
    assert data["research_run_id"] == run_id
    assert data["estimated_size"] == 1500
    assert data["priority_level"] == "high"


def test_create_segment_invalid_run(client):
    """POST /api/segments with invalid research_run_id should return 404."""
    response = client.post(
        "/api/segments/",
        json={
            "research_run_id": 99999,
            "name": "Ghost Segment",
        },
    )
    assert response.status_code == 404


def test_list_and_filter_segments(client):
    """GET /api/segments should list segments and filter by research_run_id."""
    _, run_id1 = _setup_product_and_run(client)
    _, run_id2 = _setup_product_and_run(client)

    client.post(
        "/api/segments/",
        json={"research_run_id": run_id1, "name": "Run 1 Segment"},
    )
    client.post(
        "/api/segments/",
        json={"research_run_id": run_id2, "name": "Run 2 Segment"},
    )

    # List all
    all_resp = client.get("/api/segments/")
    assert all_resp.status_code == 200
    assert len(all_resp.json()) >= 2

    # Filter by run_id1
    filtered_resp = client.get(f"/api/segments/?research_run_id={run_id1}")
    assert filtered_resp.status_code == 200
    segments = filtered_resp.json()
    assert len(segments) == 1
    assert segments[0]["name"] == "Run 1 Segment"


def test_get_segment(client):
    """GET /api/segments/{id} should return the segment."""
    _, run_id = _setup_product_and_run(client)

    create_resp = client.post(
        "/api/segments/",
        json={"research_run_id": run_id, "name": "Target Segment"},
    )
    seg_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/segments/{seg_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Target Segment"


def test_get_segment_not_found(client):
    """GET /api/segments/99999 should return 404."""
    response = client.get("/api/segments/99999")
    assert response.status_code == 404
