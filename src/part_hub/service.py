"""Unified PartHub Service: Orchestrates catalog search, direct CDN resolution, and streaming."""

from typing import Dict, List, Optional
import httpx

from part_hub.core.models import DatasheetInfo, PartDetail, PartSummary
from part_hub.providers.lcsc import LCSCProvider
from part_hub.providers.ti import TIProvider


class PartHubService:
    def __init__(self):
        self.lcsc = LCSCProvider()
        self.ti = TIProvider()
        self._url_cache: Dict[str, DatasheetInfo] = {}

    def search(self, query: str, limit: int = 10) -> List[PartSummary]:
        """Search parts across providers (LCSC/JLCPCB first, then vendor CDNs)."""
        # Primary search: LCSC / JLCPCB catalog (covers 100k+ global parts)
        results = self.lcsc.search(query, limit=limit)
        if results:
            return results

        # Fallback to direct TI CDN search
        ti_results = self.ti.search(query, limit=1)
        if ti_results:
            return ti_results

        return []

    def get_detail(self, part_id: str) -> Optional[PartDetail]:
        """Get component metadata and resolve direct CDN PDF link."""
        # Check LCSC
        detail = self.lcsc.get_detail(part_id)
        if detail:
            return detail

        # Check TI
        return self.ti.get_detail(part_id)

    def resolve_datasheet_url(self, part_id: str) -> Optional[DatasheetInfo]:
        """Get the direct, un-gated PDF link for a component (0 bytes stored)."""
        cache_key = part_id.strip().upper()
        if cache_key in self._url_cache:
            return self._url_cache[cache_key]

        # 1. Try LCSC
        info = self.lcsc.resolve_datasheet_url(part_id)
        if not info:
            # 2. Try TI
            info = self.ti.resolve_datasheet_url(part_id)

        if info:
            self._url_cache[cache_key] = info
        return info

    def stream_datasheet(self, direct_cdn_url: str):
        """Stream PDF bytes directly from the CDN to avoid CORS issues in web frontends."""
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
