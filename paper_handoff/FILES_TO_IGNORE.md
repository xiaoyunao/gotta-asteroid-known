# Files To Ignore

## Large Raw Or Intermediate Data

- `gotta_asteroids.fits`: final analysis FITS table, required to rerun analysis locally but excluded from git and from the zip because it is large.
- `all_asteroids.fits`: historical mixed-source table; do not use for this GOTTA-only paper.
- `*.fits`, `*.fits.gz`, `*.fit`, `*.fz`: raw and intermediate FITS products excluded from the handoff zip.
- `*.h5`, `*.hdf5`, large `*.npy`, and large `*.npz`: excluded binary data formats.

## Generated Or Runtime Files

- `__pycache__/`
- `.DS_Store`
- `.ipynb_checkpoints/`
- local runtime directories such as `runtime/` or `plots/` if present.

## Deprecated Scientific Material

- Any figure or statistic generated from `all_asteroids.fits`.
- Any `schedule` workflow.
- Any `unknown` asteroid linking workflow.
- Any image-subtraction transient workflow.
- Any old output under nested or superseded output directories, if present.

## External Runtime Dependencies

- Lowell `astorb.dat`
- SPICE kernels such as `de432s.bsp`
- raw GOTTA catalog directories on remote servers

These are needed for full upstream reproduction but are not part of the paper handoff packet.
