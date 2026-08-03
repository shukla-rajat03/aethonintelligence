def test_api_keys_requires_auth(client):
    resp = client.get("/api/v1/settings/api-keys")
    assert resp.status_code == 401


def test_api_keys_authenticated(client, auth_headers):
    resp = client.get("/api/v1/settings/api-keys", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
