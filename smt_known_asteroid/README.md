# Known-Asteroid Mainline Scripts

This directory keeps only the SMT-derived scripts that are part of the known-asteroid extraction mainline.

## Scripts

- `build_file_manifest.py`: scan input catalog files for a night.
- `match_single_night.py`: query known-asteroid ephemerides for each exposure and match predictions to catalog detections.
- `merge_night_parts.py`: merge per-file match products into night-level FITS tables.
- `update_all_matched_history.py`: merge night-level matched detections into a cumulative history table.

Large runtime files such as `astorb.dat`, SPICE kernels, FITS products, and plots are not tracked.

