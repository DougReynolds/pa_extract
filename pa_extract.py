"""
pa_extract.py

Author: Douglas Reynolds
Project: PA Extract — NINA TPPA Polar Alignment Log Parser
License: MIT
Year: 2026
YouTube: https://www.youtube.com/@AstroAF
Website: https://astroaf.space
"""

import pandas as pd
import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Extract first and last PA entries from a TPPA PolarAlignment log"
    )
    parser.add_argument(
        "logfile",
        type=Path,
        help="Path to PolarAlignment log file"
    )

    args = parser.parse_args()
    log_file = args.logfile
    count = 0

    if not log_file.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    records = []

    with log_file.open(encoding="utf-8") as f:
        for line in f:
            if "{" not in line:
                continue

            brace = line.find("{")
            ts = line[:brace].strip(" -")
            json_str = line[brace:]

            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                continue

            data["timestamp"] = ts
            count += 1
            data["count"] = count
            records.append(data)

    if len(records) < 2:
        raise ValueError("Not enough PA records found in log")

    df = pd.DataFrame(records)

    # Keep only first and last entries
    df_summary = df.iloc[[0, -1]].copy()

    # Convert degrees → arcseconds
    for col in ["AltitudeError", "AzimuthError", "TotalError"]:
        df_summary[col] = df_summary[col] * 3600

    # First row is sentinel (-1), second row is real adjustment count
    df_summary.iloc[0, df_summary.columns.get_loc("count")] = -1
    df_summary.iloc[1, df_summary.columns.get_loc("count")] = count

    # Order columns
    df_summary = df_summary[
        ["timestamp", "count", "AltitudeError", "AzimuthError", "TotalError"]
    ]

    # Output folder
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    out_csv = output_dir / f"{log_file.stem}_summary.csv"
    df_summary.to_csv(out_csv, index=False, header=False)

    print(f"PA summary written to: {out_csv}")

if __name__ == "__main__":
    main()