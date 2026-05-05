#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from astropy.io import fits


def category_for(name: str) -> str:
    if name in {"name", "number", "ra", "dec", "mag", "source_file", "epoch"}:
        return "Predicted asteroid ephemeris"
    if name.startswith("object_") or name in {"query_id", "query_failed", "signature_source", "signature_version"}:
        return "SBDB object metadata"
    if name.startswith("orbit_"):
        return "SBDB orbit metadata/elements"
    if name in {
        "r_AU",
        "delta_AU",
        "phase_deg",
        "RA_rate_arcsec_hour",
        "DEC_rate_arcsec_hour",
        "ang_rate_arcsec_hour",
        "ang_rate_deg_day",
        "horizons_failed",
    }:
        return "JPL Horizons apparent geometry"
    if name.startswith(("Flux_Aper", "FluxErr_Aper", "Mag_Aper", "MagErr_Aper")):
        return "Aperture photometry"
    if name.endswith("_PSF") or name in {"Chi2_PSF", "FluxErr_PSF", "MagErr_PSF"}:
        return "PSF photometry"
    if name in {"A", "AErr", "B", "BErr", "PA", "PAErr", "AB", "E", "Radius_Kron", "FWHM", "R20", "R50", "R90"}:
        return "Source morphology"
    if name.startswith(("X", "Y", "RA", "DEC")) or name in {"objID", "Flag", "Flag_ISO", "Flag_ISO_Num", "Type", "Class_ANN"}:
        return "Catalog source measurement"
    if name.startswith(("Flux", "FluxErr", "Mag", "MagErr")):
        return "Kron/catalog photometry"
    return "Other catalog column"


DESCRIPTIONS = {
    "name": "Predicted asteroid name from the ephemeris query.",
    "number": "Minor-planet number when available.",
    "ra": "Predicted asteroid right ascension at the observation epoch, degrees.",
    "dec": "Predicted asteroid declination at the observation epoch, degrees.",
    "mag": "Predicted apparent V magnitude from the asteroid ephemeris query.",
    "source_file": "Input catalog image/table where this prediction or match was produced.",
    "epoch": "Observation epoch, stored as MJD.",
    "objID": "Detected source identifier from the input catalog.",
    "RA_Win": "Measured source right ascension from the windowed catalog centroid, degrees.",
    "DEC_Win": "Measured source declination from the windowed catalog centroid, degrees.",
    "RAErr_Win": "Uncertainty of windowed RA measurement, degrees in the source catalog.",
    "DECErr_Win": "Uncertainty of windowed Dec measurement, degrees in the source catalog.",
    "X_Win": "Windowed x pixel coordinate of the detected source.",
    "Y_Win": "Windowed y pixel coordinate of the detected source.",
    "Mag_Kron": "Measured Kron magnitude of the detected source.",
    "MagErr_Kron": "Uncertainty of measured Kron magnitude.",
    "Flux_Kron": "Measured Kron flux of the detected source.",
    "FluxErr_Kron": "Uncertainty of measured Kron flux.",
    "object_des": "SBDB primary object designation.",
    "object_fullname": "SBDB full object name.",
    "object_kind": "SBDB object kind code.",
    "object_neo": "SBDB near-Earth-object flag.",
    "object_pha": "SBDB potentially hazardous asteroid flag.",
    "object_orbit_class_code": "SBDB orbit class code.",
    "object_orbit_class_name": "SBDB orbit class name, for example Main-belt Asteroid.",
    "object_spkid": "JPL/SPICE small-body identifier.",
    "orbit_elements_a": "SBDB semimajor axis.",
    "orbit_elements_e": "SBDB eccentricity.",
    "orbit_elements_i": "SBDB inclination.",
    "orbit_elements_q": "SBDB perihelion distance.",
    "orbit_elements_ad": "SBDB aphelion distance.",
    "orbit_elements_om": "SBDB longitude of ascending node.",
    "orbit_elements_w": "SBDB argument of perihelion.",
    "orbit_elements_ma": "SBDB mean anomaly.",
    "orbit_epoch": "SBDB orbit-element epoch.",
    "orbit_rms": "SBDB orbit fit RMS residual.",
    "orbit_condition_code": "SBDB orbit uncertainty/condition code.",
    "query_failed": "String flag from SBDB enrichment indicating whether object metadata query failed.",
    "query_id": "Object identifier used for SBDB/Horizons queries.",
    "r_AU": "Heliocentric distance at the observation epoch from JPL Horizons.",
    "delta_AU": "Topocentric observer-to-asteroid distance at the observation epoch from JPL Horizons.",
    "phase_deg": "Solar phase angle at the observation epoch from JPL Horizons.",
    "RA_rate_arcsec_hour": "Apparent dRA*cosDec rate from JPL Horizons, arcsec/hour.",
    "DEC_rate_arcsec_hour": "Apparent dDec rate from JPL Horizons, arcsec/hour.",
    "ang_rate_arcsec_hour": "Total apparent sky-plane angular rate, arcsec/hour.",
    "ang_rate_deg_day": "Total apparent sky-plane angular rate, deg/day.",
    "horizons_failed": "Boolean flag indicating whether the Horizons query failed for that row.",
}


def description_for(name: str) -> str:
    if name in DESCRIPTIONS:
        return DESCRIPTIONS[name]
    if name.startswith("orbit_elements_") and name.endswith("_sig"):
        base = name.removesuffix("_sig")
        return f"SBDB uncertainty for `{base}`."
    if name.startswith("Flux_Aper"):
        return "Catalog aperture flux for the corresponding aperture index."
    if name.startswith("FluxErr_Aper"):
        return "Uncertainty of catalog aperture flux for the corresponding aperture index."
    if name.startswith("Mag_Aper"):
        return "Catalog aperture magnitude for the corresponding aperture index."
    if name.startswith("MagErr_Aper"):
        return "Uncertainty of catalog aperture magnitude for the corresponding aperture index."
    return "Column copied from the matched source catalog or upstream enrichment table."


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown column dictionary for a FITS table.")
    parser.add_argument("fits_path", nargs="?", default="gotta_asteroids.fits")
    parser.add_argument("--out", default="docs/FITS_COLUMNS.md")
    args = parser.parse_args()

    fits_path = Path(args.fits_path)
    out_path = Path(args.out)

    with fits.open(fits_path, memmap=True) as hdul:
        hdu = hdul[1]
        n_rows = len(hdu.data)
        columns = list(hdu.columns)

    lines = [
        "# FITS Columns",
        "",
        f"Source file: `{fits_path}`",
        f"Rows: `{n_rows}`",
        f"Columns: `{len(columns)}`",
        "",
        "The table combines predicted known-asteroid ephemerides, the matched source-catalog measurements, SBDB object/orbit metadata, and JPL Horizons geometry/rate columns.",
        "",
        "| # | Column | FITS format | Unit | Category | Meaning |",
        "|---:|---|---|---|---|---|",
    ]
    for idx, col in enumerate(columns, 1):
        unit = col.unit or ""
        lines.append(
            f"| {idx} | `{col.name}` | `{col.format}` | `{unit}` | "
            f"{category_for(col.name)} | {description_for(col.name)} |"
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
