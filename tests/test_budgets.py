def test_budgets_requires_auth(client):
    resp = client.get("/api/v1/budgets")
    assert resp.status_code == 401


def test_budgets_authenticated(client, auth_headers):
    resp = client.get("/api/v1/budgets", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
