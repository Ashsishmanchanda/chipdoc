# PartHub — Layer 1 Component Search & Datasheet CDN Resolver

PartHub is a lean, state-of-the-art backend service designed to power hardware and EDA applications. It resolves electronic component datasheets directly from high-speed distributor and vendor CDNs (LCSC/JLCPCB, Texas Instruments) with **zero local storage required**.

---

## The First-Principles Solution to Layer 1

* **No Bulk Downloading:** Does not hoard terabytes of static PDFs.
* **Direct Cloud CDN Streaming:** Resolves the exact Alibaba Cloud/AWS CDN link (`datasheet.lcsc.com/datasheet/pdf/<hash>.pdf`) on demand in **< 300ms**.
* **Zero-CORS Web Proxy:** Provides a streaming proxy endpoint so frontend React/Vue PDF viewers (e.g. `pdf.js`) can render any datasheet in-browser without CORS errors.
* **REST API & Swagger Docs:** Native FastAPI backend ready to plug into any UI.

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

### 2. CLI Usage

```bash
# Search across 100,000+ components
part-hub search "STM32F405"

# Resolve direct un-gated CDN PDF URL
part-hub resolve "C15742"
part-hub resolve "TPS62160"

# Start the REST API server for your UI
part-hub serve --port 8000
```

---

## REST API Endpoints (For Your UI)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/search?q=STM32F405` | Search components (returns part ID, MPN, specs, stock, pricing). |
| `GET` | `/api/parts/{part_id}` | Detailed attributes, price tiers, and direct datasheet link. |
| `GET` | `/api/datasheets/{part_id}` | Returns direct CDN URL (0 bytes stored on your backend). |
| `GET` | `/api/datasheets/{part_id}/proxy` | Streams raw PDF stream directly to browser viewers (CORS-free). |

Interactive API documentation available at `http://localhost:8000/docs` when running `part-hub serve`.

---

## Architecture

```
[UI / User Search]
        │
        ▼ (FastAPI /api/search)
  [PartHub Service]
        │
        ├─► [LCSC / JLCPCB 2-Hop Resolver] ──► datasheet.lcsc.com/datasheet/pdf/...
        └─► [TI Deterministic CDN]          ──► ti.com/lit/ds/symlink/...
```
