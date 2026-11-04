"""Abstract base provider for component catalog search and datasheet resolution."""

from abc import ABC, abstractmethod
from typing import List, Optional
from part_hub.core.models import PartSummary, PartDetail, DatasheetInfo


class BaseProvider(ABC):
    """Abstract interface for component distributors and vendor CDNs."""

    name: str = "base"

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[PartSummary]:
        """Search parts by MPN, keyword, or description."""
        pass

    @abstractmethod
    def get_detail(self, part_id: str) -> Optional[PartDetail]:
        """Fetch detailed attributes, price breaks, and datasheet URLs."""
        pass

    @abstractmethod
    def resolve_datasheet_url(self, part_id_or_mpn: str) -> Optional[DatasheetInfo]:
        """Resolve a part identifier to its direct raw CDN PDF link."""
        pass
