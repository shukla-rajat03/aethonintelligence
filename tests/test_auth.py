def test_login_success(client):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "test@gmail.com", "password": "test@gmail.com"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == "test@gmail.com"


def test_login_wrong_password(client):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "test@gmail.com", "password": "WrongPassword123"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid email or password"


def test_login_nonexistent_user(client):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "qa_does_not_exist@example.com", "password": "whatever123"},
    )
    assert resp.status_code == 401


def test_login_missing_fields(client):
    resp = client.post("/api/v1/auth/login", data={})
    assert resp.status_code == 422


def test_login_json_body_rejected(client):
    # This endpoint uses OAuth2PasswordRequestForm which requires
    # x-www-form-urlencoded, not JSON.
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "test@gmail.com", "password": "test@gmail.com"},
    )
    assert resp.status_code == 422


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"


def test_me_invalid_token(client):
    resp = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid or expired token"


def test_me_authenticated(client, auth_headers):
    resp = client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "test@gmail.com"
    assert body["role"] == "Owner"
    assert "id" in body
