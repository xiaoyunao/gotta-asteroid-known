#!/usr/bin/env python3
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from generate_paper_products import (
    add_derived,
    load_table,
    plot_astrometry,
    plot_geometry,
    plot_photometry,
    plot_temporal,
    setup_style,
)


def main() -> None:
    outdir = REPO_ROOT / "reviewer_figures_20260701"
    setup_style()
    df = add_derived(load_table(REPO_ROOT / "gotta_asteroids.fits"))
    plot_photometry(df, outdir)
    plot_astrometry(df, outdir)
    plot_geometry(df, outdir)
    plot_temporal(df, outdir)


if __name__ == "__main__":
    main()
