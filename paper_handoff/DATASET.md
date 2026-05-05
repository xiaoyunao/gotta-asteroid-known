# Dataset

## Data Product

The final analysis data product is `gotta_asteroids.fits`, a filtered GOTTA-only FITS table kept in the repository working directory but intentionally excluded from git and from this handoff zip.

The table has:

| Quantity | Value |
|---|---:|
| Detection rows | 56230 |
| Columns | 164 |
| Unique `query_id` | 16053 |
| Unique `name` | 16053 |
| Unique source files | 13253 |
| UTC dates represented by `epoch` | 73 |
| Epoch range | 2025-01-17T14:00:58.725 to 2025-06-04T19:07:21.708 |

## Telescope And Instrument Context

The repository describes this as a GOTTA prototype known-asteroid analysis. Detailed telescope aperture, detector format, filter set, exposure-time distribution, seeing distribution, and weather metadata were not found in the repository.

## Input Catalogs

The upstream per-exposure inputs are photometric source catalogs, typically named `*_cat.fits` or `*_cat.fits.gz`. Each catalog provides a FITS header with WCS and timing information plus a table of source detections and photometric measurements.

Important source-catalog columns include:

- `RA_Win`, `DEC_Win`: measured source position from the windowed centroid.
- `X_Win`, `Y_Win`: measured source pixel position.
- `Mag_Kron`, `Flux_Kron`, `MagErr_Kron`, `FluxErr_Kron`: Kron photometry.
- `Mag_Aper*`, `Flux_Aper*`: aperture photometry.
- `Mag_PSF`, `Flux_PSF`: PSF photometry when present.
- morphology and quality columns such as `A`, `B`, `PA`, `FWHM`, `Flag`, and related fields.

## Final FITS Table Content

The final table combines four categories of information:

1. Predicted known-asteroid ephemerides: `name`, `number`, `ra`, `dec`, `mag`, `source_file`, `epoch`.
2. Matched source-catalog measurements: centroids, catalog RA/Dec, Kron/aperture/PSF photometry, morphology, and flags.
3. SBDB object and orbit metadata: `object_*`, `orbit_*`, `query_id`, and related query/signature fields.
4. JPL Horizons geometry and motion: `r_AU`, `delta_AU`, `phase_deg`, `RA_rate_arcsec_hour`, `DEC_rate_arcsec_hour`, `ang_rate_arcsec_hour`, `ang_rate_deg_day`, `horizons_failed`.

See `tables/FITS_COLUMNS.md` for the full column dictionary.

## Selection Effects

The final table is a matched known-asteroid detection table, not a complete record of all asteroids passing through the sky during the observing period. It is selected by GOTTA observing cadence and footprint, catalog detection completeness, WCS quality, the asteroid ephemeris query radius, the magnitude prefilter, the CCD footprint filter, and the astrometric match threshold.

## Missing Dataset Details

The following values were not found in the repository and should not be invented in the paper:

- total number of raw images before catalog matching;
- exposure-time distribution;
- filter or band distribution;
- seeing, sky brightness, transparency, and moon conditions;
- calibrated photometric zeropoint method;
- completeness as a function of magnitude or angular rate.
