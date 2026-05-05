# GOTTA Known-Asteroid Processing Order

本项目只整理“已知小行星探测、SBDB/JPL 信息补齐、结果画图”相关程序。
`schedule`、`unknown`、Rubin 第三方模拟库不作为 GOTTA 这条处理链的一部分。

## 1. 输入数据

- 当前论文分析数据文件: `gotta_asteroids.fits`
- 历史来源文件: `all_asteroids.fits`
- 注意: 后续统计和分析都不能直接用 `all_asteroids.fits`，因为其中包含其他望远镜数据
- 当前 GOTTA 筛选表规模: `56230` 行、`164` 列
- 当前唯一小行星数:
  - `query_id`: `16053`
  - `name`: `16053`
- JPL Horizons 失败行: `107`

`gotta_asteroids.fits` 是筛选后的大数据产品，保留在工作区但不提交 git。

## 2. 主要处理程序

按推荐先后顺序使用：

| 顺序 | 程序 | 用途 |
|---:|---|---|
| 1 | `smt_known_asteroid/build_file_manifest.py` | 扫描夜间 L2/L4 文件，建立待处理 catalog 清单。 |
| 2 | `smt_known_asteroid/match_single_night.py` | 逐夜读取 catalog，使用 `aleph.Query` / Lowell `astorb.dat` 预测视场内已知小行星，并与 catalog 的 `RA_Win` / `DEC_Win` 做角距离匹配。 |
| 3 | `smt_known_asteroid/merge_night_parts.py` | 如果单夜按文件并行跑，把 per-file `_all_asteroids.fits` 和 `_matched_asteroids.fits` 合并成夜级结果。 |
| 4 | `smt_known_asteroid/update_all_matched_history.py` | 把多个夜次的 `*_matched_asteroids.fits` 增量汇总成总历史表。 |
| 5 | `smt_known_asteroid/export_ades.py` | 如需提交 MPC，按 ADES PSV 格式导出已匹配 detections。GOTTA 当前整理重点不是提交，可作为后续工具保留。 |
| 6 | `remote_foundation/asteroids_jpl.py` | 对总表按 `query_id + epoch` 批量查询 JPL Horizons，补 `r_AU`、`delta_AU`、`phase_deg`、RA/Dec 角速度和总角速度。 |
| 7 | `smt_known_asteroid/make_ppt_known_object_plots.py` | 参考 SMT 项目的汇报绘图入口：补 SBDB/astorb 轨道族，画轨道分布、RA/Dec 密度和探测次数直方图。 |
| 8 | `scripts/plot_gotta_asteroids.py` | 当前论文图入口，只读 `gotta_asteroids.fits`，输出轨道分布图和 RA/Dec healpix 分布图。 |
| 9 | `scripts/summarize_gotta_asteroids.py` | 当前统计入口，只读 `gotta_asteroids.fits`，输出 `docs/GOTTA_STATS.md` 和 JSON。 |
| 10 | `scripts/describe_fits_columns.py` | 读取 FITS header，生成字段说明文档 `docs/FITS_COLUMNS.md`。 |

## 3. 远端 `/Volumes/Foundation/Asteroid` 中有用的参考程序

这些文件已拷贝到 `remote_foundation/`，保留原始写法，便于追溯。

| 文件 | 判断 |
|---|---|
| `remote_foundation/sitian_match_asteriod_multi.py` | 有用。原始 GOTTA/L2 批处理版本，按日期分组，多进程匹配 catalog 和已知小行星。 |
| `remote_foundation/sitian_match_asteriod.py` | 有用。较早的单目录版本，逻辑清楚，适合对照主流程。 |
| `remote_foundation/match_asteroid.py` | 有用。SMT 早期主处理脚本，与后来的 `smt_known_asteroid/match_single_night.py` 对应。 |
| `remote_foundation/asteroids_jpl.py` | 重要。JPL Horizons 信息补齐脚本，当前 `all_asteroids.fits` 最后 8 列来自这类逻辑。 |
| `remote_foundation/asteroids_stats.py` | 有用但次选。根据 SBDB 轨道根数本地传播计算几何量，依赖 `poliastro`，维护成本高于 Horizons 查询。 |
| `remote_foundation/asteroids_stats_pre.py` | 有用。SBDB 信息预处理/补齐参考。 |
| `remote_foundation/sitian_stats.ipynb` | 重要。原始 `asteroid_orbits` 和全体 RA/Dec 分布图 notebook。 |
| `remote_foundation/test_sbdb.ipynb` | 有用。SBDB 字段和接口测试参考。 |
| `remote_foundation/astorb/*.py` | 有用。`astorb.dat` 相关辅助代码。 |
| `remote_foundation/make_marker.py` | 次要。可用于 cutout/图片上标注检测目标，不是主流程必需。 |

## 4. 参考 SMT 项目迁移内容

`smt_known_asteroid/` 来自 `/Users/island/Desktop/smt_asteroid/known_asteroid`，是更工程化的一版：

- 参数化命令行入口比远端 notebook/脚本更适合复跑
- 已拆分 per-file、per-night、history update、ADES export 和 plotting
- 不包含 `schedule` 和 `unknown` 流程
- 大依赖 `astorb.dat`、`de432s.bsp` 不提交，需要运行时按服务器路径准备

## 5. 当前 FITS 结果概览

`gotta_asteroids.fits` 是筛选后的“GOTTA 已匹配已知小行星 detection 总表”，不是 unknown/linking 结果。
它包含四类信息：

1. 已知小行星预测位置: `name`, `number`, `ra`, `dec`, `mag`, `epoch`, `source_file`
2. 实测 catalog 源信息: `objID`, `X_Win`, `Y_Win`, `RA_Win`, `DEC_Win`, `Mag_Kron`, `Flux_*`, `Mag_*`, `PSF` 等
3. SBDB 小行星/轨道信息: `object_*`, `orbit_*`, `query_id`, `signature_*`
4. JPL Horizons 几何和运动信息: `r_AU`, `delta_AU`, `phase_deg`, `RA_rate_arcsec_hour`, `DEC_rate_arcsec_hour`, `ang_rate_arcsec_hour`, `ang_rate_deg_day`, `horizons_failed`

完整逐列说明见 `docs/FITS_COLUMNS.md`。处理方法细节见 `docs/METHOD_KNOWN_ASTEROID_EXTRACTION.md`。

## 6. 常用命令

```bash
# 生成字段说明
python3 scripts/describe_fits_columns.py gotta_asteroids.fits --out docs/FITS_COLUMNS.md

# 从总表生成轨道分布和 RA/Dec 分布图
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/plot_gotta_asteroids.py gotta_asteroids.fits --outdir outputs/gotta

# 生成统计摘要
/Users/island/opt/anaconda3/envs/astro/bin/python scripts/summarize_gotta_asteroids.py gotta_asteroids.fits --md-out docs/GOTTA_STATS.md --json-out outputs/gotta/gotta_stats.json

# 语法检查
python3 -m py_compile scripts/*.py smt_known_asteroid/*.py remote_foundation/*.py remote_foundation/astorb/*.py
```

本机默认 `python3` 的 `matplotlib/healpy` 环境不完整；`astro` conda 环境可用于绘图和 notebook 风格复现。
