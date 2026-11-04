# datasheet-cli

**`datasheet-cli`** is an automated pipeline that bridges the gap between component datasheets (TI, STMicroelectronics, ADI, etc.) and ready-to-merge PCB schematics (KiCad).

## Problem Statement
Hardware designers spend countless hours manually reading 80+ page datasheets to:
1. Locate the **"Typical Application Circuit"** or reference design.
2. Find the mathematical formulas for external passives (feedback dividers, inductors, bootstrap capacitors).
3. Re-draw the schematic symbols, pins, and nets by hand in KiCad.

`datasheet-cli` automates this entire flow:
```
[MPN / Query: e.g. TPS54302]
         │
         ▼ 1. Fetch
[Download Datasheet PDF & Pinout Metadata]
         │
         ▼ 2. Parse & Segment
[Locate "Typical Application" + "Design Procedure" + Pin Tables]
         │
         ▼ 3. Extract & Reason
[Extract Vector/Raster Schematics + Read Design Formulas via Vision/LLM]
         │
         ▼ 4. Solve Passives
[Compute E96 standard resistor values, L/C ratings for target specs]
         │
         ▼ 5. Export
[Output KiCad Schematics (.kicad_sch), Netlists (JSON/TOKN), or SKiDL code]
```

---

## Architecture

- **`fetcher`**: Retrieves component datasheets, pin counts, and package types given a Manufacturer Part Number (MPN).
- **`parser`**: PDF layout analyzer that detects and crops schematic diagrams and design procedure sections (using PyMuPDF / Surya / Marker).
- **`extractor`**: Extracts pin connectivity, component designators, netlists, and formula variables.
- **`solver`**: Evaluates circuit equations and calculates standard passive component values based on target input/output parameters.
- **`exporter`**: Generates KiCad schematics (`.kicad_sch`), SKiDL Python scripts, or structured JSON netlists.

---

## Quickstart

### Prerequisites
- Python 3.10+
- (Optional) KiCad 8+ for opening and validating generated schematics

### Installation
```bash
git clone https://github.com/<your-username>/datasheet-cli.git
cd datasheet-cli
pip install -e .
```

### CLI Usage (Planned)
```bash
# 1. Fetch datasheet for a specific part
datasheet-cli fetch TPS54302DDCR

# 2. Extract reference schematic and pinout
datasheet-cli extract TPS54302DDCR --target-vout 3.3 --target-iout 2.0

# 3. Export directly to KiCad schematic
datasheet-cli generate TPS54302DDCR -o ./output/tps54302_buck.kicad_sch
```
