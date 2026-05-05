# Known-Asteroid Extraction Method

本说明面向论文写作，重点解释如何从 GOTTA 测光星表得到已知小行星的测光信息。
后续统计和画图只使用本地筛选后的 `gotta_asteroids.fits`。

## Scope

本项目只处理已知小行星：

- 不处理 `schedule`
- 不处理未知小行星 linking
- 不处理图像相减暂现源
- 不再从 `all_asteroids.fits` 做统计，因为其中混有其他望远镜数据

## Input Catalogs

每个 GOTTA 曝光对应一个测光源表，典型输入为 `*_cat.fits` 或 `*_cat.fits.gz`。
处理脚本读取 catalog HDU 中的：

- FITS header: WCS、观测时间、曝光时间、图像尺寸
- FITS table: 源检测和测光列，例如 `RA_Win`, `DEC_Win`, `Mag_Kron`, `Flux_Kron`, aperture photometry, PSF photometry, shape parameters

主参考程序：

- `smt_known_asteroid/match_single_night.py`
- `remote_foundation/sitian_match_asteriod_multi.py`

## Per-Exposure Processing

### 1. 读取测光星表和 WCS

程序对每个 catalog 打开 FITS 文件，读取指定 HDU 的 header 和 table，并构造 `astropy.wcs.WCS`。
WCS 后续用于两件事：

1. 把图像角点像素坐标转换为天球坐标，确定曝光视场范围
2. 把星历预测的 RA/Dec 转回像素坐标，判断小行星是否实际落在 CCD 内

### 2. 确定观测时刻

观测时刻取曝光中点，而不是曝光开始时刻：

```text
epoch = DATE-OBS + EXPTIME / 2
```

工程脚本会按优先级读取 `OBS_DATE`, `DATE-OBS`, `DATEOBS` 等关键字。
输出表中的 `epoch` 存为 MJD。

### 3. 确定视场中心和半径

对每个曝光，程序读取图像尺寸 `NAXIS1/NAXIS2`，然后取四个角点：

```text
(1, 1), (1, ny), (nx, 1), (nx, ny)
```

通过 WCS 将角点转成 RA/Dec。视场中心使用图像中心像素的 WCS 坐标：

```text
field_center = WCS.pixel_to_world((nx + 1)/2, (ny + 1)/2)
```

视场搜索半径取中心到四个角点的最大角距离，再加小的边界余量：

```text
field_radius = max(separation(center, corners)) + corner_pad
confidence_radius = field_radius + confidence_pad
```

当前工程脚本默认：

- `corner_pad = 0.05 deg`
- `confidence_pad = 0.5 deg`

这样可以覆盖 WCS 边缘误差和星历查询边界误差。

### 4. 查询视场内已知小行星星历

程序用 `aleph.Query` 调用 Lowell/`astorb.dat` 小行星星历：

```python
q = Query(service="Lowell", filename="astorb.dat")
ephs = q.query_mixed_cat(
    field_center=field_center,
    radius=field_radius,
    epoch=epoch,
    observer=observer,
    njobs=njobs,
    confidence_radius=confidence_radius,
)
```

观测站位置使用兴隆站坐标：

```text
lon = 117.575 deg
lat = 40.393 deg
height = 960 m
```

查询结果先按预测星等过滤。工程脚本默认 `mag_limit = 22.5`，远端 GOTTA 原始脚本中使用过 `mag_limit = 23`。
保留的预测列包括：

- `name`
- `number`
- `ra`
- `dec`
- `mag`
- `source_file`
- `epoch`

### 5. 筛选实际落入 CCD 的预测目标

星历查询按圆形视场返回候选目标，但圆形区域会包含 CCD 外部目标。
程序将每个候选目标的预测 RA/Dec 通过 WCS 转成像素坐标：

```python
x_pix, y_pix = w.all_world2pix(ephs["ra"], ephs["dec"], 1)
inside = (x_pix >= 1) & (x_pix <= nx) & (y_pix >= 1) & (y_pix <= ny)
```

