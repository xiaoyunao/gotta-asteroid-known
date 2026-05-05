# GOTTA Known-Asteroid Statistics

Source file: `gotta_asteroids.fits`

## Basic Counts

- Detection rows: `56230`
- Columns: `164`
- Unique `query_id`: `16053`
- Unique `name`: `16053`
- Unique source files: `13253`
- UTC epoch range: `2025-01-17T14:00:58.725` to `2025-06-04T19:07:21.708`
- Number of UTC dates represented by `epoch`: `73`
- JPL Horizons failed rows: `107`

## Orbit Class Counts

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

## Numeric Columns

| Column | N | Min | P16 | Median | Mean | P84 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| `mag` | 56230 | 7.95358 | 17.018 | 18.2215 | 17.9583 | 18.9925 | 22.6508 |
| `Mag_Kron` | 56230 | 9.42562 | 16.5549 | 17.6633 | 17.3979 | 18.3395 | 21.7955 |
| `ang_rate_arcsec_hour` | 56123 | 0.04882 | 14.2393 | 29.276 | 29.0229 | 39.7301 | 1259.32 |
| `ang_rate_deg_day` | 56123 | 0.000325467 | 0.0949284 | 0.195174 | 0.193486 | 0.264867 | 8.39547 |
| `r_AU` | 56123 | 0.923043 | 2.14679 | 2.58071 | 2.67568 | 3.09992 | 52.7078 |
| `delta_AU` | 56123 | 0.0541518 | 1.31337 | 1.83952 | 1.95019 | 2.48912 | 52.3104 |
| `phase_deg` | 56123 | 0.009 | 5.21061 | 13.2451 | 13.6635 | 21.8789 | 84.3846 |
| `detections_per_object` | 16053 | 1 | 1 | 2 | 3.50277 | 6 | 317 |
