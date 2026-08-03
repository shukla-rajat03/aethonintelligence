def test_gateway_info_public(client):
    resp = client.get("/api/v1/gateway")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "Aethon Intelligence Gateway"
    assert body["status"] == "ok"
    assert body["openaiCompatible"] is True
    assert body["keyPrefix"] == "sk-finops-"
    assert body["baseUrl"] == "https://aethonintelligence.in/v1"


def test_models_catalog_public(client):
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    models = resp.json()
    assert isinstance(models, list)
    assert len(models) > 0
    for m in models:
        assert "model" in m
        assert "provider" in m
        assert "input_price_per_1m" in m
        assert "output_price_per_1m" in m
        assert m["input_price_per_1m"] >= 0
        assert m["output_price_per_1m"] >= 0


def test_models_catalog_contains_expected_providers(client):
    resp = client.get("/v1/models")
    providers = {m["provider"] for m in resp.json()}
    assert "OpenAI" in providers
    assert "Anthropic" in providers
