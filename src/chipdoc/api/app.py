"""FastAPI application factory and middleware configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chipdoc.api.routes.datasheets import router as datasheets_router
from chipdoc.api.routes.parts import router as parts_router


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="DatasheetHub API",
        description="State-of-the-art component discovery and direct CDN datasheet streaming engine.",
        version="1.0.0",
    )

    # Enable CORS for browser frontends (React, Vite, Next.js, Vue)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register modular routers
    app.include_router(parts_router)
    app.include_router(datasheets_router)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok", "service": "DatasheetHub"}

    return app


app = create_app()

