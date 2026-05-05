# Limitations

## Data Limitations

The final data product is a matched known-asteroid detection table. It is not a complete survey exposure database, a raw image archive, or a complete set of all asteroid predictions over the survey footprint.

## Selection Effects And Incompleteness

The sample is selected by observing footprint, cadence, catalog source extraction, WCS quality, ephemeris query radius, predicted-magnitude filtering, CCD footprint filtering, and astrometric matching. It should not be interpreted as a complete asteroid population sample.

## Photometric Caveats

The table includes catalog photometry such as `Mag_Kron`, aperture magnitudes, and PSF magnitudes. The repository does not document a full photometric calibration validation, color-term treatment, or photometric precision analysis. Do not claim a calibrated limiting magnitude or photometric accuracy unless additional analysis is added.

## Astrometric Caveats

The method uses WCS-based catalog positions and ephemeris matching. The repository documents match thresholds, but it does not provide final astrometric residual histograms or a false-match-rate analysis. Do not overstate astrometric precision.

## Weather, Seeing, And Background

Seeing, weather, moon phase, sky background, and transparency statistics were not found in the repository. These should not be inferred from the current packet.

## Catalog Matching Limitations

The same predicted object can be detected multiple times, and the final table is row-based. Repeated detections must be handled explicitly when object-level statistics are needed. Objects near chip edges or in crowded fields may be underrepresented.

## External Catalog Limitations

SBDB and JPL Horizons enrichment depends on external services and object identifiers. JPL Horizons failed for `107` rows. The repository does not include a detailed explanation of those failures.

## Claims To Avoid

- Do not claim discovery of unknown asteroids.
- Do not claim moving-object tracklet linking.
- Do not claim survey completeness.
- Do not claim a formal limiting magnitude.
- Do not claim validated photometric or astrometric precision beyond the columns and summaries present here.
- Do not use `all_asteroids.fits` for GOTTA-only conclusions.
