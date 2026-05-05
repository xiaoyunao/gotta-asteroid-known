# Paper Notes For ChatGPT

## Target Paper Type

This should be written as a GOTTA prototype data-processing and science-validation paper focused on known asteroid extraction and statistics. It belongs to a broader paper series covering the telescope, photometric processing, image subtraction/transients, and light curves, but this manuscript should stay focused on known asteroids.

## Suggested Titles

- "Known Asteroid Recovery in GOTTA Prototype Survey Data"
- "Extracting Known Solar System Objects from GOTTA Photometric Catalogs"
- "A GOTTA Prototype Analysis of Known Asteroid Detections"

## Suggested Abstract Structure

1. Briefly introduce GOTTA as a prototype time-domain survey system.
2. State that this paper focuses on known asteroid recovery from photometric catalogs.
3. Summarize the ephemeris-query, WCS-footprint, catalog-matching, SBDB, and JPL Horizons workflow.
4. Report the sample size: `56230` detections and `16053` unique known asteroids.
5. Mention the dominant main-belt population and the final orbit/sky-distribution figures.
6. End with a conservative statement that this validates the known-object extraction workflow and provides a baseline for future GOTTA moving-object analyses.

## Suggested Section Structure

1. Introduction
2. GOTTA Data And Photometric Catalogs
3. Known-Asteroid Matching Pipeline
4. SBDB And JPL Horizons Enrichment
5. Results
6. Discussion
7. Limitations And Future Work
8. Summary

## Main Storyline

The manuscript should present a practical, reproducible pipeline: starting from calibrated photometric source catalogs, the system determines the exposure footprint and midpoint, queries known asteroid ephemerides, filters candidates to the actual CCD footprint, matches predictions to catalog sources, and produces an enriched table that can support population statistics and figures.

## Claims To Emphasize

- The project demonstrates a complete known-object extraction workflow for GOTTA prototype data.
- The final table combines measured photometry with external small-body metadata and observing geometry.
- The sample is large enough to show clear main-belt dominance and meaningful sky/orbit distributions.
- The workflow is intentionally separate from unknown-object discovery and linking.

## Claims To Avoid

- Avoid saying the pipeline discovers new asteroids.
- Avoid claiming completeness or detection efficiency without additional injection/recovery or exposure-map analysis.
- Avoid presenting `Mag_Kron` statistics as a calibrated survey limiting magnitude.
- Avoid detailed claims about weather, seeing, or exposure conditions unless additional metadata are supplied.

## Tone

Use a conservative scientific tone. Prefer "the sample contains", "the pipeline recovers", and "the results demonstrate" over stronger claims like "complete", "unbiased", or "fully characterized".
