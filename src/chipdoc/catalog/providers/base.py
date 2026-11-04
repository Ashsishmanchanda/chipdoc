"""Abstract base class for all component catalog providers."""

from abc import ABC, abstractmethod
from typing import List, Optional
from chipdoc.catalog.models import DatasheetInfo, PartDetail, PartSummary


class BaseProvider(ABC):
    """Standardized provider interface for distributor APIs and vendor CDNs."""

    name: str = "base"

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[PartSummary]:
        """Search parts by MPN, keyword, or description."""
        pass

    @abstractmethod
    def get_detail(self, part_id: str) -> Optional[PartDetail]:
        """Fetch full parametric attributes, price tiers, and datasheet links."""
        pass

    @abstractmethod
    def resolve_datasheet_url(self, part_id_or_mpn: str) -> Optional[DatasheetInfo]:
        """Resolve a component directly to its raw, un-gated CDN PDF URL."""
        pass

