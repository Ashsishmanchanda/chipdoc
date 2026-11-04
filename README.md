# chipdoc

**`chipdoc`** is an ultra-fast, zero-storage backend engine for electronic component discovery, direct cloud CDN datasheet resolution, and CORS-free PDF streaming.

---

## What `chipdoc` Does

* **Direct Cloud CDN Streaming:** Resolves the exact cloud CDN PDF link (e.g., `datasheet.lcsc.com/datasheet/pdf/<hash>.pdf` or `ti.com/lit/ds/symlink/<part>.pdf`) in **< 300ms**.
* **Zero Local Storage Required:** Does not hoard static PDFs on disk. Everything is resolved and streamed on-demand.
* **CORS-Free PDF Proxy:** Exposes a streaming proxy endpoint (`/api/datasheets/{part_id}/proxy`) so browser PDF viewers (like `pdf.js` in React/Vue/Svelte) can render any datasheet without cross-origin blocks.
* **Production REST API:** Native FastAPI server with interactive Swagger UI.

---

## Clean Architecture

```text
chipdoc/
├── src/chipdoc/                           # Core package
│   ├── api/                               # REST API layer (FastAPI)
│   │   ├── app.py                         # Application factory & CORS
│   │   └── routes/                        # Decoupled endpoint routers
│   │       ├── parts.py                   # /api/parts (Search & component details)
│   │       └── datasheets.py              # /api/datasheets (Direct CDN & streaming proxy)
│   ├── catalog/                           # Component Discovery & Resolvers
│   │   ├── models.py                      # Pydantic schemas (PartSummary, PartDetail, DatasheetInfo)
│   │   ├── service.py                     # Catalog coordinator & memory streaming
│   │   └── providers/                     # Data source integrations
│   │       ├── base.py                    # Standardized abstract provider interface
│   │       ├── lcsc.py                    # LCSC / JLCPCB 2-hop cloud CDN resolver
│   │       └── ti.py                      # Texas Instruments deterministic CDN provider
│   └── cli/                               # Developer CLI (`chipdoc`)
│       └── main.py                        # Terminal commands: search, resolve, serve
├── tests/                                 # Automated test suite
│   ├── conftest.py                        # Shared fixtures & FastAPI TestClient
│   ├── unit/                              # Fast isolated offline tests
│   │   └── test_models.py
│   └── integration/                       # Live network & API integration tests
│       ├── test_catalog.py                # Live LCSC and TI resolution tests
│       └── test_api_endpoints.py          # FastAPI endpoint integration tests
├── pyproject.toml                         # Standard PEP 621 packaging
└── README.md
```

---

## Quickstart

### 1. Installation
```bash
git clone https://github.com/Ashsishmanchanda/chipdoc.git
cd chipdoc
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Developer CLI (`chipdoc`)
```bash
# Search components across distributor catalogs
chipdoc search "STM32F405"

# Resolve direct un-gated cloud CDN PDF URL
chipdoc resolve "C15742"
chipdoc resolve "TPS62160"

# Start the REST API server for your UI
chipdoc serve --port 8000
```

### 3. REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check probe |
| `GET` | `/api/parts/search?q=STM32F405` | Search components (returns MPN, specs, stock, pricing) |
| `GET` | `/api/parts/{part_id}` | Detailed attributes, price tiers, and product links |
| `GET` | `/api/datasheets/{part_id}` | Returns direct cloud CDN URL (0 bytes stored on server) |
| `GET` | `/api/datasheets/{part_id}/proxy` | Streams raw PDF stream directly to browser viewers |

Interactive API documentation is accessible at `http://127.0.0.1:8000/docs` when running `chipdoc serve`.
