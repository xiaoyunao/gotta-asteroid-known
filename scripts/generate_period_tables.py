#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

from generate_paper_products import add_derived, load_table


def latex_escape(value) -> str:
    text = str(value)
    if "$" in text or "\\" in text:
        return text.replace("%", r"\%")
    return text.replace("_", r"\_").replace("%", r"\%")


def fmt_float(value, ndigits: int) -> str:
    if pd.isna(value):
        return "--"
    return f"{float(value):.{ndigits}f}"


def fmt_delta_p(value) -> str:
    if pd.isna(value):
        return "--"
    value = float(value)
    if 0 <= value < 1e-4:
        return r"$<0.0001$"
    return f"{value:.4f}"


def quality_label(value) -> str:
    text = str(value).strip().lower()
    mapping = {
        "reliable": "Rel.",
        "questionable": "Tent.",
        "possible": "Poss.",
        "good": "Good",
    }
    return mapping.get(text, text.capitalize() if text else "--")


def phot_label(value) -> str:
    text = str(value).strip().lower()
    mapping = {
        "apr": "Aper",
        "aper": "Aper",
        "psf": "PSF",
        "kron": "Kron",
    }
    return mapping.get(text, text if text else "--")


def model_label(value) -> str:
    text = str(value).strip()
    if text == "2P":
        return r"$2P$"
    if text == "P":
        return r"$P$"
    return text or "--"


