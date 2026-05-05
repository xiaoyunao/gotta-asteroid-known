#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import numpy as np
from astropy.io import fits

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAVE_MPL = True
except Exception:
    HAVE_MPL = False


def clean_str(values) -> np.ndarray:
    out = []
    for value in values:
        if isinstance(value, bytes):
            out.append(value.decode("utf-8", errors="ignore").strip())
        else:
            out.append(str(value).strip())
    return np.asarray(out)


def to_float(values) -> np.ndarray:
    out = np.full(len(values), np.nan, dtype=float)
    for idx, value in enumerate(values):
        if value is None:
            continue
        text = value.decode("utf-8", errors="ignore") if isinstance(value, bytes) else str(value)
        match = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", text)
        if match:
            out[idx] = float(match.group(0))
    return out


def load_data(path: Path):
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        arrays = {name: np.array(data[name]) for name in data.names}
    return arrays


def plot_orbits(arrays: dict[str, np.ndarray], out_path: Path) -> None:
    required = ["orbit_elements_a", "orbit_elements_e", "orbit_elements_i", "object_orbit_class_name"]
    missing = [name for name in required if name not in arrays]
    if missing:
        raise SystemExit(f"Missing orbit columns: {missing}")

    a = to_float(arrays["orbit_elements_a"])
    e = to_float(arrays["orbit_elements_e"])
    inc = to_float(arrays["orbit_elements_i"])
    classes = clean_str(arrays["object_orbit_class_name"])

    good = np.isfinite(a) & np.isfinite(e) & np.isfinite(inc) & (a > 0) & (e >= 0)
    a, e, inc, classes = a[good], e[good], inc[good], classes[good]

    if not HAVE_MPL:
        plot_orbits_pillow(a, e, inc, classes, out_path)
        return

    unique, counts = np.unique(classes, return_counts=True)
    order = unique[np.argsort(counts)[::-1]]
    cmap = plt.get_cmap("tab10")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), constrained_layout=True)
    for idx, cls in enumerate(order):
        mask = classes == cls
        alpha = 0.14 if cls == "Main-belt Asteroid" else 0.75
        size = 8 if cls == "Main-belt Asteroid" else 22
        color = cmap(idx % 10)
        label = f"{cls or 'Unknown'} ({int(mask.sum())})"
        axes[0].scatter(a[mask], e[mask], s=size, alpha=alpha, color=color, edgecolors="none", label=label)
        axes[1].scatter(a[mask], inc[mask], s=size, alpha=alpha, color=color, edgecolors="none", label=label)

    a_line = np.logspace(math.log10(1.3), 2, 200)
    axes[0].plot(a_line, 1.0 - 1.3 / a_line, color="black", linestyle="--", linewidth=1.0, label="q=1.3 AU")

    axes[0].set_xscale("log")
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[0].set_xlabel("Semimajor axis [AU]")
    axes[0].set_ylabel("Eccentricity")
    axes[1].set_xlabel("Semimajor axis [AU]")
    axes[1].set_ylabel("Inclination [deg]")
    axes[0].set_title("Known asteroid orbital distribution: a vs e")
    axes[1].set_title("Known asteroid orbital distribution: a vs i")
    axes[1].legend(fontsize=8, loc="best", frameon=False)
    fig.savefig(out_path, dpi=220)
    plt.close(fig)


