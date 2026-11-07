"""Domain data models for component catalog and datasheet resolution."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PriceBreak(BaseModel):
    quantity: int = Field(..., description="Minimum order quantity for this price tier")
    unit_price_usd: float = Field(..., description="Unit price in USD")


class PartSummary(BaseModel):
    part_id: str = Field(..., description="Unique distributor part ID (e.g. C15742)")
    mpn: str = Field(..., description="Manufacturer Part Number")
    manufacturer: Optional[str] = Field(None, description="Component manufacturer")
    description: Optional[str] = Field(None, description="Brief technical summary")
    package: Optional[str] = Field(None, description="SMD/Through-hole footprint package")
    category: Optional[str] = Field(None, description="Primary/Secondary component category")
    library_type: Optional[str] = Field(None, description="JLCPCB library type: Basic vs Extended")
    stock: int = Field(0, description="Available stock quantity")
    price_usd: Optional[float] = Field(None, description="Base unit price for qty 1+")
    datasheet_url: Optional[str] = Field(None, description="Direct CDN PDF link if pre-resolved")
    source: str = Field("lcsc", description="Catalog provider name (e.g. lcsc, ti)")


class PartDetail(BaseModel):
    part_id: str
    mpn: str
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    package: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    library_type: Optional[str] = None  # "Basic" or "Extended"
    stock: int = 0
    price_breaks: List[PriceBreak] = Field(default_factory=list)
    attributes: Dict[str, str] = Field(default_factory=dict)
    datasheet_url: Optional[str] = None  # Direct un-gated CDN PDF URL
    product_url: Optional[str] = None
    source: str = "lcsc"


class DatasheetInfo(BaseModel):
    part_id: str
    mpn: str
    direct_cdn_url: str
    content_type: str = "application/pdf"
    content_length_bytes: Optional[int] = None

