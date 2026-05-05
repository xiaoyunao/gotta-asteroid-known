#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

import healpy as hp
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from matplotlib.colors import LogNorm


def as_text_array(values) -> np.ndarray:
    out = []
    for value in values:
        if isinstance(value, (bytes, np.bytes_)):
            out.append(value.decode("utf-8", errors="ignore").strip())
        else:
            out.append(str(value).strip())
    return np.asarray(out, dtype=str)


def str_to_float(values, unit: str | None = None) -> np.ndarray:
    out = []
    for value in values:
        if value is None:
            out.append(np.nan)
            continue
        if isinstance(value, (bytes, np.bytes_)):
            text = value.decode("utf-8", errors="ignore").strip()
        else:
            text = str(value).strip()
        if text in ("", "--", "nan", "NaN"):
            out.append(np.nan)
            continue
        if unit and text.endswith(unit):
            text = text[: -len(unit)].strip()
        try:
            out.append(float(text))
        except ValueError:
            match = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", text)
            out.append(float(match.group(0)) if match else np.nan)
    return np.asarray(out, dtype=float)


def load_columns(path: Path) -> dict[str, np.ndarray]:
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        return {name: np.asarray(data[name]) for name in data.names}


def safe_mask(*arrays: np.ndarray) -> np.ndarray:
    mask = np.ones_like(arrays[0], dtype=bool)
    for array in arrays:
        mask &= np.isfinite(array)
    return mask


def radec_to_pix(ra_deg: np.ndarray, dec_deg: np.ndarray, nside: int = 64, nest: bool = False) -> np.ndarray:
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    theta = 0.5 * np.pi - dec
    phi = ra % (2 * np.pi)
    return hp.ang2pix(nside, theta, phi, nest=nest)


def ra_to_mollweide_lon_rad(ra_deg: np.ndarray, center_deg: float = 180.0) -> np.ndarray:
    lon_deg = ra_deg - center_deg
    lon_deg = (lon_deg + 180.0) % 360.0 - 180.0
    return np.deg2rad(lon_deg)


def set_mollweide_ra_ticks_0_360(ax, center_deg: float = 180.0, step: int = 60) -> None:
    ra_labels = np.arange(step, 301, step)
    lon_ticks = ra_to_mollweide_lon_rad(ra_labels, center_deg=center_deg)
    ax.set_xticks(lon_ticks)
    ax.set_xticklabels([])
    label_lat = np.deg2rad(-15.0)
    for value, lon_tick in zip(ra_labels, lon_ticks):
        ax.text(
            lon_tick,
            label_lat,
            f"{value:d}",
            ha="center",
            va="center",
            fontsize=24,
            color="black",
            zorder=10,
        )


