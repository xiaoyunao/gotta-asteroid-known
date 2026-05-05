# Figure Guide

## Figure 1 Candidate: `known_object_processing.png`

- Original path: `outputs/known_object_processing.png`
- Handoff path: `figures/known_object_processing.png`
- Recommended paper section: Methods
- Status: final/candidate
- Main message: End-to-end known-object processing flow from catalogs to enriched known-asteroid detections.
- Suggested caption: "Workflow for extracting known asteroid detections from GOTTA photometric catalogs. For each exposure, the catalog WCS and timing define the field footprint and epoch; known-object ephemerides are queried, filtered to the CCD footprint, matched to catalog detections, and then enriched with SBDB and JPL Horizons information."
- Caveats: The content was manually supplied by the user; use it as a workflow schematic, not as an automatically generated data product.

## Figure 2 Candidate: `asteroid_orbits.png`

- Original path: `outputs/asteroid_orbits.png`
- Handoff path: `figures/asteroid_orbits.png`
- Recommended paper section: Results
- Status: final
- Main message: The detected known asteroids occupy the expected orbital-element regions, dominated by main-belt objects with additional populations such as Trojans and near-Earth asteroid classes.
- Suggested caption: "Orbital-element distribution of GOTTA known-asteroid detections after SBDB enrichment. Points are grouped by SBDB orbit class. The panels show semimajor axis versus eccentricity and semimajor axis versus inclination."
- Caveats: The figure is generated from detected rows, not a debiased intrinsic asteroid population.

## Figure 3 Candidate: `gotta_radec_healpix_nside64.png`

- Original path: `outputs/gotta_radec_healpix_nside64.png`
- Handoff path: `figures/gotta_radec_healpix_nside64.png`
- Recommended paper section: Results or Survey Footprint
- Status: final
- Main message: The known-asteroid detections occupy the GOTTA observed sky footprint and show structured density in RA/Dec.
- Suggested caption: "Sky distribution of GOTTA known-asteroid detections in equatorial coordinates. Detections are binned with HEALPix nside 64 and plotted in a Mollweide projection. The logarithmic color scale is clipped at 100 detections per pixel for readability."
- Caveats: This is a detection-density map, not an exposure-time map or completeness map.

## Deprecated Or Alternative Figures

No deprecated final figures are included in this handoff packet. Earlier all-data or non-GOTTA figures should be ignored because the current paper must use `gotta_asteroids.fits`, not `all_asteroids.fits`.
