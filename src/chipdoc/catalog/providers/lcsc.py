"""LCSC / JLCPCB catalog provider with direct Alibaba Cloud OSS CDN PDF resolution."""

import re
from typing import List, Optional
import httpx

from chipdoc.catalog.models import DatasheetInfo, PartDetail, PartSummary, PriceBreak
from chipdoc.catalog.providers.base import BaseProvider


class LCSCProvider(BaseProvider):
    name = "lcsc"

    SEARCH_URL = "https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList/v2"
    DETAIL_URL = "https://cart.jlcpcb.com/shoppingCart/smtGood/getComponentDetail"

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.client = httpx.Client(
            headers={"User-Agent": self.USER_AGENT, "Accept": "application/json, text/plain, */*"},
            timeout=self.timeout,
            follow_redirects=True,
        )

    def search(self, query: str, limit: int = 10) -> List[PartSummary]:
        """Search JLCPCB/LCSC parts catalog by keyword or MPN."""
        payload = {
            "keyword": query.strip(),
            "currentPage": 1,
            "pageSize": min(limit, 50),
        }

        try:
            resp = self.client.post(self.SEARCH_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()

            items = (
                data.get("data", {})
                .get("componentPageInfo", {})
                .get("list", [])
            )
            if not items:
                return []

            results = []
            for item in items[:limit]:
                price_usd = None
                prices = item.get("componentPrices", [])
                if prices:
                    price_usd = prices[0].get("productPrice")

                code = item.get("componentCode", "")
                mpn = item.get("componentModelEn") or code

                lib_type = item.get("componentLibraryType")
                lib_label = "Basic" if lib_type == "base" else "Extended" if lib_type == "expand" else lib_type

                results.append(
                    PartSummary(
                        part_id=code,
                        mpn=mpn,
                        manufacturer=item.get("componentBrandEn"),
                        description=item.get("describe"),
                        package=item.get("componentSpecificationEn"),
                        category=item.get("secondTypeNameEn") or item.get("firstTypeNameEn"),
                        library_type=lib_label,
                        stock=item.get("stockCount", 0),
                        price_usd=price_usd,
                        datasheet_url=None,
                        source="lcsc",
                    )
                )
            return results
        except Exception:
            return []

    def get_detail(self, part_id: str) -> Optional[PartDetail]:
        """Fetch complete component specs and resolve direct datasheet CDN URL."""
        code = part_id.strip().upper()
        if not re.match(r"^C\d+$", code):
            search_results = self.search(code, limit=1)
            if not search_results:
                return None
            code = search_results[0].part_id

        try:
            resp = self.client.get(self.DETAIL_URL, params={"componentCode": code})
            resp.raise_for_status()
            res_data = resp.json().get("data")
            if not res_data:
                return None

            landing_url = res_data.get("dataManualUrl")
            direct_cdn_url = self._resolve_landing_to_cdn(landing_url) if landing_url else None

            price_breaks = []
            for p in res_data.get("prices", []):
                try:
                    price_breaks.append(
                        PriceBreak(
                            quantity=p.get("startNumber", 1),
                            unit_price_usd=p.get("productPrice", 0.0),
                        )
                    )
                except Exception:
                    continue

            attributes = {}
            for attr in res_data.get("attributes", []):
                name = attr.get("attribute_name_en") or attr.get("attributeNameEn")
                val = attr.get("attribute_value_name") or attr.get("attributeValueName")
                if name and val:
                    attributes[name] = val

            lib_type = res_data.get("componentLibraryType")
            lib_label = "Basic" if lib_type == "base" else "Extended" if lib_type == "expand" else lib_type

            return PartDetail(
                part_id=code,
                mpn=res_data.get("componentModelEn") or code,
                manufacturer=res_data.get("componentBrandEn"),
                description=res_data.get("describe"),
                package=res_data.get("componentSpecificationEn"),
                category=res_data.get("firstSortName"),
                subcategory=res_data.get("secondSortName"),
                library_type=lib_label,
                stock=res_data.get("stockCount", 0),
                price_breaks=price_breaks,
                attributes=attributes,
                datasheet_url=direct_cdn_url,
                product_url=res_data.get("lcscGoodsUrl"),
                source="lcsc",
            )
        except Exception:
            return None

    def resolve_datasheet_url(self, part_id_or_mpn: str) -> Optional[DatasheetInfo]:
        """Resolve a part number to its raw, un-gated PDF link on datasheet.lcsc.com."""
        detail = self.get_detail(part_id_or_mpn)
        if not detail or not detail.datasheet_url:
            return None

        length = None
        try:
            head_resp = self.client.head(detail.datasheet_url, timeout=5.0)
            if head_resp.status_code == 200:
                length = int(head_resp.headers.get("Content-Length", 0)) or None
        except Exception:
            pass

        return DatasheetInfo(
            part_id=detail.part_id,
            mpn=detail.mpn,
            direct_cdn_url=detail.datasheet_url,
            content_type="application/pdf",
            content_length_bytes=length,
        )

    def _resolve_landing_to_cdn(self, landing_url: str) -> Optional[str]:
        """Resolve LCSC's HTML viewer landing page to the underlying Alibaba OSS PDF link."""
        try:
            resp = self.client.get(landing_url, timeout=6.0)
            if resp.status_code != 200:
                return None

            html = resp.text
            matches = re.findall(
                r"https://datasheet\.lcsc\.com/datasheet/pdf/[a-f0-9]+\.pdf",
                html,
            )
            if matches:
                return matches[0]

            fallback = re.findall(r"https://datasheet\.lcsc\.com/[^\"\'\s<>]+\.pdf", html)
            if fallback:
                return fallback[0].split("?")[0]
        except Exception:
            pass
        return None

