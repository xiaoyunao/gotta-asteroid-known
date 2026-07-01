#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle


HERE = Path(__file__).resolve().parent
SOURCE_DIR = HERE / "source_data"
IMAGE_PATH = SOURCE_DIR / "stpxl-0655_20250117_0001_1.fits.gz"
MATCH_PATH = SOURCE_DIR / "20250117_matched_asteroids.fits"
LOCAL_TOTAL = HERE.parent / "gotta_asteroids.fits"
SOURCE_FILE = "stpxl-0655_20250117_0001_1_cat.fits.gz"
IMAGE_LABEL = "stpxl-0655_20250117_0001_1"
TARGET_NAMES = ["Zvezdara", "Polakis", "1999 XG165", "1999 XY103"]
ADOPTED_MAG = "Mag_Aper4"


def as_str(value) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


def robust_limits(data: np.ndarray, lo: float = 0.5, hi: float = 99.6) -> tuple[float, float]:
    finite = np.asarray(data, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return 0.0, 1.0
    vmin, vmax = np.nanpercentile(finite, [lo, hi])
    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmax <= vmin:
        med = float(np.nanmedian(finite))
        std = float(np.nanstd(finite)) or 1.0
        return med - std, med + 5.0 * std
    return float(vmin), float(vmax)


def stretch(data: np.ndarray, vmin: float, vmax: float) -> np.ndarray:
    arr = np.clip((np.asarray(data, dtype=float) - vmin) / (vmax - vmin), 0.0, 1.0)
    arr[~np.isfinite(arr)] = 0.0
    return np.sqrt(arr)


def oc_separation_arcsec(row) -> float:
    dra = (float(row["RA_Win"]) - float(row["ra"])) * np.cos(np.deg2rad(float(row["dec"]))) * 3600.0
    ddec = (float(row["DEC_Win"]) - float(row["dec"])) * 3600.0
    return float(np.hypot(dra, ddec))


def source_rows() -> list[dict]:
    matched = Table.read(MATCH_PATH)
    total = Table.read(LOCAL_TOTAL, memmap=True)
    sub = matched[matched["source_file"] == SOURCE_FILE]
    rows = []
    local_names = np.array([as_str(x) for x in total["name"]])
    local_epoch = np.asarray(total["epoch"], dtype=float)

    for target in TARGET_NAMES:
        candidates = sub[[as_str(x) == target for x in sub["name"]]]
        if len(candidates) != 1:
            raise RuntimeError(f"Expected one match for {target}, found {len(candidates)}")
        row = candidates[0]
        local_mask = (local_names == target) & (np.abs(local_epoch - float(row["epoch"])) < 0.01)
        local = total[local_mask]
        if len(local) < 1:
            raise RuntimeError(f"Could not find local angular rate for {target}")
        number = row["number"]
        if np.ma.is_masked(number) or not np.isfinite(float(number)):
            object_id = target
        else:
            object_id = f"({int(round(float(number)))}) {target}"
        rows.append(
            {
                "name": target,
                "object_id": object_id,
                "x": float(row["X_Win"]),
                "y": float(row["Y_Win"]),
                "g_aper": float(row[ADOPTED_MAG]),
                "rate": float(local[0]["ang_rate_arcsec_hour"]),
                "sep": oc_separation_arcsec(row),
            }
        )
    return rows


def cutout(data: np.ndarray, x: float, y: float, size: int = 180) -> np.ndarray:
    ny, nx = data.shape
    half = size // 2
    cx = int(round(x)) - 1
    cy = int(round(y)) - 1
    x0, x1 = cx - half, cx + half
    y0, y1 = cy - half, cy + half
    out = np.full((size, size), np.nan, dtype=float)
    sx0, sx1 = max(0, x0), min(nx, x1)
    sy0, sy1 = max(0, y0), min(ny, y1)
    dx0, dy0 = sx0 - x0, sy0 - y0
    if sx1 > sx0 and sy1 > sy0:
        out[dy0 : dy0 + sy1 - sy0, dx0 : dx0 + sx1 - sx0] = data[sy0:sy1, sx0:sx1]
    return out


def draw_label(ax, x: float, y: float, text: str, size: int = 12, ha: str = "left", va: str = "top") -> None:
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va=va,
        color="white",
        fontsize=size,
        fontweight="bold",
        linespacing=1.18,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "black", "edgecolor": "none", "alpha": 0.68},
    )


