from datasheet_hub.catalog.models import PartSummary, PartDetail, DatasheetInfo, PriceBreak


def test_part_summary_validation():
    p = PartSummary(
        part_id="C15742",
        mpn="STM32F405RGT6",
        manufacturer="STMicroelectronics",
        stock=2150,
        price_usd=6.82,
    )
    assert p.part_id == "C15742"
    assert p.mpn == "STM32F405RGT6"
    assert p.stock == 2150


def test_datasheet_info_validation():
    info = DatasheetInfo(
        part_id="C15742",
        mpn="STM32F405RGT6",
        direct_cdn_url="https://datasheet.lcsc.com/datasheet/pdf/test.pdf",
        content_length_bytes=5000000,
    )
    assert info.direct_cdn_url.endswith(".pdf")
    assert info.content_length_bytes == 5000000
