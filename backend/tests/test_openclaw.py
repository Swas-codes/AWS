"""Tests for OpenClaw Autonomous Customer Discovery Agent Integration."""


def test_openclaw_status_endpoint(client):
    """GET /api/openclaw/status should report OpenClaw binary availability and version."""
    response = client.get("/api/openclaw/status")
    assert response.status_code == 200

    data = response.json()
    assert "installed" in data
    assert "path" in data
    assert "version" in data
    assert "enabled" in data
    assert data["installed"] is True
    assert data["status"] in ("ready", "not_installed")


def test_openclaw_run_missing_params(client):
    """POST /api/openclaw/run without product_id or research_run_id should return 400."""
    response = client.post("/api/openclaw/run", json={})
    assert response.status_code == 400


def test_openclaw_run_nonexistent_product(client):
    """POST /api/openclaw/run with invalid product_id should return 404."""
    response = client.post("/api/openclaw/run", json={"product_id": 99999})
    assert response.status_code == 404


def test_openclaw_run_successful_discovery(client):
    """POST /api/openclaw/run should execute discovery and ingest scored prospects and segments."""
    # 1. Create a product
    prod_resp = client.post(
        "/api/products/",
        json={
            "name": "DevMetrics Cloud",
            "description": "Real-time CI/CD performance and cost analytics",
            "target_users": "Platform Engineers",
            "problem": "Uncontrolled cloud spend on GitHub Actions runners",
        },
    )
    product_id = prod_resp.json()["id"]

    # 2. Trigger OpenClaw discovery
    run_resp = client.post(
        "/api/openclaw/run",
        json={"product_id": product_id},
    )
    assert run_resp.status_code == 200

    data = run_resp.json()
    assert data["message"] == "OpenClaw research completed and ingested"
    assert "research_run_id" in data
    assert data["product_id"] == product_id

    run_id = data["research_run_id"]

    # 3. Check research run status
    get_run = client.get(f"/api/research/{run_id}")
    assert get_run.status_code == 200
    run_data = get_run.json()
    assert run_data["status"] == "completed"
    assert run_data["progress"] == 100
    assert run_data["sources_analyzed"] > 0
    assert run_data["leads_found"] > 0

    # 4. Check discovered leads were persisted with deterministic scoring
    leads_resp = client.get("/api/leads/")
    assert leads_resp.status_code == 200
    leads = leads_resp.json()
    assert len(leads) >= 1
    lead = leads[0]
    assert lead["overall_score"] is not None
    assert 0.0 <= lead["overall_score"] <= 1.0

    # 5. Check discovered segments were persisted
    segments_resp = client.get("/api/segments/")
    assert segments_resp.status_code == 200
    segments = segments_resp.json()
    assert len(segments) >= 1
