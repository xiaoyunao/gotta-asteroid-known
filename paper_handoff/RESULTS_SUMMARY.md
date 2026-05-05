# Results Summary

## Sample Size

The filtered GOTTA-only known-asteroid table contains `56230` matched detection rows and `16053` unique objects by `query_id` and by `name`. The detections come from `13253` unique source files and cover `73` UTC dates between `2025-01-17T14:00:58.725` and `2025-06-04T19:07:21.708`.

## Orbit-Class Composition

| Orbit class | Detections |
|---|---:|
| Main-belt Asteroid | 51058 |
| Outer Main-belt Asteroid | 1970 |
| Jupiter Trojan | 1362 |
| Inner Main-belt Asteroid | 897 |
| Mars-crossing Asteroid | 656 |
| Amor | 139 |
| Apollo | 101 |
| TransNeptunian Object | 20 |
| Aten | 19 |
| Centaur | 5 |
| Asteroid | 3 |

The sample is therefore dominated by main-belt asteroids, with smaller but visible contributions from outer/inner main-belt objects, Jupiter Trojans, Mars-crossers, and near-Earth asteroid classes.

## Magnitudes And Geometry

| Quantity | Median | P16 | P84 | Min | Max |
|---|---:|---:|---:|---:|---:|
| Predicted magnitude `mag` | 18.2215 | 17.0180 | 18.9925 | 7.9536 | 22.6508 |
| Measured `Mag_Kron` | 17.6633 | 16.5549 | 18.3395 | 9.4256 | 21.7955 |
| Angular rate, arcsec/hour | 29.2760 | 14.2393 | 39.7301 | 0.0488 | 1259.32 |
| Angular rate, deg/day | 0.1952 | 0.0949 | 0.2649 | 0.0003 | 8.3955 |
| Heliocentric distance, AU | 2.5807 | 2.1468 | 3.0999 | 0.9230 | 52.7078 |
| Topocentric distance, AU | 1.8395 | 1.3134 | 2.4891 | 0.0542 | 52.3104 |
| Phase angle, deg | 13.2451 | 5.2106 | 21.8789 | 0.0090 | 84.3846 |

These statistics are suitable for describing the brightness range, apparent motion distribution, and observing geometry of the known-asteroid detections. They should not be used alone as a calibrated limiting-magnitude measurement or completeness function.

## Per-Object Repeats

The table contains repeated detections for many objects. The per-object detection count has median `2`, mean `3.50277`, 16th percentile `1`, 84th percentile `6`, and maximum `317`.

## Enrichment Completeness

JPL Horizons enrichment failed for `107` rows. The repository does not contain a deeper failure-mode analysis, so papers should state this as a small number of failed rows rather than interpreting it physically.

## Robust Conclusions

- GOTTA prototype catalog products can be used to recover a large sample of known asteroid detections through ephemeris-based matching.
- The matched sample is dominated by main-belt asteroids, as expected for known-object detections in typical survey fields.
- The final data product combines predicted ephemerides, measured catalog photometry, SBDB orbit metadata, and JPL Horizons geometry/rate information.
- The output supports orbit-distribution and sky-distribution visualization for a GOTTA known-asteroid paper.

## Preliminary Or Uncertain Conclusions

The repository does not yet provide calibrated completeness, false-match rate, night-by-night detection efficiency, photometric precision validation, astrometric residual distributions, or weather/seeing dependence. Those topics can be discussed as future work or as missing analysis, but they should not be presented as measured results from this packet.
