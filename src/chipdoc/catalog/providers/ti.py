"""Texas Instruments direct deterministic CDN provider."""

import re
from typing import List, Optional
import httpx

from chipdoc.catalog.models import DatasheetInfo, PartDetail, PartSummary
from chipdoc.catalog.providers.base import BaseProvider


class TIProvider(BaseProvider):
    name = "ti"

    CDN_TEMPLATE = "https://www.ti.com/lit/ds/symlink/{part}.pdf"
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self, timeout: float = 6.0):
        self.timeout = timeout
        self.client = httpx.Client(
            headers={"User-Agent": self.USER_AGENT, "Accept": "application/pdf,*/*"},
            timeout=self.timeout,
            follow_redirects=True,
        )

    def search(self, query: str, limit: int = 10) -> List[PartSummary]:
        clean = re.sub(r"[^A-Za-z0-9]", "", query).lower()
        info = self.resolve_datasheet_url(clean)
        if info:
            return [
                PartSummary(
                    part_id=clean.upper(),
                    mpn=clean.upper(),
                    manufacturer="Texas Instruments",
                    description=f"Texas Instruments {clean.upper()}",
                    datasheet_url=info.direct_cdn_url,
                    source="ti",
                )
            ]
        return []

    def get_detail(self, part_id: str) -> Optional[PartDetail]:
        info = self.resolve_datasheet_url(part_id)
        if not info:
            return None
        return PartDetail(
            part_id=info.part_id,
            mpn=info.mpn,
            manufacturer="Texas Instruments",
            datasheet_url=info.direct_cdn_url,
            product_url=f"https://www.ti.com/product/{info.part_id}",
            source="ti",
        )

    def resolve_datasheet_url(self, part_id_or_mpn: str) -> Optional[DatasheetInfo]:
        clean = re.sub(r"[^A-Za-z0-9]", "", part_id_or_mpn).lower()
        url = self.CDN_TEMPLATE.format(part=clean)
        try:
            resp = self.client.head(url)
            if resp.status_code == 200 and "pdf" in resp.headers.get("content-type", "").lower():
                length = int(resp.headers.get("Content-Length", 0)) or None
                return DatasheetInfo(
                    part_id=clean.upper(),
                    mpn=clean.upper(),
                    direct_cdn_url=url,
                    content_type="application/pdf",
                    content_length_bytes=length,
                )
        except Exception:
            pass
        return None

