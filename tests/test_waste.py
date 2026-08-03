def test_waste_requires_auth(client):
    resp = client.get("/api/v1/waste")
    assert resp.status_code == 401


def test_waste_authenticated(client, auth_headers):
    resp = client.get("/api/v1/waste", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
