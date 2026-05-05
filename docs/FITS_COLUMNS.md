# FITS Columns

Source file: `gotta_asteroids.fits`
Rows: `56230`
Columns: `164`

The table combines predicted known-asteroid ephemerides, the matched source-catalog measurements, SBDB object/orbit metadata, and JPL Horizons geometry/rate columns.

| # | Column | FITS format | Unit | Category | Meaning |
|---:|---|---|---|---|---|
| 1 | `name` | `32A` | `` | Predicted asteroid ephemeris | Predicted asteroid name from the ephemeris query. |
| 2 | `number` | `D` | `` | Predicted asteroid ephemeris | Minor-planet number when available. |
| 3 | `ra` | `D` | `` | Predicted asteroid ephemeris | Predicted asteroid right ascension at the observation epoch, degrees. |
| 4 | `dec` | `D` | `` | Predicted asteroid ephemeris | Predicted asteroid declination at the observation epoch, degrees. |
| 5 | `mag` | `E` | `` | Predicted asteroid ephemeris | Predicted apparent V magnitude from the asteroid ephemeris query. |
| 6 | `source_file` | `34A` | `` | Predicted asteroid ephemeris | Input catalog image/table where this prediction or match was produced. |
| 7 | `epoch` | `D` | `` | Predicted asteroid ephemeris | Observation epoch, stored as MJD. |
| 8 | `objID` | `J` | `` | Catalog source measurement | Detected source identifier from the input catalog. |
| 9 | `A` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 10 | `AErr` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 11 | `B` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 12 | `BErr` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 13 | `PA` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 14 | `PAErr` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 15 | `AB` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 16 | `E` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 17 | `Radius_Kron` | `D` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 18 | `X_Win` | `D` | `` | Catalog source measurement | Windowed x pixel coordinate of the detected source. |
| 19 | `XErr_Win` | `D` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 20 | `Y_Win` | `D` | `` | Catalog source measurement | Windowed y pixel coordinate of the detected source. |
| 21 | `YErr_Win` | `D` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 22 | `RA_Win` | `D` | `` | Catalog source measurement | Measured source right ascension from the windowed catalog centroid, degrees. |
| 23 | `RAErr_Win` | `D` | `` | Catalog source measurement | Uncertainty of windowed RA measurement, degrees in the source catalog. |
| 24 | `DEC_Win` | `D` | `` | Catalog source measurement | Measured source declination from the windowed catalog centroid, degrees. |
| 25 | `DECErr_Win` | `D` | `` | Catalog source measurement | Uncertainty of windowed Dec measurement, degrees in the source catalog. |
| 26 | `Flag` | `I` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 27 | `Flag_ISO` | `J` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 28 | `Flag_ISO_Num` | `J` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 29 | `FWHM` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 30 | `Flux_Kron` | `D` | `` | Kron/catalog photometry | Measured Kron flux of the detected source. |
| 31 | `FluxErr_Kron` | `E` | `` | Kron/catalog photometry | Uncertainty of measured Kron flux. |
| 32 | `Mag_Kron` | `D` | `` | Kron/catalog photometry | Measured Kron magnitude of the detected source. |
| 33 | `MagErr_Kron` | `D` | `` | Kron/catalog photometry | Uncertainty of measured Kron magnitude. |
| 34 | `Class_ANN` | `E` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 35 | `Flux_Aper1` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 36 | `FluxErr_Aper1` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 37 | `Mag_Aper1` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 38 | `MagErr_Aper1` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 39 | `Flux_Aper2` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 40 | `FluxErr_Aper2` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 41 | `Mag_Aper2` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 42 | `MagErr_Aper2` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 43 | `Flux_Aper3` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 44 | `FluxErr_Aper3` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 45 | `Mag_Aper3` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 46 | `MagErr_Aper3` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 47 | `Flux_Aper4` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 48 | `FluxErr_Aper4` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 49 | `Mag_Aper4` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 50 | `MagErr_Aper4` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 51 | `Flux_Aper5` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 52 | `FluxErr_Aper5` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 53 | `Mag_Aper5` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 54 | `MagErr_Aper5` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 55 | `Flux_Aper6` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 56 | `FluxErr_Aper6` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 57 | `Mag_Aper6` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 58 | `MagErr_Aper6` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 59 | `Flux_Aper7` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 60 | `FluxErr_Aper7` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 61 | `Mag_Aper7` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 62 | `MagErr_Aper7` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 63 | `Flux_Aper8` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 64 | `FluxErr_Aper8` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 65 | `Mag_Aper8` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 66 | `MagErr_Aper8` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 67 | `Flux_Aper9` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 68 | `FluxErr_Aper9` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 69 | `Mag_Aper9` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 70 | `MagErr_Aper9` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 71 | `Flux_Aper10` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 72 | `FluxErr_Aper10` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 73 | `Mag_Aper10` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 74 | `MagErr_Aper10` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 75 | `Flux_Aper11` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 76 | `FluxErr_Aper11` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 77 | `Mag_Aper11` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 78 | `MagErr_Aper11` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 79 | `Flux_Aper12` | `E` | `` | Aperture photometry | Catalog aperture flux for the corresponding aperture index. |
| 80 | `FluxErr_Aper12` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture flux for the corresponding aperture index. |
| 81 | `Mag_Aper12` | `E` | `` | Aperture photometry | Catalog aperture magnitude for the corresponding aperture index. |
| 82 | `MagErr_Aper12` | `E` | `` | Aperture photometry | Uncertainty of catalog aperture magnitude for the corresponding aperture index. |
| 83 | `Type` | `J` | `` | Catalog source measurement | Column copied from the matched source catalog or upstream enrichment table. |
| 84 | `R20` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 85 | `R50` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 86 | `R90` | `E` | `` | Source morphology | Column copied from the matched source catalog or upstream enrichment table. |
| 87 | `X_PSF` | `D` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 88 | `Y_PSF` | `D` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 89 | `RA_PSF` | `D` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 90 | `DEC_PSF` | `D` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 91 | `Chi2_PSF` | `E` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 92 | `Flux_PSF` | `E` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 93 | `FluxErr_PSF` | `E` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 94 | `Mag_PSF` | `E` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 95 | `MagErr_PSF` | `E` | `` | PSF photometry | Column copied from the matched source catalog or upstream enrichment table. |
| 96 | `object_des` | `10A` | `` | SBDB object metadata | SBDB primary object designation. |
| 97 | `object_fullname` | `35A` | `` | SBDB object metadata | SBDB full object name. |
| 98 | `object_kind` | `2A` | `` | SBDB object metadata | SBDB object kind code. |
| 99 | `object_neo` | `5A` | `` | SBDB object metadata | SBDB near-Earth-object flag. |
| 100 | `object_orbit_class_code` | `3A` | `` | SBDB object metadata | SBDB orbit class code. |
| 101 | `object_orbit_class_name` | `24A` | `` | SBDB object metadata | SBDB orbit class name, for example Main-belt Asteroid. |
| 102 | `object_orbit_id` | `3A` | `` | SBDB object metadata | Column copied from the matched source catalog or upstream enrichment table. |
| 103 | `object_pha` | `5A` | `` | SBDB object metadata | SBDB potentially hazardous asteroid flag. |
| 104 | `object_prefix` | `A` | `` | SBDB object metadata | Column copied from the matched source catalog or upstream enrichment table. |
| 105 | `object_shortname` | `22A` | `` | SBDB object metadata | Column copied from the matched source catalog or upstream enrichment table. |
| 106 | `object_spkid` | `8A` | `` | SBDB object metadata | JPL/SPICE small-body identifier. |
| 107 | `orbit_comment` | `61A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 108 | `orbit_condition_code` | `A` | `` | SBDB orbit metadata/elements | SBDB orbit uncertainty/condition code. |
| 109 | `orbit_cov_epoch` | `11A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 110 | `orbit_data_arc` | `5A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 111 | `orbit_elements_a` | `8A` | `` | SBDB orbit metadata/elements | SBDB semimajor axis. |
| 112 | `orbit_elements_a_sig` | `10A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_a`. |
| 113 | `orbit_elements_ad` | `8A` | `` | SBDB orbit metadata/elements | SBDB aphelion distance. |
| 114 | `orbit_elements_ad_sig` | `10A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_ad`. |
| 115 | `orbit_elements_e` | `7A` | `` | SBDB orbit metadata/elements | SBDB eccentricity. |
| 116 | `orbit_elements_e_sig` | `7A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_e`. |
| 117 | `orbit_elements_i` | `9A` | `` | SBDB orbit metadata/elements | SBDB inclination. |
| 118 | `orbit_elements_i_sig` | `11A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_i`. |
| 119 | `orbit_elements_ma` | `10A` | `` | SBDB orbit metadata/elements | SBDB mean anomaly. |
| 120 | `orbit_elements_ma_sig` | `11A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_ma`. |
| 121 | `orbit_elements_n` | `16A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 122 | `orbit_elements_n_sig` | `15A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_n`. |
| 123 | `orbit_elements_om` | `9A` | `` | SBDB orbit metadata/elements | SBDB longitude of ascending node. |
| 124 | `orbit_elements_om_sig` | `11A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_om`. |
| 125 | `orbit_elements_per` | `10A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 126 | `orbit_elements_per_sig` | `9A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_per`. |
| 127 | `orbit_elements_q` | `8A` | `` | SBDB orbit metadata/elements | SBDB perihelion distance. |
| 128 | `orbit_elements_q_sig` | `10A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_q`. |
| 129 | `orbit_elements_tp` | `13A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 130 | `orbit_elements_tp_sig` | `9A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_tp`. |
| 131 | `orbit_elements_w` | `10A` | `` | SBDB orbit metadata/elements | SBDB argument of perihelion. |
| 132 | `orbit_elements_w_sig` | `11A` | `` | SBDB orbit metadata/elements | SBDB uncertainty for `orbit_elements_w`. |
| 133 | `orbit_epoch` | `11A` | `` | SBDB orbit metadata/elements | SBDB orbit-element epoch. |
| 134 | `orbit_equinox` | `5A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 135 | `orbit_first_obs` | `10A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 136 | `orbit_last_obs` | `10A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 137 | `orbit_moid` | `10A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 138 | `orbit_moid_jup` | `10A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 139 | `orbit_n_del_obs_used` | `A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 140 | `orbit_n_dop_obs_used` | `A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 141 | `orbit_n_obs_used` | `5A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 142 | `orbit_not_valid_after` | `A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 143 | `orbit_not_valid_before` | `A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 144 | `orbit_orbit_id` | `3A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 145 | `orbit_pe_used` | `5A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 146 | `orbit_producer` | `17A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 147 | `orbit_rms` | `4A` | `` | SBDB orbit metadata/elements | SBDB orbit fit RMS residual. |
| 148 | `orbit_sb_used` | `9A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 149 | `orbit_soln_date` | `19A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 150 | `orbit_source` | `3A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 151 | `orbit_t_jup` | `5A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 152 | `orbit_two_body` | `A` | `` | SBDB orbit metadata/elements | Column copied from the matched source catalog or upstream enrichment table. |
| 153 | `query_failed` | `5A` | `` | SBDB object metadata | String flag from SBDB enrichment indicating whether object metadata query failed. |
| 154 | `query_id` | `10A` | `` | SBDB object metadata | Object identifier used for SBDB/Horizons queries. |
| 155 | `signature_source` | `39A` | `` | SBDB object metadata | Column copied from the matched source catalog or upstream enrichment table. |
| 156 | `signature_version` | `3A` | `` | SBDB object metadata | Column copied from the matched source catalog or upstream enrichment table. |
| 157 | `r_AU` | `D` | `AU` | JPL Horizons apparent geometry | Heliocentric distance at the observation epoch from JPL Horizons. |
| 158 | `delta_AU` | `D` | `AU` | JPL Horizons apparent geometry | Topocentric observer-to-asteroid distance at the observation epoch from JPL Horizons. |
| 159 | `phase_deg` | `D` | `deg` | JPL Horizons apparent geometry | Solar phase angle at the observation epoch from JPL Horizons. |
| 160 | `RA_rate_arcsec_hour` | `D` | `arcsec h-1` | JPL Horizons apparent geometry | Apparent dRA*cosDec rate from JPL Horizons, arcsec/hour. |
| 161 | `DEC_rate_arcsec_hour` | `D` | `arcsec h-1` | JPL Horizons apparent geometry | Apparent dDec rate from JPL Horizons, arcsec/hour. |
| 162 | `ang_rate_arcsec_hour` | `D` | `arcsec h-1` | JPL Horizons apparent geometry | Total apparent sky-plane angular rate, arcsec/hour. |
| 163 | `ang_rate_deg_day` | `D` | `deg d-1` | JPL Horizons apparent geometry | Total apparent sky-plane angular rate, deg/day. |
| 164 | `horizons_failed` | `L` | `` | JPL Horizons apparent geometry | Boolean flag indicating whether the Horizons query failed for that row. |
