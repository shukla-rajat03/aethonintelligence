def test_requests_list_requires_auth(client):
    resp = client.get("/api/v1/requests")
    assert resp.status_code == 401


def test_requests_list_authenticated(client, auth_headers):
    resp = client.get("/api/v1/requests", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
    assert "total" in body
    assert "page" in body
    assert "limit" in body
    assert isinstance(body["data"], list)


def test_requests_list_pagination_params(client, auth_headers):
    resp = client.get(
        "/api/v1/requests", headers=auth_headers, params={"page": 1, "limit": 5}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["page"] == 1
    assert body["limit"] == 5


def test_requests_list_invalid_page(client, auth_headers):
    resp = client.get(
        "/api/v1/requests", headers=auth_headers, params={"page": -1}
    )
    assert resp.status_code in (200, 422)
