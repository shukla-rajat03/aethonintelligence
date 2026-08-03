def test_cache_stats_requires_auth(client):
    resp = client.get("/api/v1/cache/stats")
    assert resp.status_code == 401


def test_cache_stats_authenticated(client, auth_headers):
    resp = client.get("/api/v1/cache/stats", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    for key in ("hits", "misses", "hit_rate", "total_savings", "cache_size", "evictions"):
        assert key in body
