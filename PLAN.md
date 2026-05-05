# PLAN

## Current objective

建立 GOTTA 已知小行星探测处理仓库，收集可复用程序，整理处理顺序和
`all_asteroids.fits` 结果字段说明，并推送到一个新的远端仓库。

## Milestones

1. 已初始化本地 git 仓库和项目记忆文件
2. 已下载服务器 `/data/proc/xiaoyunao/all_asteroids.fits`
3. 已检查 `/Volumes/Foundation/Asteroid` 下 `.py` 和 `.ipynb` 文件，并迁移顶层相关脚本
4. 已参考 `/Users/island/Desktop/smt_asteroid` 迁移已知小行星处理、SBDB/JPL 匹配和绘图程序
5. 已读取 FITS 文件，生成列名、类型和含义说明
6. 已创建远端仓库并推送 `main`

## Outstanding issues

- 若需要完全复刻 `sitian_stats.ipynb` 的 healpix 图，需要在有可用 `healpy` 的环境运行 notebook 或 `sitian_stats_cell_1.py`

## Validation criteria

- `all_asteroids.fits` 存在于本地工作区但不提交 git：已完成
- 有用脚本已按用途放入当前仓库：已完成
- Markdown 文档写明处理顺序、脚本用途和最终结果字段：已完成
- Python 文件至少通过语法检查：已完成
- 本地 git 仓库已推送到新建远端：`https://github.com/xiaoyunao/gotta-asteroid-known`

## Next recommended steps

1. 如需完全复刻 notebook healpix 图，在有可用 `healpy` 的环境运行 `smt_known_asteroid/sitian_stats_cell_1.py`
2. 如需重新生成字段说明，运行 `python3 scripts/describe_fits_columns.py all_asteroids.fits --out docs/FITS_COLUMNS.md`
