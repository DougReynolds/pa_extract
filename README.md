# PA Extract — NINA TPPA Polar Alignment Log Parser

## Overview

`pa_extract.py` is a small utility script that parses **NINA TPPA (Three Point Polar Alignment)** log files and extracts the meaningful polar alignment states needed for long-term analysis.

Instead of manually logging polar alignment values or relying on intuition, this script turns TPPA’s existing logs into clean, repeatable CSV summaries that can be used for:

- Long-term polar alignment stability tracking  
- Pier-mounted mount drift analysis  
- Before/after comparison of mechanical changes  
- Data-driven diagnosis of ALT vs AZ behavior  

<p align="center">
  <a href="https://youtu.be/pUJI16hSdoE">
    <img src="./astrophotography_gear_whispering_thumb.jpg" alt="Polar Alignment Analysis Video">
  </a>
  <a href="https://youtu.be/pUJI16hSdoE">Related Video by AstroAF</a>
</p>

The goal is simple:  
**turn polar alignment from a subjective task into a measurable system characteristic.**

---

## Why This Exists

NINA’s TPPA plugin already logs detailed polar alignment data for every adjustment step, including:

- Altitude error  
- Azimuth error  
- Total polar alignment error  
- Timestamp  

However, those logs are verbose and not immediately usable for session-to-session tracking.

For long-term analysis, what actually matters is:

1. Initial PA error — how far off the mount is at the start of the session  
2. Final PA error — where alignment is left for the next session  
3. Adjustment / solve count — how much effort it took to get there  

`pa_extract.py` automatically extracts exactly those values.

---

## What the Script Does

For each TPPA log file, the script:

- Reads the log line-by-line  
- Safely extracts embedded JSON records  
- Identifies:
  - The initial state (before any adjustments)
  - The final solved state
- Converts PA errors from degrees to arcseconds  
- Captures:
  - Timestamp
  - ALT error (arcsec)
  - AZ error (arcsec)
  - Total PA error (arcsec)
  - Adjustment / solve count
- Writes a single-session CSV summary into an output directory  

The original log files can be discarded afterward — the CSV becomes the permanent record.

---
## Dependencies

```md
Dependencies:
- pandas

Installation:
```bash
pip install pandas

## Input Requirements

- NINA with **TPPA logging enabled**
- TPPA log files
- Python 3.x

### Typical TPPA Log Location (Windows)

```
Documents\N.I.N.A\PolarAlignment\
```

Each session generates a log file similar to:

```
YYYY-MM-DD_HH-MM-SS-PolarAlignment.log
```

---

## Usage

From a command prompt or PowerShell:

```
python pa_extract.py <path_to_log_file>
```

Example:

```
python pa_extract.py 2026-02-03_20-32-30-PolarAlignment.log
```

---

## Output

For each input log, the script creates a CSV file in an `output` directory:

```
output/
└── YYYY-MM-DD_HH-MM-SS-PolarAlignment_summary.csv
```

### CSV Contents

Each summary CSV includes:

- Timestamp  
- Initial ALT error (arcsec)  
- Initial AZ error (arcsec)  
- Initial total PA error (arcsec)  
- Final ALT error (arcsec)  
- Final AZ error (arcsec)  
- Final total PA error (arcsec)  
- Adjustment / solve count  

These CSVs are designed for direct import into Excel or Google Sheets.

---

## Recommended Workflow

1. Enable TPPA logging in NINA  
2. Run TPPA normally during polar alignment  
3. After the session:
   - Run `pa_extract.py` on the TPPA log
   - Import the generated CSV into your spreadsheet
4. Repeat per session
5. Use charts to analyze trends over time

---

## Example Use Cases

- Identifying whether ALT or AZ dominates PA correction  
- Validating mechanical changes with before/after data  
- Measuring pier-mounted stability across weeks or months  
- Replacing subjective alignment feel with measurable results  

---

## License

MIT License

Copyright (c) 2026 Doug Reynolds

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
