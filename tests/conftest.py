import os
import time

import httpx
import pytest

BASE_URL = os.environ.get("BASE_URL", "https://aethonintelligence.in")
TEST_USERNAME = "test@gmail.com"
TEST_PASSWORD = "test@gmail.com"


class _ThrottledTransport(httpx.BaseTransport):
    def __init__(self, inner, min_interval=0.3):
        self._inner = inner
        self._gap = min_interval
        self._last = 0.0

    def handle_request(self, request):
        wait = self._gap - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()
        return self._inner.handle_request(request)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def client(base_url):
    with httpx.Client(
        base_url=base_url,
        timeout=30.0,
        follow_redirects=True,
        verify=False,
        transport=_ThrottledTransport(httpx.HTTPTransport()),
    ) as c:
        yield c


@pytest.fixture(scope="session")
def auth_token(client):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
