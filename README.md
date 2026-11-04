# dlogex

**`dlogex`** (Datasheet Logic Extractor) is an open-source EDA backend platform designed for automated electronic component discovery, direct cloud CDN datasheet streaming, and PCB circuit synthesis.

---

## Clean Architecture & Folder Structure

```text
dlogex/
├── docs/                                  # Technical specifications & roadmap
│   └── architecture.md
├── src/datasheet_hub/                     # Core package
│   ├── api/                               # REST API layer (FastAPI)
│   │   ├── app.py                         # Application factory, CORS, and health check
│   │   └── routes/                        # Decoupled endpoint routers
│   │       ├── parts.py                   # /api/parts (Search & component details)
│   │       └── datasheets.py              # /api/datasheets (Direct CDN & streaming proxy)
│   ├── catalog/                           # Layer 1: Component Discovery & Resolvers
│   │   ├── models.py                      # Pydantic schemas (PartSummary, PartDetail, DatasheetInfo)
│   │   ├── service.py                     # Catalog coordinator & memory streaming
│   │   └── providers/                     # Data source integrations
│   │       ├── base.py                    # Standardized abstract provider interface
│   │       ├── lcsc.py                    # LCSC / JLCPCB 2-hop cloud CDN resolver
│   │       └── ti.py                      # Texas Instruments deterministic CDN provider
│   ├── extraction/                        # Layer 2: PDF Parsing & Circuit Extraction (Planned)
│   ├── synthesis/                         # Layer 3 & 4: Math Solver & KiCad Generator (Planned)
│   └── cli/                               # Developer & scripting CLI (`dlogex` / `dhub`)
│       └── main.py                        # Terminal commands: search, resolve, serve
├── tests/                                 # Complete automated test suite
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

## Layer 1: Component Search & Direct CDN Datasheet Resolution

* **0 Local Storage Required:** Resolves direct un-gated cloud CDN PDF URLs (`datasheet.lcsc.com/datasheet/pdf/<hash>.pdf`) in **< 300ms** on-demand without hoarding static files.
* **CORS-Free Proxy Stream:** Streams raw PDF bytes directly to web frontend viewers (e.g. `pdf.js` in React) to bypass browser cross-origin blocks.
* **Production REST API:** Native FastAPI server with interactive Swagger documentation.

---

## Quickstart

### 1. Installation
```bash
git clone https://github.com/Ashsishmanchanda/dlogex.git
cd dlogex
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Developer CLI (`dlogex`)
```bash
# Search components
dlogex search "STM32F405"

# Resolve direct cloud CDN PDF URL
dlogex resolve "C15742"
dlogex resolve "TPS62160"

# Start the REST API server for your UI
dlogex serve --port 8000
```

### 3. REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check probe |
| `GET` | `/api/parts/search?q=STM32F405` | Search components (returns MPN, specs, stock, pricing) |
| `GET` | `/api/parts/{part_id}` | Detailed attributes, price tiers, and product links |
| `GET` | `/api/datasheets/{part_id}` | Returns direct cloud CDN URL (0 bytes stored on server) |
| `GET` | `/api/datasheets/{part_id}/proxy` | Streams raw PDF stream directly to browser viewers |

Interactive API documentation is accessible at `http://127.0.0.1:8000/docs` when running `dlogex serve`.
