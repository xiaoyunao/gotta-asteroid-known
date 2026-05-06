#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon

ADOPTED_APERTURE_INDEX = 5
ADOPTED_MAG = f"Mag_Aper{ADOPTED_APERTURE_INDEX}"
ADOPTED_MAGERR = f"MagErr_Aper{ADOPTED_APERTURE_INDEX}"
ADOPTED_FLUX = f"Flux_Aper{ADOPTED_APERTURE_INDEX}"
ADOPTED_FLUXERR = f"FluxErr_Aper{ADOPTED_APERTURE_INDEX}"


def as_text(values) -> pd.Series:
    return pd.Series(values).astype(str).str.strip()


def load_table(path: Path) -> pd.DataFrame:
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        columns = {}
        for name in data.names:
            arr = np.array(data[name])
            if arr.dtype.byteorder in {">", "<"} and arr.dtype.byteorder != "=":
                arr = arr.astype(arr.dtype.newbyteorder("="), copy=False)
            columns[name] = arr
        return pd.DataFrame(columns)


def parse_night(source_file: str) -> str:
    match = re.search(r"(20\d{6})", str(source_file))
    if not match:
        return "unknown"
    text = match.group(1)
    return f"{text[:4]}-{text[4:6]}-{text[6:8]}"


def parse_field(source_file: str) -> str:
    match = re.match(r"(.+?)_20\d{6}_", str(source_file))
    if match:
        return match.group(1)
    return str(source_file).split("_")[0]


def truthy(values: pd.Series) -> pd.Series:
    return values.astype(str).str.strip().str.lower().isin({"true", "t", "1", "yes", "y"})


def add_derived(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in [
        "ra",
        "dec",
        "RA_Win",
        "DEC_Win",
        "Mag_Kron",
        "MagErr_Kron",
        "Flux_Kron",
        "FluxErr_Kron",
        "mag",
        "epoch",
        "ang_rate_arcsec_hour",
        "ang_rate_deg_day",
        "phase_deg",
        "r_AU",
        "delta_AU",
        ADOPTED_MAG,
        ADOPTED_MAGERR,
        ADOPTED_FLUX,
        ADOPTED_FLUXERR,
    ]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    for idx in range(1, 13):
        for prefix in ["Mag_Aper", "MagErr_Aper", "Flux_Aper", "FluxErr_Aper"]:
            col = f"{prefix}{idx}"
            if col in out:
                out[col] = pd.to_numeric(out[col], errors="coerce")
        mag_col = f"Mag_Aper{idx}"
        err_col = f"MagErr_Aper{idx}"
        if mag_col in out:
            out.loc[(out[mag_col] <= 0) | (out[mag_col] > 40), mag_col] = np.nan
        if err_col in out:
            out.loc[(out[err_col] < 0) | (out[err_col] > 10), err_col] = np.nan
    for mag_col in ["Mag_Kron", "mag"]:
        if mag_col in out:
            out.loc[(out[mag_col] <= 0) | (out[mag_col] > 40), mag_col] = np.nan

    dra_deg = ((out["RA_Win"] - out["ra"] + 180.0) % 360.0) - 180.0
    out["dra_cosdec_arcsec"] = dra_deg * np.cos(np.deg2rad(out["dec"])) * 3600.0
    out["ddec_arcsec"] = (out["DEC_Win"] - out["dec"]) * 3600.0
    out["sep_arcsec"] = np.hypot(out["dra_cosdec_arcsec"], out["ddec_arcsec"])
    out["night"] = as_text(out["source_file"]).map(parse_night)
    out["field_id"] = as_text(out["source_file"]).map(parse_field)
    out["query_id"] = as_text(out["query_id"])
    out["name"] = as_text(out["name"])
    out["object_orbit_class_code"] = as_text(out["object_orbit_class_code"])
    out["object_orbit_class_name"] = as_text(out["object_orbit_class_name"])
    out["object_neo_bool"] = truthy(out["object_neo"])
    out["object_pha_bool"] = truthy(out["object_pha"])
    out["snr_kron_proxy"] = out["Flux_Kron"] / out["FluxErr_Kron"].replace(0, np.nan)
    out.loc[out["snr_kron_proxy"] <= 0, "snr_kron_proxy"] = np.nan
    out["snr_aper_proxy"] = out[ADOPTED_FLUX] / out[ADOPTED_FLUXERR].replace(0, np.nan)
    out.loc[out["snr_aper_proxy"] <= 0, "snr_aper_proxy"] = np.nan
    out["dmag_obs_minus_pred"] = out[ADOPTED_MAG] - out["mag"]
    return out


def finite(series: pd.Series) -> np.ndarray:
    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    return values[np.isfinite(values)]


def q(series: pd.Series, percentile: float) -> float:
    values = finite(series)
    if values.size == 0:
        return np.nan
    return float(np.nanpercentile(values, percentile))


def rms(series: pd.Series) -> float:
    values = finite(series)
    if values.size == 0:
        return np.nan
    return float(np.sqrt(np.nanmean(values**2)))


def fmt(value: float, ndigits: int = 3) -> str:
    if pd.isna(value):
        return "--"
    if abs(value) >= 1000 and float(value).is_integer():
        return f"{value:,.0f}"
    if abs(value) >= 1000:
        return f"{value:,.1f}"
    return f"{value:.{ndigits}f}"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 30,
            "axes.linewidth": 1.4,
            "xtick.major.width": 1.2,
            "ytick.major.width": 1.2,
            "xtick.major.size": 7,
            "ytick.major.size": 7,
            "legend.frameon": False,
            "figure.dpi": 150,
        }
    )


