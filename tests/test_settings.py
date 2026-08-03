def test_api_keys_requires_auth(client):
    resp = client.get("/api/v1/settings/api-keys")
    assert resp.status_code == 401


def test_api_keys_authenticated(client, auth_headers):
    resp = client.get("/api/v1/settings/api-keys", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_api_keys_create_requires_auth(client):
    resp = client.post("/api/v1/settings/api-keys", json={"name": "qa-key"})
    assert resp.status_code == 401


def test_api_keys_create_and_appears_in_list(client, auth_headers):
    resp = client.post(
        "/api/v1/settings/api-keys",
        json={"name": "qa-lifecycle-key"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    body = resp.json()
    assert "id" in body
    assert body["name"] == "qa-lifecycle-key"
    # Full secret key is returned once on creation.
    assert body["key"].startswith("sk-")
    assert body["status"] == "active"

    key_id = body["id"]
    try:
        list_resp = client.get("/api/v1/settings/api-keys", headers=auth_headers)
        assert list_resp.status_code == 200
        ids = [k["id"] for k in list_resp.json()]
        assert key_id in ids
        # The list view must not leak the full plaintext secret again.
        listed = next(k for k in list_resp.json() if k["id"] == key_id)
        assert listed.get("key") != body["key"]
    finally:
        client.delete(f"/api/v1/settings/api-keys/{key_id}", headers=auth_headers)


def test_api_keys_create_missing_name(client, auth_headers):
    resp = client.post("/api/v1/settings/api-keys", json={}, headers=auth_headers)
    assert resp.status_code in (400, 422)


def test_api_keys_revoke_requires_auth(client):
    resp = client.delete("/api/v1/settings/api-keys/nonexistent-id")
    assert resp.status_code == 401


def test_api_keys_revoke_then_gone_from_list(client, auth_headers):
    create_resp = client.post(
        "/api/v1/settings/api-keys",
        json={"name": "qa-revoke-key"},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    key_id = create_resp.json()["id"]

    delete_resp = client.delete(
        f"/api/v1/settings/api-keys/{key_id}", headers=auth_headers
    )
    assert delete_resp.status_code in (200, 204)

    list_resp = client.get("/api/v1/settings/api-keys", headers=auth_headers)
    ids = [k["id"] for k in list_resp.json()]
    assert key_id not in ids


def test_api_keys_revoke_nonexistent_id(client, auth_headers):
    resp = client.delete(
        "/api/v1/settings/api-keys/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_api_keys_revoke_twice_is_not_ok(client, auth_headers):
    create_resp = client.post(
        "/api/v1/settings/api-keys",
        json={"name": "qa-double-revoke-key"},
        headers=auth_headers,
    )
    key_id = create_resp.json()["id"]

    first = client.delete(f"/api/v1/settings/api-keys/{key_id}", headers=auth_headers)
    assert first.status_code in (200, 204)

    second = client.delete(f"/api/v1/settings/api-keys/{key_id}", headers=auth_headers)
    assert second.status_code == 404
