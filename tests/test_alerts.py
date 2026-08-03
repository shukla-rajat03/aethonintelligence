def test_alerts_requires_auth(client):
    resp = client.get("/api/v1/alerts")
    assert resp.status_code == 401


def test_alerts_authenticated(client, auth_headers):
    resp = client.get("/api/v1/alerts", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