def plot() -> None:
    rows = source_rows()
    with fits.open(IMAGE_PATH, memmap=True) as hdul:
        data = np.asarray(hdul["IMG"].data, dtype=float)
        hdr = hdul["IMG"].header
    mjd = float(hdr["MJD"])
    ny, nx = data.shape

    # Downsample the full frame for a light-weight overview while keeping
    # marker positions in the native CCD pixel coordinate system.
    factor = 6
    view = data[: ny - ny % factor, : nx - nx % factor].reshape(ny // factor, factor, nx // factor, factor).mean(axis=(1, 3))
    full_vmin, full_vmax = robust_limits(view, 0.5, 99.7)

    fig = plt.figure(figsize=(15.5, 8.8), dpi=220)
    gs = GridSpec(2, 3, width_ratios=[2.35, 1, 1], height_ratios=[1, 1], wspace=0.055, hspace=0.07)

    ax_full = fig.add_subplot(gs[:, 0])
    ax_full.imshow(stretch(view, full_vmin, full_vmax), cmap="gray", origin="lower", extent=[0, nx, 0, ny], interpolation="nearest")
    ax_full.set_xticks([])
    ax_full.set_yticks([])
    for spine in ax_full.spines.values():
        spine.set_color("0.15")
        spine.set_linewidth(1.2)

    draw_label(ax_full, 130, ny - 170, f"{IMAGE_LABEL}\nMJD = {mjd:.8f}", size=12, va="top")
    colors = ["#ffcc33", "#00b4d8", "#fb5607", "#80ed99"]
    for idx, (row, color) in enumerate(zip(rows, colors), 1):
        ax_full.add_patch(Circle((row["x"], row["y"]), 155, fill=False, edgecolor=color, linewidth=3.0))
        ax_full.plot(row["x"], row["y"], marker="+", ms=15, mew=2.4, color=color)
        label_x = min(max(row["x"] + 185, 120), nx - 1500)
        label_y = min(max(row["y"] + 110, 220), ny - 170)
        draw_label(ax_full, label_x, label_y, f"{idx}  {row['name']}", size=10.5, va="center")

    for idx, row in enumerate(rows, 1):
        ax = fig.add_subplot(gs[(idx - 1) // 2, 1 + (idx - 1) % 2])
        cut = cutout(data, row["x"], row["y"])
        vmin, vmax = robust_limits(cut, 1.0, 99.8)
        ax.imshow(stretch(cut, vmin, vmax), cmap="gray", origin="lower", interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(colors[idx - 1])
            spine.set_linewidth(2.3)
        cy = cx = cut.shape[0] / 2.0 - 0.5
        ax.add_patch(Circle((cx, cy), 17, fill=False, edgecolor=colors[idx - 1], linewidth=2.0))
        ax.plot(cx, cy, marker="+", ms=12, mew=1.8, color=colors[idx - 1])
        label = (
            f"{idx}. {row['object_id']}\n"
            f"$g_{{\\rm aper}}$ = {row['g_aper']:.2f} mag\n"
            f"$\\mu$ = {row['rate']:.1f} arcsec hr$^{{-1}}$\n"
            f"O-C = {row['sep']:.2f} arcsec"
        )
        draw_label(ax, 7, cut.shape[0] - 8, label, size=9.5, va="top")

    fig.savefig(HERE / "fig1_review_cutouts.png", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(HERE / "fig1_review_cutouts.pdf", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


if __name__ == "__main__":
    plot()
