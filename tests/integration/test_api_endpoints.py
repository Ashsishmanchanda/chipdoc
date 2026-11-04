def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert resp.json()["service"] == "chipdoc"


def test_api_search(client):
    resp = client.get("/api/parts/search", params={"q": "STM32F405", "limit": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert "STM32F405" in data[0]["mpn"]


def test_api_resolve_datasheet(client):
    resp = client.get("/api/datasheets/C15742")
    assert resp.status_code == 200
    data = resp.json()
    assert data["part_id"] == "C15742"
    assert "datasheet.lcsc.com/datasheet/pdf/" in data["direct_cdn_url"]


def test_api_proxy_stream(client):
    # Tests the CORS-free streaming proxy (reads first 1KB of PDF)
    resp = client.get("/api/datasheets/C15742/proxy")
    assert resp.status_code == 200
    assert "application/pdf" in resp.headers.get("content-type", "")
    assert resp.content.startswith(b"%PDF")