def save_figure(fig: plt.Figure, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def histogram(ax, values, bins, xlabel, ylabel="Detections", logy=False, color="#4c78a8") -> None:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    ax.hist(values, bins=bins, color=color, histtype="stepfilled", alpha=0.82, edgecolor="black", linewidth=0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if logy:
        ax.set_yscale("log")
    ax.tick_params(labelsize=22)


def hexbin(ax, x, y, xlabel, ylabel, gridsize=55, xscale=None, yscale=None) -> None:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if xscale == "log":
        mask &= x > 0
    if yscale == "log":
        mask &= y > 0
    hb = ax.hexbin(x[mask], y[mask], gridsize=gridsize, mincnt=1, cmap="rainbow", linewidths=0.0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if xscale:
        ax.set_xscale(xscale)
    if yscale:
        ax.set_yscale(yscale)
    ax.tick_params(labelsize=22)
    cb = ax.figure.colorbar(hb, ax=ax)
    cb.set_label("Detections", fontsize=22)
    cb.ax.tick_params(labelsize=18)


def running_rate_statistics(rate: pd.Series, sep: pd.Series, nbins: int = 20) -> pd.DataFrame:
    data = pd.DataFrame({"rate": pd.to_numeric(rate, errors="coerce"), "sep": pd.to_numeric(sep, errors="coerce")})
    data = data[np.isfinite(data["rate"]) & np.isfinite(data["sep"]) & (data["rate"] > 0)]
    if data.empty:
        return pd.DataFrame(columns=["rate", "p16", "median", "p84", "count"])
    edges = np.logspace(np.log10(data["rate"].quantile(0.002)), np.log10(data["rate"].quantile(0.998)), nbins + 1)
    rows = []
    for left, right in zip(edges[:-1], edges[1:]):
        sub = data[(data["rate"] >= left) & (data["rate"] < right)]["sep"]
        if len(sub) < 20:
            continue
        rows.append(
            {
                "rate": np.sqrt(left * right),
                "p16": np.nanpercentile(sub, 16),
                "median": np.nanpercentile(sub, 50),
                "p84": np.nanpercentile(sub, 84),
                "count": len(sub),
            }
        )
    return pd.DataFrame(rows)


def write_csv_and_latex(df: pd.DataFrame, csv_path: Path, caption: str, label: str, column_format: str | None = None) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    tex_path = csv_path.with_suffix(".tex")
    if column_format is None:
        column_format = "l" * len(df.columns)
    with tex_path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{table*}\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write(f"\\label{{{label}}}\n")
        handle.write("\\resizebox{\\textwidth}{!}{%\n")
        handle.write(f"\\begin{{tabular}}{{{column_format}}}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(latex_escape(col) for col in df.columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for _, row in df.iterrows():
            handle.write(" & ".join(latex_escape(x) for x in row.to_list()) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def latex_escape(value) -> str:
    text = str(value)
    return text.replace("_", r"\_").replace("%", r"\%")


def make_tables(df: pd.DataFrame, outdir: Path) -> dict[str, pd.DataFrame]:
    overall = pd.DataFrame(
        [
            ("Accepted asteroid-source associations", f"{len(df):,}", "Detection-level catalog associations"),
            ("Distinct known objects", f"{df['query_id'].nunique():,}", "Unique minor-planet identifiers"),
            ("Exposure catalogs represented", f"{df['source_file'].nunique():,}", "Input catalog products with accepted associations"),
            ("UTC nights represented", f"{df['night'].nunique():,}", "Recovered sample date coverage"),
            ("Inferred field identifiers", f"{df['field_id'].nunique():,}", "Field-level grouping from catalog metadata"),
            ("Unique NEOs", f"{df.loc[df['object_neo_bool'], 'query_id'].nunique():,}", "SBDB object_neo flag"),
            ("Unique PHAs", f"{df.loc[df['object_pha_bool'], 'query_id'].nunique():,}", "SBDB object_pha flag"),
            ("Median predicted magnitude", fmt(q(df["mag"], 50), 4), "Ephemeris magnitude"),
            (f"Median {ADOPTED_MAG}", fmt(q(df[ADOPTED_MAG], 50), 4), "Adopted aperture magnitude"),
            (f"Median {ADOPTED_MAGERR}", fmt(q(df[ADOPTED_MAGERR], 50), 4) + " mag", "Adopted aperture uncertainty"),
            ("Median aperture S/N proxy", fmt(q(df["snr_aper_proxy"], 50), 4), f"{ADOPTED_FLUX} / {ADOPTED_FLUXERR}"),
            ("Median separation", fmt(q(df["sep_arcsec"], 50), 3) + " arcsec", "Observed minus predicted"),
            ("84th-percentile separation", fmt(q(df["sep_arcsec"], 84), 3) + " arcsec", "Observed minus predicted"),
            ("2D residual RMS", fmt(rms(df["sep_arcsec"]), 3) + " arcsec", r"sqrt(mean(sep$^2$))"),
            ("RMS delta RA cos Dec", fmt(rms(df["dra_cosdec_arcsec"]), 3) + " arcsec", "Coordinate residual"),
            ("RMS delta Dec", fmt(rms(df["ddec_arcsec"]), 3) + " arcsec", "Coordinate residual"),
            ("Median angular rate", fmt(q(df["ang_rate_arcsec_hour"], 50), 3) + r" arcsec hr$^{-1}$", "JPL Horizons"),
            ("Median phase angle", fmt(q(df["phase_deg"], 50), 3) + " deg", "JPL Horizons"),
            ("Rows without Horizons geometry", f"{int(truthy(df['horizons_failed']).sum()):,}", "Rows excluded from geometry/rate statistics"),
        ],
        columns=["Quantity", "Value", "Note"],
    )

    orbit = (
        df.groupby(["object_orbit_class_code", "object_orbit_class_name"], dropna=False)
        .agg(
            Detections=("query_id", "size"),
            **{
                "Unique objects": ("query_id", "nunique"),
                f"Median {ADOPTED_MAG}": (ADOPTED_MAG, "median"),
                "Median separation": ("sep_arcsec", "median"),
            },
        )
        .reset_index()
        .sort_values("Detections", ascending=False)
    )
    orbit.columns = ["Code", "Orbit class", "Detections", "Unique objects", f"Median {ADOPTED_MAG}", "Median separation"]
    orbit["Detections"] = orbit["Detections"].map(lambda x: f"{x:,}")
    orbit["Unique objects"] = orbit["Unique objects"].map(lambda x: f"{x:,}")
    orbit[f"Median {ADOPTED_MAG}"] = orbit[f"Median {ADOPTED_MAG}"].map(lambda x: fmt(x, 3))
    orbit["Median separation"] = orbit["Median separation"].map(lambda x: fmt(x, 3))

    work = df.copy()
    mag_bins = pd.IntervalIndex.from_tuples([(12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20)], closed="left")
    work["mag_bin"] = pd.cut(work[ADOPTED_MAG], mag_bins)
    mag_ast = (
        work.groupby("mag_bin", observed=True)
        .agg(
            Detections=("query_id", "size"),
            **{
                "Median separation": ("sep_arcsec", "median"),
                "RMS separation": ("sep_arcsec", rms),
                "Median mag. error": (ADOPTED_MAGERR, "median"),
            },
        )
        .reset_index()
    )
    mag_ast["Magnitude bin"] = mag_ast["mag_bin"].map(lambda x: f"$[{x.left:.0f},{x.right:.0f})$")
    mag_ast = mag_ast[["Magnitude bin", "Detections", "Median separation", "RMS separation", "Median mag. error"]]
    for col in ["Median separation", "RMS separation", "Median mag. error"]:
        mag_ast[col] = mag_ast[col].map(lambda x: fmt(x, 3))
    mag_ast["Detections"] = mag_ast["Detections"].map(lambda x: f"{x:,}")

    rate_bins = pd.IntervalIndex.from_tuples([(0, 10), (10, 20), (20, 40), (40, 80), (80, 160), (160, 320), (320, 1000)], closed="left")
    work["rate_bin"] = pd.cut(work["ang_rate_arcsec_hour"], rate_bins)
    rate_ast = (
        work.groupby("rate_bin", observed=True)
        .agg(
            Detections=("query_id", "size"),
            **{
                "Median separation": ("sep_arcsec", "median"),
                "RMS separation": ("sep_arcsec", rms),
                f"Median {ADOPTED_MAG}": (ADOPTED_MAG, "median"),
            },
        )
        .reset_index()
    )
    rate_ast["Rate bin"] = rate_ast["rate_bin"].map(lambda x: f"$[{x.left:.0f},{x.right:.0f})$")
    rate_ast = rate_ast[["Rate bin", "Detections", "Median separation", "RMS separation", f"Median {ADOPTED_MAG}"]]
    for col in ["Median separation", "RMS separation", f"Median {ADOPTED_MAG}"]:
        rate_ast[col] = rate_ast[col].map(lambda x: fmt(x, 3))
    rate_ast["Detections"] = rate_ast["Detections"].map(lambda x: f"{x:,}")

    nightly = (
        df.groupby("night")
        .agg(
            Detections=("query_id", "size"),
            **{
                "Unique objects": ("query_id", "nunique"),
                "Source files": ("source_file", "nunique"),
                f"Median {ADOPTED_MAG}": (ADOPTED_MAG, "median"),
                "Median separation": ("sep_arcsec", "median"),
            },
        )
        .reset_index()
        .sort_values("Detections", ascending=False)
        .head(5)
    )
    nightly.columns = ["UTC date", "Detections", "Unique objects", "Source files", f"Median {ADOPTED_MAG}", "Median separation"]
    for col in ["Detections", "Unique objects", "Source files"]:
        nightly[col] = nightly[col].map(lambda x: f"{x:,}")
    for col in [f"Median {ADOPTED_MAG}", "Median separation"]:
        nightly[col] = nightly[col].map(lambda x: fmt(x, 3))

    obj = (
        df.groupby("query_id")
        .agg(
            Name=("name", "first"),
            Detections=("query_id", "size"),
            **{
                "Distinct nights": ("night", "nunique"),
                "First epoch": ("epoch", "min"),
                "Last epoch": ("epoch", "max"),
                f"Median {ADOPTED_MAG}": (ADOPTED_MAG, "median"),
                "Median separation": ("sep_arcsec", "median"),
                "Orbit class": ("object_orbit_class_code", "first"),
            },
        )
        .reset_index()
        .sort_values("Detections", ascending=False)
        .head(5)
    )
    obj["Baseline days"] = obj["Last epoch"] - obj["First epoch"]
    obj = obj[["query_id", "Name", "Detections", "Distinct nights", "First epoch", "Last epoch", "Baseline days", f"Median {ADOPTED_MAG}", "Median separation", "Orbit class"]]
    obj.columns = ["Object ID", "Name", "Detections", "Distinct nights", "First MJD", "Last MJD", "Baseline days", f"Median {ADOPTED_MAG}", "Median separation", "Orbit class"]
    for col in ["First MJD", "Last MJD", "Baseline days", f"Median {ADOPTED_MAG}", "Median separation"]:
        obj[col] = obj[col].map(lambda x: fmt(x, 3))

    write_csv_and_latex(overall, outdir / "overall_statistics.csv", "Catalog-level statistics for the recovered GOTTA known-asteroid sample.", "tab:summary", "lll")
    write_csv_and_latex(orbit, outdir / "orbit_class_statistics.csv", "Orbit-class composition of the recovered known-asteroid sample. Separations are in arcsec.", "tab:orbit_class", "llrrrr")
    write_csv_and_latex(mag_ast, outdir / "astrometry_by_magnitude.csv", rf"Astrometric residuals as a function of the adopted aperture magnitude \texttt{{Mag\_Aper{ADOPTED_APERTURE_INDEX}}}. Separations are in arcsec.", "tab:mag_astrometry", "lrrrr")
    write_csv_and_latex(rate_ast, outdir / "astrometry_by_rate.csv", r"Astrometric residuals as a function of apparent angular rate. Rate bins are in arcsec hr$^{-1}$ and separations are in arcsec.", "tab:rate_astrometry", "lrrrr")
    write_csv_and_latex(nightly, outdir / "nightly_top5.csv", "Five UTC nights with the largest numbers of accepted known-asteroid associations.", "tab:nightly_top5", "lrrrrr")
    write_csv_and_latex(obj, outdir / "most_observed_objects_top5.csv", "Five most frequently observed known asteroids in the recovered sample.", "tab:most_observed", "llrrrrrrrl")
    return {"overall": overall, "orbit": orbit, "mag_ast": mag_ast, "rate_ast": rate_ast, "nightly": nightly, "objects": obj}


def plot_photometry(df: pd.DataFrame, outdir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    aper_cols = [f"Mag_Aper{i}" for i in range(1, 13) if f"Mag_Aper{i}" in df]
    ref = aper_cols[-1]
    bright = np.isfinite(df[ref]) & (df[ref] > 10) & (df[ref] < 17) & np.isfinite(df[f"MagErr_Aper{len(aper_cols)}"]) & (df[f"MagErr_Aper{len(aper_cols)}"] < 0.1)
    x = np.arange(1, len(aper_cols) + 1)
    med = []
    p16 = []
    p84 = []
    for col in aper_cols:
        diff = df[col] - df[ref]
        vals = diff[bright & np.isfinite(diff)]
        med.append(np.nanmedian(vals))
        p16.append(np.nanpercentile(vals, 16))
        p84.append(np.nanpercentile(vals, 84))
    axes[0, 0].plot(x, med, color="black", marker="o", linewidth=2.0)
    axes[0, 0].fill_between(x, p16, p84, color="#4c78a8", alpha=0.25, linewidth=0)
    axes[0, 0].axvline(ADOPTED_APERTURE_INDEX, color="#e15759", linestyle="--", linewidth=1.8)
    axes[0, 0].set_xlabel("Aperture index")
    axes[0, 0].set_ylabel(r"$m_{\rm aper}-m_{\rm aper12}$ [mag]")
    axes[0, 0].tick_params(labelsize=22)
    histogram(axes[0, 1], finite(df[ADOPTED_MAG]), np.linspace(10, 22, 49), f"{ADOPTED_MAG} [mag]", color="#59a14f")
    histogram(axes[1, 0], finite(df[ADOPTED_MAGERR]), np.linspace(0, 1.1, 56), f"{ADOPTED_MAGERR} [mag]", logy=True, color="#f28e2b")
    hexbin(axes[1, 1], df[ADOPTED_MAG], df[ADOPTED_MAGERR], f"{ADOPTED_MAG} [mag]", f"{ADOPTED_MAGERR} [mag]", gridsize=50)
    axes[1, 1].set_ylim(-0.1, 1.1)
    fig.tight_layout()
    save_figure(fig, outdir / "photometric_statistics")


def plot_astrometry(df: pd.DataFrame, outdir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    histogram(axes[0, 0], finite(df["sep_arcsec"]), np.linspace(0, 1.5, 61), "Separation [arcsec]", logy=True)
    med = q(df["sep_arcsec"], 50)
    p84 = q(df["sep_arcsec"], 84)
    axes[0, 0].axvline(med, color="black", linestyle="--", linewidth=1.4, label=f"median={med:.3f}")
    axes[0, 0].axvline(p84, color="black", linestyle=":", linewidth=1.4, label=f"84%={p84:.3f}")
    axes[0, 0].legend(fontsize=18)
    histogram(axes[0, 1], finite(df["dra_cosdec_arcsec"]), np.linspace(-1.2, 1.2, 61), r"$\Delta\alpha\cos\delta$ [arcsec]", logy=True, color="#59a14f")
    histogram(axes[1, 0], finite(df["ddec_arcsec"]), np.linspace(-1.2, 1.2, 61), r"$\Delta\delta$ [arcsec]", logy=True, color="#f28e2b")
    hexbin(axes[1, 1], df[ADOPTED_MAG], df["sep_arcsec"], f"{ADOPTED_MAG} [mag]", "Separation [arcsec]", gridsize=55)
    axes[1, 1].set_ylim(0, 1.5)
    fig.tight_layout()
    save_figure(fig, outdir / "astrometric_residuals")

    fig, ax = plt.subplots(figsize=(10, 8))
    data = df[np.isfinite(df["ang_rate_arcsec_hour"]) & np.isfinite(df["sep_arcsec"]) & (df["ang_rate_arcsec_hour"] > 0)]
    if len(data) > 15000:
        plot_data = data.sample(15000, random_state=3)
    else:
        plot_data = data
    ax.scatter(plot_data["ang_rate_arcsec_hour"], plot_data["sep_arcsec"], s=5, alpha=0.08, color="#4c78a8", linewidths=0)
    stats = running_rate_statistics(data["ang_rate_arcsec_hour"], data["sep_arcsec"])
    if not stats.empty:
        ax.plot(stats["rate"], stats["median"], color="black", linewidth=2.2, label="running median")
        ax.fill_between(stats["rate"], stats["p16"], stats["p84"], color="#e15759", alpha=0.25, label="16--84 percentile")
        ax.legend(fontsize=18, loc="upper left")
    ax.set_xlabel(r"Angular rate [arcsec hr$^{-1}$]")
    ax.set_ylabel("Separation [arcsec]")
    ax.set_xscale("log")
    ax.set_ylim(0, 1.5)
    ax.tick_params(labelsize=22)
    fig.tight_layout()
    save_figure(fig, outdir / "separation_vs_rate")


def plot_geometry(df: pd.DataFrame, outdir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    histogram(axes[0, 0], finite(df["ang_rate_arcsec_hour"]), np.logspace(-1, 3.2, 65), r"Angular rate [arcsec hr$^{-1}$]", logy=True)
    axes[0, 0].set_xscale("log")
    axes[0, 0].axvline(q(df["ang_rate_arcsec_hour"], 50), color="black", linestyle="--", linewidth=1.6)
    histogram(axes[0, 1], finite(df["phase_deg"]), np.linspace(0, 40, 49), "Phase angle [deg]", color="#59a14f")
    axes[0, 1].axvline(q(df["phase_deg"], 50), color="black", linestyle="--", linewidth=1.6)
    histogram(axes[1, 0], finite(df["r_AU"]), np.linspace(0, 6, 61), "Heliocentric distance [AU]", color="#f28e2b")
    axes[1, 0].axvline(q(df["r_AU"], 50), color="black", linestyle="--", linewidth=1.6)
    histogram(axes[1, 1], finite(df["delta_AU"]), np.linspace(0, 5, 61), "Topocentric distance [AU]", color="#e15759")
    axes[1, 1].axvline(q(df["delta_AU"], 50), color="black", linestyle="--", linewidth=1.6)
    fig.tight_layout()
    save_figure(fig, outdir / "motion_geometry")


def plot_temporal(df: pd.DataFrame, outdir: Path) -> None:
    nightly = df.groupby("night").size().sort_index()
    objects = df.groupby("query_id").agg(detections=("query_id", "size"), distinct_nights=("night", "nunique"), first_epoch=("epoch", "min"), last_epoch=("epoch", "max"))
    objects["baseline_days"] = objects["last_epoch"] - objects["first_epoch"]

    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    dates = pd.to_datetime(nightly.index)
    axes[0, 0].bar(dates, nightly.to_numpy(), color="#4c78a8", width=1.0)
    axes[0, 0].xaxis.set_major_locator(mdates.MonthLocator())
    axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    axes[0, 0].tick_params(axis="x", labelrotation=35)
    axes[0, 0].set_xlabel("UTC date")
    axes[0, 0].set_ylabel("Detections")
    axes[0, 0].tick_params(labelsize=18)
    histogram(axes[0, 1], objects["detections"], np.arange(1, min(objects["detections"].max(), 60) + 2), "Detections per object", logy=True, color="#59a14f")
    values = np.sort(objects["detections"].to_numpy())
    axes[1, 0].step(values, np.arange(1, len(values) + 1) / len(values), where="post", color="black", linewidth=2.0)
    axes[1, 0].set_xscale("log")
    axes[1, 0].set_xlabel("Detections per object")
    axes[1, 0].set_ylabel("Cumulative fraction")
    axes[1, 0].tick_params(labelsize=22)
    values = np.sort(objects["baseline_days"].replace([np.inf, -np.inf], np.nan).dropna().to_numpy())
    axes[1, 1].step(values, np.arange(1, len(values) + 1) / len(values), where="post", color="black", linewidth=2.0)
    axes[1, 1].set_xlabel("Baseline per object [days]")
    axes[1, 1].set_ylabel("Cumulative fraction")
    axes[1, 1].tick_params(labelsize=22)
    fig.tight_layout()
    save_figure(fig, outdir / "temporal_sampling")


def plot_example(df: pd.DataFrame, outdir: Path) -> None:
    counts = df.groupby("source_file").size().sort_values(ascending=False)
    source_file = counts.index[0]
    sub = df[df["source_file"] == source_file].copy()

    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    sc = axes[0, 0].scatter(sub["X_Win"], sub["Y_Win"], c=sub["sep_arcsec"], s=70, cmap="rainbow", edgecolor="black", linewidth=0.3)
    axes[0, 0].set_xlabel("X_Win [pixel]")
    axes[0, 0].set_ylabel("Y_Win [pixel]")
    axes[0, 0].set_title("Accepted matches", fontsize=26)
    cb = fig.colorbar(sc, ax=axes[0, 0])
    cb.set_label("Separation [arcsec]", fontsize=20)
    cb.ax.tick_params(labelsize=18)

    sample = sub.sort_values("sep_arcsec", ascending=False).head(min(35, len(sub)))
    axes[0, 1].quiver(
        sample["X_Win"],
        sample["Y_Win"],
        sample["dra_cosdec_arcsec"],
        sample["ddec_arcsec"],
        angles="xy",
        scale_units="xy",
        scale=0.05,
        color="black",
        width=0.004,
    )
    axes[0, 1].set_xlabel("X_Win [pixel]")
    axes[0, 1].set_ylabel("Y_Win [pixel]")
    axes[0, 1].set_title("Residual vectors", fontsize=26)

    histogram(axes[1, 0], sub["sep_arcsec"], np.linspace(0, max(0.2, float(sub["sep_arcsec"].max()) * 1.05), 25), "Separation [arcsec]", color="#59a14f")
    axes[1, 1].scatter(sub["mag"], sub[ADOPTED_MAG], s=55, alpha=0.8, color="#4c78a8", edgecolor="black", linewidth=0.3)
    axes[1, 1].set_xlabel("Predicted magnitude [mag]")
    axes[1, 1].set_ylabel(f"{ADOPTED_MAG} [mag]")
    axes[1, 1].tick_params(labelsize=22)
    fig.suptitle(f"Matched-only diagnostic: {source_file}", fontsize=28)
    fig.tight_layout()
    save_figure(fig, outdir / "example_crossmatch_diagnostic")


def add_box(ax, xy, w, h, text, kind) -> None:
    x, y = xy
    colors = {
        "input": ("#dceeff", "#4f81bd"),
        "process": ("#d9ead3", "#6aa84f"),
        "decision": ("#fff2cc", "#bf9000"),
        "reject": ("#f4cccc", "#cc0000"),
        "output": ("#eadcf8", "#8e7cc3"),
        "database": ("#d9eaf7", "#6d9eeb"),
    }
    face, edge = colors[kind]
    if kind == "decision":
        patch = Polygon([(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)], closed=True, facecolor=face, edgecolor=edge, linewidth=2.0)
    elif kind in {"input", "output"}:
        skew = 0.15 * w
        patch = Polygon([(x + skew, y), (x + w, y), (x + w - skew, y + h), (x, y + h)], closed=True, facecolor=face, edgecolor=edge, linewidth=2.0)
    elif kind == "database":
        patch = Ellipse((x + w / 2, y + h / 2), w, h, facecolor=face, edgecolor=edge, linewidth=2.0)
    else:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.07", facecolor=face, edgecolor=edge, linewidth=2.0)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=17)


def arrow(ax, start, end) -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=18, linewidth=1.8, color="#444444"))


def plot_flowchart(outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(15, 18))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 18)
    ax.axis("off")

    nodes = {
        "catalog": ((3.2, 16.8), 3.6, 0.7, "Photometric\ncatalog", "input"),
        "header": ((0.4, 15.3), 3.0, 0.8, "FITS header\nWCS + time", "input"),
        "orbit": ((6.6, 15.3), 3.0, 0.8, "Lowell astorb\nSBDB / Horizons", "input"),
        "read": ((3.4, 15.1), 3.2, 0.8, "Read table\nand header", "process"),
        "wcs": ((3.4, 13.8), 3.2, 0.8, "WCS footprint\nfrom CCD corners", "process"),
        "epoch": ((3.4, 12.5), 3.2, 0.8, "Mid-exposure\nepoch", "process"),
        "query": ((3.4, 11.2), 3.2, 0.8, "Ephemeris\nscreening", "process"),
        "mag": ((3.55, 9.75), 2.9, 1.0, "Magnitude\npre-filter?", "decision"),
        "faint": ((7.0, 9.9), 2.4, 0.7, "Reject faint\ncandidates", "reject"),
        "pixel": ((3.4, 8.4), 3.2, 0.8, "Predicted RA/Dec\ninto pixels", "process"),
        "inside": ((3.55, 6.95), 2.9, 1.0, "Inside CCD\nfootprint?", "decision"),
        "offccd": ((7.0, 7.1), 2.4, 0.7, "Reject off-CCD\npredictions", "reject"),
        "match": ((3.4, 5.6), 3.2, 0.8, "Nearest-neighbor\nangular match", "process"),
        "accept": ((3.55, 4.15), 2.9, 1.0, "Separation\nthreshold?", "decision"),
        "unmatched": ((7.0, 4.3), 2.4, 0.7, "Reject unmatched\nrows", "reject"),
        "merge": ((3.4, 2.8), 3.2, 0.8, "Merge ephemeris\nand catalog row", "process"),
        "augment": ((3.4, 1.55), 3.2, 0.8, "SBDB + Horizons\naugmentation", "process"),
        "final": ((3.1, 0.3), 3.8, 0.8, "gotta_asteroids.fits\nstatistics + figures", "output"),
    }
    for xy, w, h, text, kind in nodes.values():
        add_box(ax, xy, w, h, text, kind)

    arrow(ax, (5.0, 16.8), (5.0, 15.9))
    arrow(ax, (3.4, 15.7), (3.4, 15.5))
    arrow(ax, (6.6, 15.7), (6.6, 15.5))
    for y0, y1 in [(15.1, 14.6), (13.8, 13.3), (12.5, 12.0), (11.2, 10.75), (9.75, 9.2), (8.4, 7.95), (6.95, 6.4), (5.6, 5.15), (4.15, 3.6), (2.8, 2.35), (1.55, 1.1)]:
        arrow(ax, (5.0, y0), (5.0, y1))
    arrow(ax, (6.45, 10.25), (7.0, 10.25))
    arrow(ax, (6.45, 7.45), (7.0, 7.45))
    arrow(ax, (6.45, 4.65), (7.0, 4.65))
    ax.text(6.62, 10.48, "no", fontsize=16)
    ax.text(6.62, 7.68, "no", fontsize=16)
    ax.text(6.62, 4.88, "no", fontsize=16)
    ax.text(4.65, 9.45, "yes", fontsize=16)
    ax.text(4.65, 6.65, "yes", fontsize=16)
    ax.text(4.65, 3.85, "yes", fontsize=16)
    ax.text(5.0, 17.75, "Known-object processing", ha="center", va="center", fontsize=30)
    save_figure(fig, outdir / "method_flowchart_styled")


def write_mermaid(outdir: Path) -> None:
    text = """flowchart TD
    A[/Per-exposure photometric catalog/]:::input
    B[/FITS header metadata: WCS, DATE-OBS, EXPTIME/]:::input
    C[/External orbit resources: Lowell astorb, SBDB, JPL Horizons/]:::input
    D([Read source table and header]):::process
    E([Build WCS and project CCD corners]):::process
    F([Compute mid-exposure epoch]):::process
    G([Estimate padded field search radius]):::process
    H([Ephemeris screening]):::process
    I{{Predicted magnitude within limit?}}:::decision
    J([Transform predictions to pixel coordinates]):::process
    K{{Inside CCD footprint?}}:::decision
    L([Nearest-neighbor angular cross-match]):::process
    M{{Separation threshold and optional magnitude check?}}:::decision
    N([Merge prediction row with catalog source row]):::process
    O([Merge exposure/night products]):::process
    P([SBDB and Horizons augmentation]):::process
    Q[/Final gotta_asteroids.fits/]:::output
    R[/Statistics, figures, light-curve inputs/]:::output
    X1([Reject faint candidates]):::reject
    X2([Reject off-CCD predictions]):::reject
    X3([Reject unmatched rows]):::reject
    A --> D
    B --> D
    C --> H
    D --> E --> G --> H
    D --> F --> H
    H --> I
    I -- yes --> J --> K
    I -- no --> X1
    K -- yes --> L --> M
    K -- no --> X2
    M -- yes --> N --> O --> P --> Q --> R
    M -- no --> X3
    classDef input fill:#dceeff,stroke:#4f81bd,stroke-width:2px;
    classDef process fill:#d9ead3,stroke:#6aa84f,stroke-width:2px;
    classDef decision fill:#fff2cc,stroke:#bf9000,stroke-width:2px;
    classDef reject fill:#f4cccc,stroke:#cc0000,stroke-width:2px;
    classDef output fill:#eadcf8,stroke:#8e7cc3,stroke-width:2px;
"""
    (outdir / "method_flowchart_styled.mmd").write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper figures and tables from gotta_asteroids.fits.")
    parser.add_argument("fits_path", nargs="?", default="gotta_asteroids.fits")
    parser.add_argument("--outdir", default="paper_draft")
    parser.add_argument("--paper-version", default="v3")
    args = parser.parse_args()

    root = Path(args.outdir)
    figdir = root / f"figures_{args.paper_version}"
    tabledir = root / f"tables_{args.paper_version}"
    setup_style()
    df = add_derived(load_table(Path(args.fits_path)))
    make_tables(df, tabledir)
    plot_flowchart(figdir)
    write_mermaid(figdir)
    workflow_src = Path("outputs/known_object_processing.png")
    if workflow_src.exists():
        shutil.copy2(workflow_src, figdir / "known_object_processing.png")
    plot_photometry(df, figdir)
    plot_astrometry(df, figdir)
    plot_geometry(df, figdir)
    plot_temporal(df, figdir)
    plot_example(df, figdir)
    print(f"Wrote figures to {figdir}")
    print(f"Wrote tables to {tabledir}")


if __name__ == "__main__":
    main()
