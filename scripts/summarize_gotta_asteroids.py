#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.time import Time


def text_array(values) -> list[str]:
    out = []
    for value in values:
        if isinstance(value, (bytes, np.bytes_)):
            out.append(value.decode("utf-8", errors="ignore").strip())
        else:
            out.append(str(value).strip())
    return out


def numeric_summary(values) -> dict[str, float | int | None]:
    arr = np.asarray(values, dtype=float)
    good = np.isfinite(arr)
    if not np.any(good):
        return {"n": 0, "min": None, "p16": None, "median": None, "mean": None, "p84": None, "max": None}
    vals = arr[good]
    return {
        "n": int(vals.size),
        "min": float(np.min(vals)),
        "p16": float(np.percentile(vals, 16)),
        "median": float(np.median(vals)),
        "mean": float(np.mean(vals)),
        "p84": float(np.percentile(vals, 84)),
        "max": float(np.max(vals)),
    }


def markdown_table(rows: list[tuple[str, int]], headers: tuple[str, str]) -> list[str]:
    lines = [f"| {headers[0]} | {headers[1]} |", "|---|---:|"]
    lines.extend(f"| {name or 'Unknown'} | {count} |" for name, count in rows)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize GOTTA known-asteroid FITS detections.")
    parser.add_argument("fits_path", nargs="?", default="gotta_asteroids.fits")
    parser.add_argument("--md-out", default="docs/GOTTA_STATS.md")
    parser.add_argument("--json-out", default="outputs/gotta/gotta_stats.json")
    args = parser.parse_args()

    fits_path = Path(args.fits_path)
    with fits.open(fits_path, memmap=True) as hdul:
        data = hdul[1].data
        columns = data.names
        n_rows = len(data)
        arrays = {name: np.asarray(data[name]) for name in columns}

    query_ids = text_array(arrays["query_id"])
    names = text_array(arrays["name"])
    source_files = text_array(arrays["source_file"])
    classes = text_array(arrays["object_orbit_class_name"])
    horizons_failed = np.asarray(arrays["horizons_failed"], dtype=bool) if "horizons_failed" in arrays else np.zeros(n_rows, dtype=bool)

    epochs = np.asarray(arrays["epoch"], dtype=float)
    good_epoch = np.isfinite(epochs)
    if np.any(good_epoch):
        times = Time(epochs[good_epoch], format="mjd", scale="utc")
        date_start = str(times.min().isot)
        date_end = str(times.max().isot)
        nights = sorted(set(times.datetime64.astype("datetime64[D]").astype(str)))
    else:
        date_start = date_end = ""
        nights = []

    object_counts = Counter(query_ids)
    class_counts = Counter(classes)
    detections_per_object = np.asarray(list(object_counts.values()), dtype=float)

    numeric_cols = [
        "mag",
        "Mag_Kron",
        "ang_rate_arcsec_hour",
        "ang_rate_deg_day",
        "r_AU",
        "delta_AU",
        "phase_deg",
    ]
    numeric = {name: numeric_summary(arrays[name]) for name in numeric_cols if name in arrays}
    numeric["detections_per_object"] = numeric_summary(detections_per_object)

    summary = {
        "fits_path": str(fits_path),
        "rows": int(n_rows),
        "columns": int(len(columns)),
        "unique_query_id": int(len(set(query_ids))),
        "unique_name": int(len(set(names))),
        "unique_source_file": int(len(set(source_files))),
        "date_start_utc": date_start,
        "date_end_utc": date_end,
        "n_nights": int(len(nights)),
        "horizons_failed_rows": int(horizons_failed.sum()),
        "class_counts": dict(class_counts.most_common()),
        "numeric": numeric,
    }

    md_lines = [
        "# GOTTA Known-Asteroid Statistics",
        "",
        f"Source file: `{fits_path}`",
        "",
        "## Basic Counts",
        "",
        f"- Detection rows: `{n_rows}`",
        f"- Columns: `{len(columns)}`",
        f"- Unique `query_id`: `{len(set(query_ids))}`",
        f"- Unique `name`: `{len(set(names))}`",
        f"- Unique source files: `{len(set(source_files))}`",
        f"- UTC epoch range: `{date_start}` to `{date_end}`",
        f"- Number of UTC dates represented by `epoch`: `{len(nights)}`",
        f"- JPL Horizons failed rows: `{int(horizons_failed.sum())}`",
        "",
        "## Orbit Class Counts",
        "",
        *markdown_table(class_counts.most_common(), ("Orbit class", "Detections")),
        "",
        "## Numeric Columns",
        "",
        "| Column | N | Min | P16 | Median | Mean | P84 | Max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, stats in numeric.items():
        md_lines.append(
            f"| `{name}` | {stats['n']} | {stats['min']:.6g} | {stats['p16']:.6g} | "
            f"{stats['median']:.6g} | {stats['mean']:.6g} | {stats['p84']:.6g} | {stats['max']:.6g} |"
        )

    md_path = Path(args.md_out)
    json_path = Path(args.json_out)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()

