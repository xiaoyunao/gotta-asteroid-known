# WORKLOG

## 2026-05-05

- task: 下载 GOTTA 总表、迁移已知小行星处理程序并生成文档
- files_changed: `remote_foundation/`, `smt_known_asteroid/`, `scripts/describe_fits_columns.py`, `scripts/plot_all_asteroids_summary.py`, `docs/PROCESSING_ORDER.md`, `docs/FITS_COLUMNS.md`, `README.md`, `PLAN.md`, `.gitignore`
- commands_run: `scp -P 9553 xiaoya@159.226.170.185:/data/proc/xiaoyunao/all_asteroids.fits .`; `ssh yunaoxiao@100.67.138.26 find /Volumes/Foundation/Asteroid -type f`; `scp yunaoxiao@100.67.138.26:/Volumes/Foundation/Asteroid/*.py remote_foundation/`; `scp yunaoxiao@100.67.138.26:/Volumes/Foundation/Asteroid/*.ipynb remote_foundation/`; `python3 scripts/describe_fits_columns.py all_asteroids.fits --out docs/FITS_COLUMNS.md`; `python3 scripts/plot_all_asteroids_summary.py all_asteroids.fits --outdir outputs`; `python3 -m py_compile scripts/describe_fits_columns.py scripts/plot_all_asteroids_summary.py smt_known_asteroid/*.py remote_foundation/*.py remote_foundation/astorb/*.py`; `gh repo create gotta-asteroid-known --private --source=. --remote=origin`; `git push -u origin main`
- key_findings:
  - `all_asteroids.fits` 已下载到本地，大小约 `183M`
  - FITS 表共有 `162933` 行、`164` 列、`18123` 个唯一 `query_id`
  - 表包含已知小行星预测位置、实测 catalog 源、SBDB 元数据/轨道根数、JPL Horizons 几何和角速度
  - `/Volumes/Foundation/Asteroid` 中主要有用文件是 `sitian_match_asteriod_multi.py`、`asteroids_jpl.py`、`sitian_stats.ipynb`、`test_sbdb.ipynb`、`astorb/*.py`
  - SMT 项目中更工程化的主流程位于 `known_asteroid/`，已迁移为 `smt_known_asteroid/`
- validation:
  - `docs/FITS_COLUMNS.md` 已由实际 FITS header 生成
  - `outputs/asteroid_orbits.png` 和 `outputs/all_radec_distribution.png` 已成功生成（输出目录不提交）；可用环境为 `/Users/island/opt/anaconda3/envs/astro/bin/python`
  - Python 语法检查通过
  - 已创建远端仓库 `https://github.com/xiaoyunao/gotta-asteroid-known`
  - 已推送 `main` 到远端仓库
- remaining_issues:
  - 默认 `python3` 的 `healpy` 不可用；`astro` conda 环境可用
- next_step:
  - 如需完全复刻 notebook healpix 图，用 `/Users/island/opt/anaconda3/envs/astro/bin/python` 运行 `smt_known_asteroid/sitian_stats_cell_1.py`

- task: 初始化 GOTTA 小行星处理仓库
- files_changed: `README.md`, `WORKLOG.md`, `PLAN.md`, `.gitignore`
- commands_run: `git init -b main`
- key_findings:
  - 当前目录原本为空，且不是 git 仓库
  - 参考项目为 `/Users/island/Desktop/smt_asteroid`
- validation:
  - 已初始化本地 git 仓库
- remaining_issues:
  - 需要下载 `all_asteroids.fits`
  - 需要从远端 `/Volumes/Foundation/Asteroid` 筛选并迁移有用脚本
  - 需要整理流程顺序、输出字段说明并推送到新远端仓库
- next_step:
  - 下载数据并抓取远端 Python / notebook 脚本清单
