def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


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