只有落在 CCD 有效像素范围内的候选目标进入后续匹配。

### 6. 与测光源表做角距离匹配

预测小行星坐标和测光源表坐标分别构造成 `SkyCoord`：

```python
asteroid_coords = SkyCoord(ephs["ra"], ephs["dec"], unit="deg")
cat_coords = SkyCoord(cat["RA_Win"], cat["DEC_Win"], unit="deg")
idx, sep2d, _ = match_coordinates_sky(asteroid_coords, cat_coords)
matched = sep2d < sep_limit
```

工程脚本默认匹配半径为 `1 arcsec`；早期远端脚本使用过 `3 arcsec`。
`smt_known_asteroid/match_single_night.py` 还支持星等一致性过滤：

```text
abs(predicted_mag - Mag_Kron) < magdiff
```

匹配成功后，程序把小行星预测星历表和测光源表按行横向合并：

```python
combined = hstack([matched_ast, matched_cat], join_type="exact")
```

这一步得到的就是“已知小行星测光 detection”。

## Night-Level And Global Products

单曝光或单夜程序会写出：

- `<night>_all_asteroids.fits`: 该夜所有落入视场的已知小行星预测目标
- `<night>_matched_asteroids.fits`: 与测光源表成功匹配的 detection

如果按文件并行运行：

- `smt_known_asteroid/merge_night_parts.py` 合并 per-file 结果

如果要构建长期历史表：

- `smt_known_asteroid/update_all_matched_history.py` 增量合并多夜 `*_matched_asteroids.fits`

当前论文统计使用筛选后的：

```text
gotta_asteroids.fits
```

## SBDB Enrichment

匹配 detection 之后，再按小行星编号或名称查询 NASA/JPL SBDB，补充小行星身份和轨道信息。
相关参考程序：

- `remote_foundation/asteroids_stats_pre.py`

主要补充列：

- `object_des`
- `object_fullname`
- `object_orbit_class_code`
- `object_orbit_class_name`
- `object_spkid`
- `orbit_elements_a`
- `orbit_elements_e`
- `orbit_elements_i`
- `orbit_elements_q`
- `orbit_elements_om`
- `orbit_elements_w`
- `orbit_epoch`
- `orbit_condition_code`
- `orbit_rms`

这些列用于轨道族统计和 `asteroid_orbits.png`。

## JPL Horizons Enrichment

`remote_foundation/asteroids_jpl.py` 按 `query_id` 和观测 JD 分组查询 JPL Horizons。
一次查询同一目标多个观测历元，减少网络请求量。

补充列：

- `r_AU`: 日心距
- `delta_AU`: 站心距
- `phase_deg`: 相位角
- `RA_rate_arcsec_hour`: `dRA*cosDec/dt`
- `DEC_rate_arcsec_hour`: `dDec/dt`
- `ang_rate_arcsec_hour`: 天球面总角速度
- `ang_rate_deg_day`: 天球面总角速度，单位 deg/day
- `horizons_failed`: Horizons 查询失败标记

这些列用于运动速度、距离和观测几何统计。

## Plot And Statistics Entry Points

当前本地分析统一使用：

```bash
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/plot_gotta_asteroids.py gotta_asteroids.fits --outdir outputs
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/summarize_gotta_asteroids.py gotta_asteroids.fits --md-out docs/GOTTA_STATS.md --json-out outputs/gotta_stats.json
python3 scripts/describe_fits_columns.py gotta_asteroids.fits --out docs/FITS_COLUMNS.md
```

其中：

- `outputs/asteroid_orbits.png` 严格沿用原 `asteroid_orbits` 图的绘图格式
- `outputs/gotta_radec_healpix_nside64.png` 沿用原 notebook 的 healpix/Mollweide RA-Dec 密度图逻辑，并统一到轨道图字体风格
- `docs/GOTTA_STATS.md` 是当前可直接给论文草稿使用的统计摘要
