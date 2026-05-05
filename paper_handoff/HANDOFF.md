# Paper Handoff Packet

Repository: `gotta-asteroid-known`

Branch: `main`

Source analysis commit: `0a76e4dc8f4ee013dc9d65a39b8a8e46029155b4`

Generated: `2026-05-05 16:27:55 CST`

GitHub repository: https://github.com/xiaoyunao/gotta-asteroid-known

## Repository Summary

This repository contains the GOTTA known-asteroid extraction, enrichment, statistics, and plotting materials for a paper focused on known Solar System object detections in GOTTA prototype data. The final analysis input is the local filtered table `gotta_asteroids.fits`, which is not included in git or this handoff zip because it is a large FITS data product. The tracked repository includes the main processing scripts, method documentation, summary statistics, and final figure products.

## Intended Paper

The intended paper is one article in a broader GOTTA prototype paper series. This specific paper should focus on extracting known asteroids from photometric source catalogs, matching predicted ephemerides to catalog detections, enriching detections with SBDB and JPL Horizons information, and reporting the statistical properties of the resulting known-asteroid sample.

## Recommended Reading Order

1. `DATASET.md`
2. `METHODS.md`
3. `RESULTS_SUMMARY.md`
4. `FIGURE_GUIDE.md`
5. `TABLE_GUIDE.md`
6. `LIMITATIONS.md`
7. `PAPER_NOTES.md`

## Pinned Source Links

These links point to the source analysis commit used to generate this packet:

- README: https://raw.githubusercontent.com/xiaoyunao/gotta-asteroid-known/0a76e4dc8f4ee013dc9d65a39b8a8e46029155b4/README.md
- Method notes: https://raw.githubusercontent.com/xiaoyunao/gotta-asteroid-known/0a76e4dc8f4ee013dc9d65a39b8a8e46029155b4/docs/METHOD_KNOWN_ASTEROID_EXTRACTION.md
- Statistics summary: https://raw.githubusercontent.com/xiaoyunao/gotta-asteroid-known/0a76e4dc8f4ee013dc9d65a39b8a8e46029155b4/docs/GOTTA_STATS.md
- Figure notes: https://raw.githubusercontent.com/xiaoyunao/gotta-asteroid-known/0a76e4dc8f4ee013dc9d65a39b8a8e46029155b4/docs/FIGURES.md

Pinned raw links to the `paper_handoff/` files cannot be self-referentially fixed before the handoff commit exists. Use the zip archive as the authoritative packet, or use the repository `main` branch after the handoff commit is pushed.

## Key Results

- Final GOTTA-only table: `gotta_asteroids.fits` with `56230` detection rows and `164` columns.
- Unique known asteroids: `16053` by both `query_id` and `name`.
- Unique source files: `13253`.
- Observation epochs represented in the final table: `2025-01-17T14:00:58.725` to `2025-06-04T19:07:21.708`.
- UTC dates represented by `epoch`: `73`.
- Dominant orbit class: Main-belt Asteroid, `51058` detections.
- JPL Horizons failed rows: `107`.
- Median predicted ephemeris magnitude `mag`: `18.2215`.
- Median measured Kron magnitude `Mag_Kron`: `17.6633`.
- Median total apparent angular rate: `29.276 arcsec/hour`.

## Final Figures

- `figures/known_object_processing.png`: processing workflow diagram.
- `figures/asteroid_orbits.png`: orbital-element distribution, semimajor axis versus eccentricity and inclination.
- `figures/gotta_radec_healpix_nside64.png`: sky distribution of GOTTA known-asteroid detections in RA/Dec using HEALPix nside 64.

## Final Tables

- `tables/GOTTA_STATS.md`: human-readable statistics summary.
- `tables/gotta_stats.json`: machine-readable statistics summary.
- `tables/FITS_COLUMNS.md`: column dictionary for the final FITS table.

## What ChatGPT Should Write From This Packet

Use this packet to draft a scientific manuscript sectioned around: GOTTA prototype context, known-asteroid extraction from photometric catalogs, ephemeris matching, SBDB/JPL enrichment, statistical results, figures, limitations, and implications for future time-domain survey operation. The paper should be conservative and method-driven. It should not claim unknown-object discovery or moving-object linking.

## Do Not Use / Deprecated Material

Do not use `all_asteroids.fits` for analysis or statistics; it contains data from other telescopes. Do not include `schedule`, `unknown`, image-subtraction transient, or linking workflows as part of this paper's method. Do not infer weather, seeing, exposure-time distributions, limiting magnitudes, or photometric precision beyond what is explicitly present in the repository.
