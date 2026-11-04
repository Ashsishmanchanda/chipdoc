"""FastAPI application factory and middleware configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chipdoc.api.routes.datasheets import router as datasheets_router
from chipdoc.api.routes.parts import router as parts_router


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="chipdoc API",
        description="Fast electronic component discovery, direct cloud CDN datasheet resolution, and CORS-free PDF streaming.",
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
        return {"status": "ok", "service": "chipdoc"}

    return app


app = create_app()

