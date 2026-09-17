"""Tests for Research API — async creation, status polling, and callback ingestion."""


def _create_product(client):
    """Helper: create a product and return its ID."""
    resp = client.post(
        "/api/products/",
        json={"name": "TestProduct", "problem": "Testing"},
    )
    return resp.json()["id"]


def test_trigger_research(client):
    """POST /api/research should create a run and return immediately."""
    product_id = _create_product(client)

    response = client.post(
        "/api/research/",
        json={"product_id": product_id},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["product_id"] == product_id
    assert data["status"] in ("pending", "queued")
    assert data["progress"] >= 0
    assert "id" in data


def test_trigger_research_nonexistent_product(client):
    """POST /api/research with invalid product_id should return 404."""
    response = client.post(
        "/api/research/",
        json={"product_id": 99999},
    )
    assert response.status_code == 404


def test_list_research_runs(client):
    """GET /api/research should return a list of runs."""
    product_id = _create_product(client)
    client.post("/api/research/", json={"product_id": product_id})

    response = client.get("/api/research/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_research_run(client):
    """GET /api/research/{id} should return the run with progress."""
    product_id = _create_product(client)
    create_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = create_resp.json()["id"]

    response = client.get(f"/api/research/{run_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == run_id
    assert "progress" in data
    assert "sources_analyzed" in data
    assert "leads_found" in data


def test_filter_research_by_product(client):
    """GET /api/research?product_id=X should filter results."""
    product_id = _create_product(client)
    client.post("/api/research/", json={"product_id": product_id})

    response = client.get(f"/api/research/?product_id={product_id}")
    assert response.status_code == 200
    for run in response.json():
        assert run["product_id"] == product_id


def test_research_callback_without_auth(client):
    """POST /api/research/{id}/callback without auth should return 401."""
    product_id = _create_product(client)
    create_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = create_resp.json()["id"]

    response = client.post(
        f"/api/research/{run_id}/callback",
        json={
            "research_run_id": run_id,
            "event_id": "evt_test_1",
            "status": "completed",
        },
    )
    assert response.status_code == 401


def test_research_callback_with_wrong_secret(client):
    """POST /api/research/{id}/callback with wrong secret should return 401."""
    product_id = _create_product(client)
    create_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = create_resp.json()["id"]

    response = client.post(
        f"/api/research/{run_id}/callback",
        json={
            "research_run_id": run_id,
            "event_id": "evt_test_2",
            "status": "completed",
        },
        headers={"Authorization": "Bearer wrong-secret"},
    )
    assert response.status_code == 401


def test_research_callback_success(client):
    """POST /api/research/{id}/callback with valid auth should process results."""
    product_id = _create_product(client)
    create_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = create_resp.json()["id"]

    callback_payload = {
        "research_run_id": run_id,
        "event_id": "evt_success_1",
        "status": "completed",
        "progress": 100,
        "sources_analyzed": 50,
        "results_found": 200,
        "relevant_results": 30,
        "leads": [
            {
                "source": "reddit",
                "source_url": "https://reddit.com/r/startups/1",
                "author": "testuser",
                "customer_segment": "Startup founders",
                "problem_detected": "Can't find early customers",
                "pain_level": 0.85,
                "intent_level": 0.72,
                "problem_fit": 0.91,
                "persona_fit": 0.87,
                "evidence_strength": 0.84,
                "reason": "Actively seeking customer discovery tools",
                "outreach_angle": "Automate your customer discovery",
                "evidence": [
                    {
                        "content": "I spend 5 hours every week trying to find potential customers",
                        "source_url": "https://reddit.com/r/startups/1",
                        "signal_type": "pain",
                        "strength": 0.9,
                    }
                ],
            }
        ],
        "segments": [
            {
                "name": "Solo Founders",
                "description": "Individual founders building products alone",
                "estimated_size": 50000,
                "priority_level": "high",
                "market_language": "customer discovery, finding users, validation",
            }
        ],
        "report": {
            "summary": "Strong signals detected in startup communities",
            "top_customer_segments": ["Solo Founders", "Indie Hackers"],
            "top_pain_points": ["Finding early customers", "Manual research"],
            "market_language": ["customer discovery", "validation"],
            "recommended_next_steps": ["Target Reddit communities", "Create landing page"],
        },
    }

    response = client.post(
        f"/api/research/{run_id}/callback",
        json=callback_payload,
        headers={"Authorization": "Bearer test-secret"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "processed"
    assert data["leads_created"] == 1
    assert data["segments_created"] == 1
    assert data["report_created"] is True

    # Verify the run was updated
    run_resp = client.get(f"/api/research/{run_id}")
    run_data = run_resp.json()
    assert run_data["status"] == "completed"
    assert run_data["progress"] == 100
    assert run_data["sources_analyzed"] == 50
    assert run_data["leads_found"] == 1
    assert run_data["segments_found"] == 1

    # Verify leads endpoint
    leads_resp = client.get(f"/api/research/{run_id}/leads")
    assert leads_resp.status_code == 200
    assert len(leads_resp.json()) == 1
    assert leads_resp.json()[0]["overall_score"] is not None

    # Verify segments endpoint
    segs_resp = client.get(f"/api/research/{run_id}/segments")
    assert segs_resp.status_code == 200
    assert len(segs_resp.json()) == 1

    # Verify report endpoint
    report_resp = client.get(f"/api/research/{run_id}/report")
    assert report_resp.status_code == 200
    assert report_resp.json()["summary"] == "Strong signals detected in startup communities"


def test_research_callback_idempotent(client):
    """Sending the same callback twice should be idempotent."""
    product_id = _create_product(client)
    create_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = create_resp.json()["id"]

    payload = {
        "research_run_id": run_id,
        "event_id": "evt_idemp_1",
        "status": "completed",
        "leads": [
            {
                "source": "github",
                "problem_detected": "Needs tool",
                "pain_level": 0.5,
                "evidence": [],
            }
        ],
    }
    headers = {"Authorization": "Bearer test-secret"}

    # First call
    resp1 = client.post(f"/api/research/{run_id}/callback", json=payload, headers=headers)
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "processed"

    # Second call with same event_id
    resp2 = client.post(f"/api/research/{run_id}/callback", json=payload, headers=headers)
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "duplicate"

    # Should still only have 1 lead
    leads_resp = client.get(f"/api/research/{run_id}/leads")
    assert len(leads_resp.json()) == 1
