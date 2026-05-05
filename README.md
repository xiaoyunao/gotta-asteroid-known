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
- `scripts/plot_all_asteroids_summary.py`: draw orbit and RA/Dec summary plots
- `docs/PROCESSING_ORDER.md`: recommended processing order and useful-file notes
- `docs/FITS_COLUMNS.md`: `all_asteroids.fits` column dictionary

## Local Data

`all_asteroids.fits` was downloaded to this directory from:

```bash
scp -P 9553 xiaoya@159.226.170.185:/data/proc/xiaoyunao/all_asteroids.fits .
```

It has `162933` rows and `164` columns. It is ignored by git.

## Useful Commands

```bash
python3 scripts/describe_fits_columns.py all_asteroids.fits --out docs/FITS_COLUMNS.md
python3 scripts/plot_all_asteroids_summary.py all_asteroids.fits --outdir outputs
python3 -m py_compile scripts/*.py smt_known_asteroid/*.py remote_foundation/*.py remote_foundation/astorb/*.py
```
