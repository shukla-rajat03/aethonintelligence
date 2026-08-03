def test_routing_rules_requires_auth(client):
    resp = client.get("/api/v1/routing/rules")
    assert resp.status_code == 401


def test_routing_rules_authenticated(client, auth_headers):
    resp = client.get("/api/v1/routing/rules", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
