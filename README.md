# DatasheetHub

**DatasheetHub** is an open-source, modular backend architecture designed for automated electronics research, component discovery, direct CDN datasheet streaming, and PCB circuit synthesis.

---

## Clean Architecture & Folder Structure

```
datasheet-cli/
├── docs/                        # Architecture & API documentation
│   └── architecture.md
├── src/datasheet_hub/           # Core package
│   ├── api/                     # REST API layer (FastAPI)
│   │   ├── app.py               # Application factory & CORS
│   │   └── routes/              # Modular route controllers
│   │       ├── parts.py         # Component search & detail endpoints
│   │       └── datasheets.py    # CDN resolution & CORS-free proxy streaming
│   ├── catalog/                 # Layer 1: Component Catalog & Resolvers
│   │   ├── models.py            # Pydantic domain models
│   │   ├── service.py           # CatalogService coordinator
│   │   └── providers/           # Distributor and CDN integrations
│   │       ├── base.py          # Abstract provider interface
│   │       ├── lcsc.py          # LCSC / JLCPCB 2-hop direct CDN resolver
│   │       └── ti.py            # Texas Instruments deterministic CDN
│   ├── extraction/              # Layer 2: PDF Parsing & Circuit Extraction (Planned)
│   ├── synthesis/               # Layer 3 & 4: Math Solvers & KiCad Generation (Planned)
│   └── cli/                     # Developer CLI interface
│       └── main.py              # CLI entrypoint (`dhub` / `datasheet-hub`)
├── tests/                       # Test suite
│   ├── conftest.py              # Pytest fixtures & FastAPI TestClient
│   ├── unit/                    # Fast isolated tests
│   │   └── test_models.py
│   └── integration/             # Live network & API integration tests
│       ├── test_catalog.py
│       └── test_api_endpoints.py
├── pyproject.toml
└── README.md
```

---

## Layer 1: Component Search & Direct CDN Datasheet Resolution

* **0 Local Storage Required:** Resolves direct un-gated cloud CDN PDF URLs (`datasheet.lcsc.com/datasheet/pdf/<hash>.pdf`) in **< 300ms** on-demand without bulk-downloading files.
* **CORS-Free Proxy Stream:** Streams raw PDF bytes directly to web frontend viewers (e.g. `pdf.js` in React) to bypass browser cross-origin blocks.
* **Production REST API:** Native FastAPI server with interactive Swagger documentation.

---

## Quickstart

### 1. Installation
```bash
git clone https://github.com/Ashsishmanchanda/datasheet-cli.git
cd datasheet-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Developer CLI (`dhub`)
```bash
# Search components
dhub search "STM32F405"

# Resolve direct cloud CDN PDF URL
dhub resolve "C15742"
dhub resolve "TPS62160"

# Start the REST API server for your UI
dhub serve --port 8000
```

### 3. REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check probe |
| `GET` | `/api/parts/search?q=STM32F405` | Search components (returns MPN, specs, stock, pricing) |
| `GET` | `/api/parts/{part_id}` | Detailed attributes, price tiers, and product links |
| `GET` | `/api/datasheets/{part_id}` | Returns direct cloud CDN URL (0 bytes stored on server) |
| `GET` | `/api/datasheets/{part_id}/proxy` | Streams raw PDF stream directly to browser viewers |

Interactive API documentation is accessible at `http://127.0.0.1:8000/docs` when running `dhub serve`.
