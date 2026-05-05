# Handoff Manifest

This file lists the contents of `paper_handoff/`. File sizes are approximate local sizes at packet generation time.

## Core Markdown Files

| Path | Type | Description | Status | Size |
|---|---|---|---|---:|
| `HANDOFF.md` | Markdown | Main entry point and reading order for ChatGPT. | final | 4.2K |
| `MANIFEST.md` | Markdown | This file list. | final | 4.0K |
| `DATASET.md` | Markdown | Dataset summary and known missing metadata. | final | 2.9K |
| `METHODS.md` | Markdown | End-to-end known-asteroid extraction method. | final | 4.6K |
| `RESULTS_SUMMARY.md` | Markdown | Paper-ready numerical results summary. | final | 3.1K |
| `FIGURE_GUIDE.md` | Markdown | Figure captions, messages, and caveats. | final | 2.5K |
| `TABLE_GUIDE.md` | Markdown | Table descriptions and suggested use. | final | 1.3K |
| `LIMITATIONS.md` | Markdown | Conservative limitations and claims to avoid. | final | 2.2K |
| `REPRODUCE.md` | Markdown | Commands and environment notes for reproduction. | final | 2.4K |
| `PAPER_NOTES.md` | Markdown | Direct manuscript guidance for ChatGPT. | final | 2.8K |
| `FILES_TO_IGNORE.md` | Markdown | Deprecated, large, or irrelevant files to ignore. | final | 1.1K |

## Figures

| Path | Type | Description | Status | Size |
|---|---|---|---|---:|
| `figures/known_object_processing.png` | PNG | Known-object processing workflow diagram. | final/candidate | 268K |
| `figures/asteroid_orbits.png` | PNG | Orbit-element distribution figure. | final | 845K |
| `figures/gotta_radec_healpix_nside64.png` | PNG | RA/Dec HEALPix sky distribution figure. | final | 1.6M |

## Tables

| Path | Type | Description | Status | Size |
|---|---|---|---|---:|
| `tables/GOTTA_STATS.md` | Markdown | Human-readable numerical statistics. | final | 1.5K |
| `tables/gotta_stats.json` | JSON | Machine-readable numerical statistics. | auxiliary | 2.4K |
| `tables/FITS_COLUMNS.md` | Markdown | FITS column dictionary. | reference | 21K |

## Script References

| Path | Type | Description | Status | Size |
|---|---|---|---|---:|
| `scripts_reference/build_file_manifest.py` | Python | Build a catalog file manifest. | reference | 3.2K |
| `scripts_reference/match_single_night.py` | Python | Main known-asteroid matching workflow. | reference | 12K |
| `scripts_reference/merge_night_parts.py` | Python | Merge per-file match products. | reference | 1.6K |
| `scripts_reference/update_all_matched_history.py` | Python | Merge night-level products into history table. | reference | 4.1K |
| `scripts_reference/asteroids_jpl.py` | Python | JPL Horizons enrichment reference. | reference | 7.8K |
| `scripts_reference/asteroids_stats_pre.py` | Python | SBDB enrichment reference. | reference | 6.7K |
| `scripts_reference/sitian_match_asteriod_multi.py` | Python | Original remote multi-process matching reference. | reference | 8.0K |
| `scripts_reference/plot_gotta_asteroids.py` | Python | Final plotting script. | reference | 7.9K |
| `scripts_reference/summarize_gotta_asteroids.py` | Python | Final statistics script. | reference | 5.3K |
| `scripts_reference/describe_fits_columns.py` | Python | FITS column dictionary generator. | reference | 6.9K |

## Useful Files Outside The Packet

| Path | Reason not copied |
|---|---|
| `gotta_asteroids.fits` | Large final FITS table; required for local regeneration but excluded from zip and git. |
| `README.md` | Repository overview; summarized in `HANDOFF.md`. |
| `docs/METHOD_KNOWN_ASTEROID_EXTRACTION.md` | Source method document; distilled into `METHODS.md`. |
| `docs/PROCESSING_ORDER.md` | Source script-order document; distilled into `METHODS.md` and `REPRODUCE.md`. |
| `docs/FIGURES.md` | Source figure notes; distilled into `FIGURE_GUIDE.md`. |
| `WORKLOG.md` and `PLAN.md` | Project continuity notes; useful for development history, not required for paper drafting. |
