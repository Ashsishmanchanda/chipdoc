"""Catalog Service: Coordinates multi-provider searches, direct CDN resolution, and streaming."""

from typing import Dict, List, Optional
import httpx

from datasheet_hub.catalog.models import DatasheetInfo, PartDetail, PartSummary
from datasheet_hub.catalog.providers.lcsc import LCSCProvider
from datasheet_hub.catalog.providers.ti import TIProvider


class CatalogService:
    def __init__(self):
        self.lcsc = LCSCProvider()
        self.ti = TIProvider()
        self._url_cache: Dict[str, DatasheetInfo] = {}

    def search(self, query: str, limit: int = 10) -> List[PartSummary]:
        """Search parts across catalogs (LCSC first, then TI fallback)."""
        results = self.lcsc.search(query, limit=limit)
        if results:
            return results

        ti_results = self.ti.search(query, limit=1)
        if ti_results:
            return ti_results

        return []

    def get_detail(self, part_id: str) -> Optional[PartDetail]:
        """Retrieve part specifications and direct datasheet link."""
        detail = self.lcsc.get_detail(part_id)
        if detail:
            return detail

        return self.ti.get_detail(part_id)

    def resolve_datasheet_url(self, part_id: str) -> Optional[DatasheetInfo]:
        """Resolve the direct un-gated PDF link for a component (0 bytes stored)."""
        cache_key = part_id.strip().upper()
        if cache_key in self._url_cache:
            return self._url_cache[cache_key]

        info = self.lcsc.resolve_datasheet_url(part_id)
        if not info:
            info = self.ti.resolve_datasheet_url(part_id)

        if info:
            self._url_cache[cache_key] = info
        return info

    def stream_pdf(self, direct_cdn_url: str):
        """Stream PDF bytes from the cloud CDN to eliminate browser CORS blocks."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        with httpx.stream("GET", direct_cdn_url, headers=headers, follow_redirects=True) as r:
            r.raise_for_status()
            for chunk in r.iter_bytes(chunk_size=65536):
                yield chunk

