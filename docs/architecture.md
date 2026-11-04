# DatasheetHub Architecture

DatasheetHub is designed from first principles as an end-to-end electronics design platform, broken down into 4 clear decoupled layers:

```
[Web / Desktop UI]
        │
        ▼ (FastAPI / REST / SSE)
┌────────────────────────────────────────────────────────┐
│                   DATASHEETHUB CORE                    │
├────────────────────────────────────────────────────────┤
│ Layer 1: Catalog & Direct CDN Datasheet Resolution     │
│   - Multi-vendor search (LCSC/JLCPCB, Texas Inst.)     │
│   - Direct CDN extraction (0 local storage)            │
│   - CORS-free PDF streaming proxy                      │
├────────────────────────────────────────────────────────┤
│ Layer 2: Document & Circuit Extraction (Planned)       │
│   - PyMuPDF vector/layout parsing                      │
│   - Typical Application circuit detection              │
│   - Multi-modal LLM netlist & pin recovery             │
├────────────────────────────────────────────────────────┤
│ Layer 3: Parametric Math & Rules (Planned)             │
│   - Feedback divider and passive calculators           │
│   - E96 resistor table snapping                        │
│   - Decoupling capacitor proximity checks              │
├────────────────────────────────────────────────────────┤
│ Layer 4: EDA Synthesis & Export (Planned)              │
│   - KiCad 8+ S-Expression generation (.kicad_sch)      │
│   - Netlist (JSON / TOKN) export                       │
└────────────────────────────────────────────────────────┘
```

## Directory Layout

* `src/datasheet_hub/api/`: FastAPI web server and route controllers (`parts.py`, `datasheets.py`).
* `src/datasheet_hub/catalog/`: Layer 1 engine and distributor providers (`lcsc.py`, `ti.py`).
* `src/datasheet_hub/extraction/`: Layer 2 document vision and netlist extraction models.
* `src/datasheet_hub/synthesis/`: Layer 3 & 4 math solvers and KiCad generator.
* `src/datasheet_hub/cli/`: Command-line tools for developers (`dhub`).
* `tests/unit/`: Fast unit tests for models and offline logic.
* `tests/integration/`: Network tests against live distributor endpoints and API routes.