def plot_orbits(columns: dict[str, np.ndarray], out_path: Path) -> None:
    a = str_to_float(columns["orbit_elements_a"], unit="AU")
    e = str_to_float(columns["orbit_elements_e"])
    inc = str_to_float(columns["orbit_elements_i"], unit="deg")
    classes = as_text_array(columns["object_orbit_class_name"])

    unique_classes = np.unique(classes)
    markers = ["o", "s", "D", "^", "v", "*", "p", "h", "+", "x"]
    colors = plt.cm.tab10.colors

    class_marker_color = {}
    for idx, cls in enumerate(unique_classes):
        class_marker_color[cls] = (markers[idx % len(markers)], colors[idx % len(colors)])

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 30

    fig, axes = plt.subplots(1, 2, figsize=(18, 9))
    ax1, ax2 = axes

    for cls in unique_classes:
        mask = classes == cls
        if cls == "TransNeptunian Object":
            alpha_val = 0.8
            color_val = "r"
            size_val = 100
        elif cls == "Main-belt Asteroid":
            alpha_val = 0.1
            color_val = class_marker_color[cls][1]
            size_val = 10
        else:
            alpha_val = 0.8
            color_val = class_marker_color[cls][1]
            size_val = 40

        ax1.scatter(
            a[mask],
            e[mask],
            marker=class_marker_color[cls][0],
            color=color_val,
            s=size_val,
            alpha=alpha_val,
        )

    a_line = np.logspace(np.log10(1.3), 2, 100)
    e_line = 1 - 1.3 / a_line
    ax1.plot(a_line, e_line, "k--", label="q=1.3 AU")
    ax1.legend()
    ax1.set_xscale("log")
    ax1.set_xlabel("Semimajor axis [AU]")
    ax1.set_ylabel("Eccentricity")

    for cls in unique_classes:
        mask = classes == cls
        if cls == "TransNeptunian Object":
            alpha_val = 0.8
            color_val = "r"
            size_val = 100
        elif cls == "Main-belt Asteroid":
            alpha_val = 0.1
            color_val = class_marker_color[cls][1]
            size_val = 20
        else:
            alpha_val = 0.8
            color_val = class_marker_color[cls][1]
            size_val = 40

        ax2.scatter(
            a[mask],
            inc[mask],
            marker=class_marker_color[cls][0],
            color=color_val,
            s=size_val,
            alpha=alpha_val,
            label=cls,
        )

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("Semimajor axis [AU]")
    ax2.set_ylabel("Inclination [°]")
    ax2.legend(fontsize=18, loc="best")

    plt.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_radec(columns: dict[str, np.ndarray], out_path: Path, nside: int = 64) -> None:
    ra_col = "ra"
    dec_col = "dec"
    ra = np.asarray(columns[ra_col], dtype=float)
    dec = np.asarray(columns[dec_col], dtype=float)

    mask = safe_mask(ra, dec) & (dec > -90) & (dec < 90)
    ra = ra[mask]
    dec = dec[mask]

    nest = False
    npix = hp.nside2npix(nside)
    pix = radec_to_pix(ra, dec, nside=nside, nest=nest)
    hp_counts = np.bincount(pix, minlength=npix).astype(np.float64)

    ipix = np.arange(npix)
    theta, phi = hp.pix2ang(nside, ipix, nest=nest)
    dec_c = np.rad2deg(0.5 * np.pi - theta)
    ra_c = np.rad2deg(phi)

    lon = ra_to_mollweide_lon_rad(ra_c, center_deg=180.0)
    lat = np.deg2rad(dec_c)

    cmap = plt.get_cmap("rainbow").copy()
    cmap.set_bad(alpha=0.0)
    counts = hp_counts.astype(np.float64)
    counts_plot = np.clip(counts, 1, 100)
    val = np.ma.masked_where(counts == 0, counts_plot)

    font = {"family": "Times New Roman", "size": 30, "weight": "normal"}
    plt.rc("font", **font)

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection="mollweide")
    im = ax.scatter(
        lon,
        lat,
        c=val,
        s=8,
        linewidths=0,
        cmap=cmap,
        norm=LogNorm(vmin=1, vmax=100),
        rasterized=True,
    )

    ax.grid(True, alpha=0.3)
    set_mollweide_ra_ticks_0_360(ax, center_deg=180.0, step=60)
    ax.tick_params(axis="y", labelsize=24)

    cax = ax.inset_axes([0.30, 0.09, 0.40, 0.045])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label(r"$\mathrm{Counts\ per\ pixel}$", fontsize=18)
    cb.ax.xaxis.set_label_position("top")
    cb.ax.tick_params(labelsize=16, direction="in", length=5, width=1.1)

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Make publication-style GOTTA known-asteroid plots.")
    parser.add_argument("fits_path", nargs="?", default="gotta_asteroids.fits")
    parser.add_argument("--outdir", default="outputs")
    parser.add_argument("--nside", type=int, default=64)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    columns = load_columns(Path(args.fits_path))

    orbit_path = outdir / "asteroid_orbits.png"
    radec_path = outdir / "gotta_radec_healpix_nside64.png"
    plot_orbits(columns, orbit_path)
    plot_radec(columns, radec_path, nside=args.nside)

    print(f"Wrote {orbit_path}")
    print(f"Wrote {radec_path}")


if __name__ == "__main__":
    main()
