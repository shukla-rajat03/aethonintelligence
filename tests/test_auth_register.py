def test_register_missing_all_fields(client):
    resp = client.post("/api/v1/auth/register", json={})
    assert resp.status_code == 422
    missing = {e["loc"][-1] for e in resp.json()["detail"]}
    assert {"name", "email", "password", "orgName", "orgType"} <= missing


def test_register_invalid_email_format(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "name": "QA Bot",
            "email": "not-an-email",
            "password": "SomeStrongPass123",
            "orgName": "QA Org",
            "orgType": "solo",
        },
    )
    assert resp.status_code == 422


def test_register_existing_email_does_not_create_duplicate_account(client):
    # Account-enumeration check: registering with an email that is already
    # in use must not silently create/overwrite an account or leak whether
    # the account exists via a distinctly different error than validation errors.
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Duplicate Test",
            "email": "test@gmail.com",
            "password": "AnotherStrongPass123",
            "orgName": "Duplicate Org",
            "orgType": "solo",
        },
    )
    assert resp.status_code in (400, 409, 422)
    # The original account must still authenticate with its original password.
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "test@gmail.com", "password": "test@gmail.com"},
    )
    assert login_resp.status_code == 200


def test_register_missing_password(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "name": "QA Bot",
            "email": "qa-register-probe@example.com",
            "orgName": "QA Org",
            "orgType": "solo",
        },
    )
    assert resp.status_code == 422


def test_register_invalid_org_type(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "name": "QA Bot",
            "email": "qa-register-probe-2@example.com",
            "password": "SomeStrongPass123",
            "orgName": "QA Org",
            "orgType": "not-a-real-type",
        },
    )
    assert resp.status_code == 422
