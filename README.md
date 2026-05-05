# gotta_asteroid_1

GOTTA asteroid processing workspace.

This repository collects the useful known-asteroid processing and plotting
programs for GOTTA data, adapted from the SMT asteroid workflow and reference
scripts under `/Volumes/Foundation/Asteroid`.

Large FITS data products are kept locally and are not committed to git.

## Contents

- `remote_foundation/`: selected reference scripts and notebooks copied from
  `/Volumes/Foundation/Asteroid`
- `smt_known_asteroid/`: engineering version of the known-asteroid workflow
  copied from `/Users/island/Desktop/smt_asteroid/known_asteroid`
- `scripts/describe_fits_columns.py`: generate `docs/FITS_COLUMNS.md`
- `scripts/plot_gotta_asteroids.py`: draw publication-style orbit and RA/Dec summary plots
- `scripts/summarize_gotta_asteroids.py`: generate `docs/GOTTA_STATS.md`
- `docs/METHOD_KNOWN_ASTEROID_EXTRACTION.md`: method notes from photometric catalog to asteroid photometry
- `docs/PROCESSING_ORDER.md`: recommended processing order and useful-file notes
- `docs/FITS_COLUMNS.md`: `all_asteroids.fits` column dictionary

## Local Data

`all_asteroids.fits` was downloaded to this directory from:

```bash
scp -P 9553 xiaoya@159.226.170.185:/data/proc/xiaoyunao/all_asteroids.fits .
```

It has `162933` rows and `164` columns. It is ignored by git.

Use `gotta_asteroids.fits` for paper figures and statistics. It is the filtered
GOTTA-only table and currently has `56230` rows and `164` columns.

## Useful Commands

```bash
python3 scripts/describe_fits_columns.py gotta_asteroids.fits --out docs/FITS_COLUMNS.md
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/plot_gotta_asteroids.py gotta_asteroids.fits --outdir outputs/gotta
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/summarize_gotta_asteroids.py gotta_asteroids.fits --md-out docs/GOTTA_STATS.md --json-out outputs/gotta/gotta_stats.json
python3 -m py_compile scripts/*.py smt_known_asteroid/*.py remote_foundation/*.py remote_foundation/astorb/*.py
```
