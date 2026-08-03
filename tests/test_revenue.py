def test_revenue_summary_requires_auth(client):
    resp = client.get("/api/v1/revenue/summary")
    assert resp.status_code == 401


def test_revenue_summary_authenticated(client, auth_headers):
    resp = client.get("/api/v1/revenue/summary", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    for key in ("total_leakage", "leakage_pct", "finding_count", "scan_date"):
        assert key in body
