"""Tests for Leads and Evidence API."""


def _setup_product_and_run(client):
    """Helper to create a product and a research run."""
    prod_resp = client.post("/api/products/", json={"name": "Lead Test Product"})
    product_id = prod_resp.json()["id"]

    run_resp = client.post("/api/research/", json={"product_id": product_id})
    run_id = run_resp.json()["id"]
    return product_id, run_id


def test_create_lead(client):
    """POST /api/leads should create a lead with auto-calculated overall score."""
    _, run_id = _setup_product_and_run(client)

    response = client.post(
        "/api/leads/",
        json={
            "research_run_id": run_id,
            "author": "u/startup_founder",
            "source": "reddit",
            "source_url": "https://reddit.com/r/startups/123",
            "customer_segment": "Technical Founders",
            "problem_detected": "Can't find early users",
            "problem_fit": 0.8,
            "intent_level": 0.9,
            "persona_fit": 0.7,
            "evidence_strength": 0.8,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "u/startup_founder"
    assert data["source"] == "reddit"
    assert data["overall_score"] is not None
    # 0.8*0.35 + 0.9*0.30 + 0.7*0.20 + 0.8*0.15 = 0.28 + 0.27 + 0.14 + 0.12 = 0.81
    assert abs(data["overall_score"] - 0.81) < 0.01


def test_create_lead_invalid_run(client):
    """POST /api/leads with invalid research_run_id should return 404."""
    response = client.post(
        "/api/leads/",
        json={
            "research_run_id": 99999,
            "author": "Ghost",
            "source": "twitter",
        },
    )
    assert response.status_code == 404


def test_list_and_filter_leads(client):
    """GET /api/leads should return leads and support filtering."""
    _, run_id = _setup_product_and_run(client)

    client.post(
        "/api/leads/",
        json={
            "research_run_id": run_id,
            "author": "High Scorer",
            "source": "reddit",
            "customer_segment": "Enterprise",
            "problem_fit": 1.0,
            "intent_level": 1.0,
            "persona_fit": 1.0,
            "evidence_strength": 1.0,
        },
    )
    client.post(
        "/api/leads/",
        json={
            "research_run_id": run_id,
            "author": "Low Scorer",
            "source": "github",
            "customer_segment": "Hobbyist",
            "problem_fit": 0.1,
            "intent_level": 0.1,
            "persona_fit": 0.1,
            "evidence_strength": 0.1,
        },
    )

    # Filter by min_score
    resp = client.get("/api/leads/?min_score=0.5")
    assert resp.status_code == 200
    leads = resp.json()
    assert len(leads) == 1
    assert leads[0]["author"] == "High Scorer"

    # Filter by source
    resp_source = client.get("/api/leads/?source=github")
    assert resp_source.status_code == 200
    assert len(resp_source.json()) == 1
    assert resp_source.json()[0]["author"] == "Low Scorer"

    # Filter by segment
    resp_seg = client.get("/api/leads/?segment=Enterprise")
    assert resp_seg.status_code == 200
    assert len(resp_seg.json()) == 1


def test_get_lead_and_add_evidence(client):
    """GET /api/leads/{id} returns lead details and evidence."""
    _, run_id = _setup_product_and_run(client)

    lead_resp = client.post(
        "/api/leads/",
        json={"research_run_id": run_id, "author": "Evidence Tester", "source": "hackernews"},
    )
    lead_id = lead_resp.json()["id"]

    # Add evidence
    ev_resp = client.post(
        f"/api/leads/{lead_id}/evidence",
        json={
            "content": "Looking for a tool to solve this exact problem!",
            "source_url": "https://news.ycombinator.com/item?id=123",
            "signal_type": "high_intent",
            "strength": 0.95,
        },
    )
    assert ev_resp.status_code == 201
    assert ev_resp.json()["lead_id"] == lead_id

    # Retrieve lead with evidence
    get_resp = client.get(f"/api/leads/{lead_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert len(data["evidence"]) == 1
    assert data["evidence"][0]["strength"] == 0.95


def test_get_lead_not_found(client):
    """GET /api/leads/99999 should return 404."""
    response = client.get("/api/leads/99999")
    assert response.status_code == 404