def plot_radec(arrays: dict[str, np.ndarray], out_path: Path) -> None:
    ra_name = "RA_Win" if "RA_Win" in arrays else "ra"
    dec_name = "DEC_Win" if "DEC_Win" in arrays else "dec"
    ra = np.asarray(arrays[ra_name], dtype=float)
    dec = np.asarray(arrays[dec_name], dtype=float)
    good = np.isfinite(ra) & np.isfinite(dec) & (dec > -90) & (dec < 90)
    ra = ra[good]
    dec = dec[good]

    if not HAVE_MPL:
        plot_radec_pillow(ra, dec, out_path)
        return

    lon = np.deg2rad((ra - 180.0 + 180.0) % 360.0 - 180.0)
    lat = np.deg2rad(dec)

    fig = plt.figure(figsize=(10.5, 6.2))
    ax = fig.add_subplot(111, projection="mollweide")
    hb = ax.hexbin(lon, lat, gridsize=120, bins="log", mincnt=1, cmap="viridis", linewidths=0)
    ax.grid(True, alpha=0.3)
    ax.set_title("All matched known asteroids: RA-Dec density")
    ax.set_xticks(np.deg2rad([-120, -60, 0, 60, 120]))
    ax.set_xticklabels(["60", "120", "180", "240", "300"])
    cb = fig.colorbar(hb, ax=ax, pad=0.08, shrink=0.82)
    cb.set_label("log10(counts)")
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def draw_axes(draw, box, xlabel: str, ylabel: str, title: str) -> None:
    x0, y0, x1, y1 = box
    draw.rectangle(box, outline=(40, 40, 40), width=2)
    draw.text((x0 + 8, y0 + 8), title, fill=(20, 20, 20))
    draw.text(((x0 + x1) // 2 - 60, y1 + 28), xlabel, fill=(20, 20, 20))
    draw.text((x0 - 54, (y0 + y1) // 2), ylabel, fill=(20, 20, 20))


def scale_linear(values: np.ndarray, lo: float, hi: float, pix0: int, pix1: int) -> np.ndarray:
    return pix0 + (values - lo) / (hi - lo) * (pix1 - pix0)


def plot_orbits_pillow(a: np.ndarray, e: np.ndarray, inc: np.ndarray, classes: np.ndarray, out_path: Path) -> None:
    from PIL import Image, ImageDraw

    width, height = 1500, 700
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img, "RGBA")
    left = (95, 70, 705, 585)
    right = (820, 70, 1430, 585)
    draw_axes(draw, left, "log10(a / AU)", "e", "Known asteroid orbital distribution: a vs e")
    draw_axes(draw, right, "log10(a / AU)", "log10(i / deg)", "Known asteroid orbital distribution: a vs i")

    loga = np.log10(a)
    logi = np.log10(np.clip(inc, 0.01, None))
    xlo, xhi = np.nanpercentile(loga, [0.5, 99.8])
    ilo, ihi = np.nanpercentile(logi, [0.5, 99.8])
    colors = [
        (31, 119, 180, 80),
        (214, 39, 40, 130),
        (44, 160, 44, 130),
        (148, 103, 189, 130),
        (255, 127, 14, 130),
        (23, 190, 207, 130),
    ]
    unique, counts = np.unique(classes, return_counts=True)
    order = unique[np.argsort(counts)[::-1]]
    color_for = {cls: colors[idx % len(colors)] for idx, cls in enumerate(order)}

    for cls in order:
        mask = classes == cls
        color = color_for[cls]
        radius = 1 if cls == "Main-belt Asteroid" else 2
        xs = scale_linear(loga[mask], xlo, xhi, left[0], left[2])
        ys = scale_linear(e[mask], 0.0, min(1.1, max(1.0, np.nanpercentile(e, 99.8))), left[3], left[1])
        for x, y in zip(xs, ys):
            if left[0] <= x <= left[2] and left[1] <= y <= left[3]:
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
        xs = scale_linear(loga[mask], xlo, xhi, right[0], right[2])
        ys = scale_linear(logi[mask], ilo, ihi, right[3], right[1])
        for x, y in zip(xs, ys):
            if right[0] <= x <= right[2] and right[1] <= y <= right[3]:
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    legend_x, legend_y = 95, 615
    for idx, cls in enumerate(order[:8]):
        y = legend_y + (idx // 4) * 24
        x = legend_x + (idx % 4) * 330
        draw.rectangle((x, y, x + 16, y + 12), fill=color_for[cls])
        draw.text((x + 22, y - 2), f"{cls or 'Unknown'} ({int((classes == cls).sum())})", fill=(20, 20, 20))
    img.save(out_path)


def plot_radec_pillow(ra: np.ndarray, dec: np.ndarray, out_path: Path) -> None:
    from PIL import Image, ImageDraw

    width, height = 1200, 650
    margin = 70
    plot_w, plot_h = width - 2 * margin, height - 2 * margin
    hist, _, _ = np.histogram2d(ra % 360.0, dec, bins=[720, 360], range=[[0, 360], [-90, 90]])
    val = np.log10(hist.T + 1.0)
    val = val / max(float(val.max()), 1.0)
    rgb = np.zeros((val.shape[0], val.shape[1], 3), dtype=np.uint8)
    rgb[..., 0] = (35 + 220 * val).astype(np.uint8)
    rgb[..., 1] = (45 + 160 * np.sqrt(val)).astype(np.uint8)
    rgb[..., 2] = (90 + 80 * (1.0 - val)).astype(np.uint8)
    heat = Image.fromarray(np.flipud(rgb), "RGB").resize((plot_w, plot_h))
    img = Image.new("RGB", (width, height), "white")
    img.paste(heat, (margin, margin))
    draw = ImageDraw.Draw(img)
    box = (margin, margin, margin + plot_w, margin + plot_h)
    draw.rectangle(box, outline=(40, 40, 40), width=2)
    draw.text((margin + 10, 25), "All matched known asteroids: RA-Dec density", fill=(20, 20, 20))
    draw.text((width // 2 - 80, height - 42), "RA [deg]", fill=(20, 20, 20))
    draw.text((10, height // 2), "Dec [deg]", fill=(20, 20, 20))
    for tick in range(0, 361, 60):
        x = margin + int(plot_w * tick / 360)
        draw.line((x, margin + plot_h, x, margin + plot_h + 8), fill=(40, 40, 40))
        draw.text((x - 12, margin + plot_h + 12), str(tick), fill=(20, 20, 20))
    for tick in range(-60, 91, 30):
        y = margin + int(plot_h * (90 - tick) / 180)
        draw.line((margin - 8, y, margin, y), fill=(40, 40, 40))
        draw.text((margin - 48, y - 8), str(tick), fill=(20, 20, 20))
    img.save(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot orbit and RA/Dec summaries from all_asteroids.fits.")
    parser.add_argument("fits_path", nargs="?", default="all_asteroids.fits")
    parser.add_argument("--outdir", default="outputs")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    arrays = load_data(Path(args.fits_path))
    plot_orbits(arrays, outdir / "asteroid_orbits.png")
    plot_radec(arrays, outdir / "all_radec_distribution.png")
    print(f"Wrote {outdir / 'asteroid_orbits.png'}")
    print(f"Wrote {outdir / 'all_radec_distribution.png'}")


if __name__ == "__main__":
    main()
