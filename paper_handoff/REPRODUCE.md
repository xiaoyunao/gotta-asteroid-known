# Reproduction Notes

## Environment

The repository notes that the system `python3` environment may not include all plotting dependencies. The working plotting environment used locally is:

```bash
/Users/island/opt/anaconda3/envs/astro/bin/python
```

Required packages include at least:

- `astropy`
- `numpy`
- `matplotlib`
- `healpy`

The matching pipeline also depends on external asteroid ephemeris tooling such as `aleph`, Lowell `astorb.dat`, and SPICE/kernel resources where applicable.

## Main Inputs

The final analysis input is:

```text
gotta_asteroids.fits
```

This file is excluded from git and from the handoff zip because it is a large FITS data product.

## Recreate Documentation And Statistics

```bash
python3 scripts/describe_fits_columns.py gotta_asteroids.fits --out docs/FITS_COLUMNS.md
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/summarize_gotta_asteroids.py gotta_asteroids.fits --md-out docs/GOTTA_STATS.md --json-out outputs/gotta_stats.json
```

## Recreate Figures

```bash
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/plot_gotta_asteroids.py gotta_asteroids.fits --outdir outputs
```

Expected outputs:

- `outputs/asteroid_orbits.png`
- `outputs/gotta_radec_healpix_nside64.png`

## Validate Python Syntax

```bash
/Users/island/opt/anaconda3/envs/astro/bin/python -m py_compile scripts/*.py smt_known_asteroid/*.py remote_foundation/*.py
```

## Recreate Handoff Zip

```bash
repo_name=$(basename -s .git "$(git remote get-url origin 2>/dev/null || basename "$PWD")")
shortcommit=$(git rev-parse --short HEAD)

zip -r "paper_handoff_${repo_name}_${shortcommit}.zip" paper_handoff \
  -x "*.fits" "*.fits.gz" "*.fit" "*.fz" "*.h5" "*.hdf5" "*.npy" "*.npz" \
     "*/__pycache__/*" "*/.DS_Store" "*/.ipynb_checkpoints/*"

unzip -l "paper_handoff_${repo_name}_${shortcommit}.zip"
unzip -l "paper_handoff_${repo_name}_${shortcommit}.zip" | grep -Ei '\.fits$|\.fits\.gz$|\.fit$|\.fz$' || true
shasum -a 256 "paper_handoff_${repo_name}_${shortcommit}.zip" > "paper_handoff_${repo_name}_${shortcommit}.zip.sha256"
```

## Reproduction Limits

The final figures and summaries can be regenerated if `gotta_asteroids.fits` and the `astro` environment are available. Rebuilding `gotta_asteroids.fits` from raw catalogs requires the upstream catalog files, Lowell `astorb.dat`, external ephemeris tooling, and SBDB/JPL Horizons access; those inputs are not contained in this handoff zip.
