def test_search_stm32(catalog_service):
    results = catalog_service.search("STM32F405", limit=5)
    assert len(results) > 0
    top = results[0]
    assert "STM32F405" in top.mpn
    assert top.part_id.startswith("C")


def test_resolve_lcsc_direct_cdn(catalog_service):
    # STM32F405RGT6 (C15742)
    info = catalog_service.resolve_datasheet_url("C15742")
    assert info is not None
    assert "datasheet.lcsc.com/datasheet/pdf/" in info.direct_cdn_url
    assert info.direct_cdn_url.endswith(".pdf")
    assert info.content_length_bytes is not None
    assert info.content_length_bytes > 1_000_000


def test_resolve_rp2040(catalog_service):
    # RP2040 (C2040)
    info = catalog_service.resolve_datasheet_url("C2040")
    assert info is not None
    assert "datasheet.lcsc.com/datasheet/pdf/" in info.direct_cdn_url


def test_resolve_ti_powerchip(catalog_service):
    # TI TPS62160
    info = catalog_service.resolve_datasheet_url("TPS62160")
    assert info is not None
    assert info.direct_cdn_url.endswith(".pdf")
    assert any(domain in info.direct_cdn_url for domain in ["datasheet.lcsc.com", "ti.com"])

