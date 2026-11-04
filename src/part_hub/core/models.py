"""Data models for component search, metadata, and direct datasheet URLs."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PriceBreak(BaseModel):
    quantity: int
    unit_price_usd: float


class PartSummary(BaseModel):
    part_id: str  # e.g., "C15742" or "STM32F405RGT6"
    mpn: str  # Manufacturer Part Number
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    package: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = 0
    price_usd: Optional[float] = None
    datasheet_url: Optional[str] = None  # Direct CDN URL
    source: str = "lcsc"


class PartDetail(BaseModel):
    part_id: str
    mpn: str
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    package: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    stock: Optional[int] = 0
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
