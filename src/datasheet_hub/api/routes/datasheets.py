"""API endpoints for resolving direct CDN datasheet links and CORS-free streaming."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from datasheet_hub.catalog.models import DatasheetInfo
from datasheet_hub.catalog.service import CatalogService

router = APIRouter(prefix="/api/datasheets", tags=["Datasheets"])


from datasheet_hub.api.routes.parts import get_service


@router.get("/{part_id}", response_model=DatasheetInfo)
def resolve_datasheet_url(
    part_id: str,
    service: CatalogService = Depends(get_service),
):
    """Resolve and return direct cloud CDN PDF URL for a component (0 bytes stored)."""
    info = service.resolve_datasheet_url(part_id)
    if not info:
        raise HTTPException(
            status_code=404,
            detail=f"Datasheet for component '{part_id}' could not be resolved",
        )
    return info


@router.get("/{part_id}/proxy")
def proxy_datasheet_pdf(
    part_id: str,
    service: CatalogService = Depends(get_service),
):
    """Stream raw PDF bytes to web frontend PDF viewers without browser CORS errors."""
    info = service.resolve_datasheet_url(part_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Datasheet for '{part_id}' not found")

    return StreamingResponse(
        service.stream_pdf(info.direct_cdn_url),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{info.mpn}_datasheet.pdf"',
        },
    )
