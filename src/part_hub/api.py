"""FastAPI application providing REST endpoints for UI integration."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from part_hub.core.models import DatasheetInfo, PartDetail, PartSummary
from part_hub.service import PartHubService

app = FastAPI(
    title="PartHub Datasheet Engine",
    description="Layer 1 Backend: Search electronic components and stream direct CDN datasheets with 0 local storage.",
    version="1.0.0",
)

# Enable CORS for frontend applications (React, Vite, Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = PartHubService()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "PartHub Datasheet Engine"}


@app.get("/api/search", response_model=list[PartSummary])
def search_parts(
    q: str = Query(..., description="Part number, keyword, or description (e.g. STM32F405, TPS62160, NE555)"),
    limit: int = Query(10, ge=1, le=50),
):
    """Search for components across catalogs."""
    results = service.search(q, limit=limit)
    return results


@app.get("/api/parts/{part_id}", response_model=PartDetail)
def get_part_detail(part_id: str):
    """Retrieve full component specifications, pricing, and direct datasheet link."""
    detail = service.get_detail(part_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found")
    return detail


@app.get("/api/datasheets/{part_id}", response_model=DatasheetInfo)
def get_datasheet_url(part_id: str):
    """Resolve and return the un-gated direct CDN PDF link (0 bytes stored on server)."""
    info = service.resolve_datasheet_url(part_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Datasheet for '{part_id}' could not be resolved")
    return info


@app.get("/api/datasheets/{part_id}/proxy")
def proxy_datasheet_pdf(part_id: str):
    """Stream raw PDF bytes to the frontend viewer to eliminate browser CORS restrictions."""
    info = service.resolve_datasheet_url(part_id)
    if not info:
        raise HTTPException(status_code=404, detail=f"Datasheet for '{part_id}' not found")

    return StreamingResponse(
        service.stream_datasheet(info.direct_cdn_url),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{info.mpn}_datasheet.pdf"',
        },
    )
