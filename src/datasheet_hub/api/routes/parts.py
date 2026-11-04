"""API endpoints for part search and component details."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from datasheet_hub.catalog.models import PartDetail, PartSummary
from datasheet_hub.catalog.service import CatalogService

router = APIRouter(prefix="/api/parts", tags=["Parts"])


_shared_service = CatalogService()


def get_service() -> CatalogService:
    return _shared_service


@router.get("/search", response_model=List[PartSummary])
def search_parts(
    q: str = Query(..., min_length=1, description="Part number or keyword (e.g. STM32F405, RP2040, TPS62160)"),
    limit: int = Query(10, ge=1, le=50, description="Max results to return"),
    service: CatalogService = Depends(get_service),
):
    """Search for components across distributor and manufacturer catalogs."""
    return service.search(q, limit=limit)


@router.get("/{part_id}", response_model=PartDetail)
def get_part_detail(
    part_id: str,
    service: CatalogService = Depends(get_service),
):
    """Retrieve full parametric attributes, price breaks, and pre-resolved datasheet link."""
    detail = service.get_detail(part_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found in catalog")
    return detail