def fetch_sbdb_class(object_id: str) -> str:
    params = urllib.parse.urlencode({"sstr": object_id})
    url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?{params}"
    with urllib.request.urlopen(url, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    orbit_class = payload.get("object", {}).get("orbit_class", {})
    return str(orbit_class.get("code") or "--").strip() or "--"


def build_class_map(fits_path: Path, object_ids: list[str], class_csv: Path | None = None) -> dict[str, str]:
    df = add_derived(load_table(fits_path))
    local = {str(k): str(v).strip() for k, v in df.groupby("query_id")["object_orbit_class_code"].first().items()}
    cached: dict[str, str] = {}
    if class_csv is not None and class_csv.exists():
        cache_df = pd.read_csv(class_csv, dtype=str)
        cached = {str(row["Object ID"]): str(row["Type"]).strip() for _, row in cache_df.iterrows()}
    classes = {}
    for object_id in object_ids:
        classes[object_id] = local.get(object_id, "--")
        if classes[object_id] == "--" and object_id in cached:
            classes[object_id] = cached[object_id]
        if classes[object_id] == "--":
            try:
                classes[object_id] = fetch_sbdb_class(object_id)
            except Exception:
                classes[object_id] = "--"
    return classes


def write_table(path: Path, caption: str, label: str, columns: list[str], rows: list[list[str]], colspec: str, font_size: str, tabcolsep: float, placement: str = "!htbp") -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(f"\\begin{{table}}[{placement}]\n")
        handle.write("\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write(f"\\label{{{label}}}\n")
        handle.write(f"{font_size}\n")
        handle.write(f"\\setlength{{\\tabcolsep}}{{{tabcolsep:g}pt}}\n")
        handle.write("\\renewcommand{\\arraystretch}{1.12}\n")
        handle.write(f"\\begin{{tabular}}{{{colspec}}}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            handle.write(" & ".join(latex_escape(item) for item in row) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")
        handle.write("\\end{table}\n")


def write_period_validation_table(path: Path, caption: str, label: str, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{table}[!p]\n")
        handle.write("\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write(f"\\label{{{label}}}\n")
        handle.write("\\scriptsize\n")
        handle.write("\\setlength{\\tabcolsep}{2.5pt}\n")
        handle.write("\\renewcommand{\\arraystretch}{1.12}\n")
        handle.write("\\begin{tabular}{r r c r r r r r c c r c c}\n")
        handle.write("\\toprule\n")
        handle.write("Object ID & $H$ & Type & $N_{\\rm total}$ & $N_{\\rm eff}$ & Span & $P_{\\rm rot}$ & $\\Delta P$ & Model & Phot. & MP & Search & Final \\\\\n")
        handle.write("          & (mag) &      &                   &                 & (hr) & (hr) & (hr) &       &       &    &        &       \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            handle.write(" & ".join(latex_escape(item) for item in row) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")
        handle.write("\\end{table}\n")


def make_rows(df: pd.DataFrame, classes: dict[str, str], full: bool) -> list[list[str]]:
    rows = []
    for _, row in df.iterrows():
        object_id = str(int(row["Object ID"]))
        base = [
            object_id,
            fmt_float(row["Median_H"], 2),
            classes.get(object_id, "--"),
        ]
        if full:
            base.extend(
                [
                    f"{int(row['Ntotal'])}",
                    f"{int(row['Neff'])}",
                    fmt_float(row["Span"], 1),
                    fmt_float(row["Prot"], 4),
                    fmt_delta_p(row["ΔP"]),
                    model_label(row["Model"]),
                    phot_label(row["best_mode"]),
                    "--" if pd.isna(row["match_point"]) else f"{int(float(row['match_point']))}",
                    quality_label(row["Quality"]),
                    quality_label(row["Final_Quality"]),
                ]
            )
        else:
            base = [
                object_id,
                classes.get(object_id, "--"),
                f"{int(row['Neff'])}",
                fmt_float(row["Span"], 1),
                fmt_float(row["Prot"], 4),
                fmt_delta_p(row["ΔP"]),
                model_label(row["Model"]),
                phot_label(row["best_mode"]),
            ]
        rows.append(base)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate light-curve period tables for the manuscript.")
    parser.add_argument("--period-tsv", default="/Users/yunaoxiao/Downloads/final_period_table_merged_updated.tsv")
    parser.add_argument("--fits-path", default="gotta_asteroids.fits")
    parser.add_argument("--outdir", default="paper_draft/tables_v7")
    parser.add_argument("--class-csv", default="paper_draft/tables_v7/period_object_classes.csv")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.period_tsv, sep="\t")
    df = df.sort_values(["Final_Quality", "Object ID"], ascending=[False, True]).reset_index(drop=True)
    object_ids = [str(int(value)) for value in df["Object ID"]]
    classes = build_class_map(Path(args.fits_path), object_ids, Path(args.class_csv) if args.class_csv else None)

    reliable = df[df["Final_Quality"].astype(str).str.lower() == "reliable"].copy()
    write_table(
        outdir / "period_reliable_main.tex",
        "Reliable asteroid rotation-period measurements from the combined GOTTA Prototype and 60 cm Schmidt validation sample. Only objects assigned reliable final quality flags are included. The full validation sample, including tentative solutions, is given in Appendix~\\ref{app:lightcurve}.",
        "tab:period_reliable_main",
        ["Object ID", "Type", "$N_{\\rm eff}$", "Span", "$P_{\\rm rot}$", "$\\Delta P$", "Model", "Phot."],
        make_rows(reliable, classes, full=False),
        "llrrrrll",
        r"\footnotesize",
        5.0,
        "!htbp",
    )

    write_period_validation_table(
        outdir / "period_reliable_objects.tex",
        "Final period-analysis table for the combined GOTTA Prototype and 60 cm Schmidt validation sample. The column ``Type'' gives the small-body orbit class used in the known-asteroid catalog. $N_{\\rm total}$ is the total number of photometric points reported by the period-analysis pipeline, and $N_{\\rm eff}$ is the number retained after quality cuts. The final-quality flag separates reliable solutions from tentative follow-up candidates.",
        "tab:period_validation",
        make_rows(df, classes, full=True),
    )

    pd.DataFrame({"Object ID": object_ids, "Type": [classes[object_id] for object_id in object_ids]}).to_csv(outdir / "period_object_classes.csv", index=False)


if __name__ == "__main__":
    main()
