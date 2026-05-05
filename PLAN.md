# PLAN

## Current objective

建立 GOTTA 已知小行星论文分析工作区，收集可复用程序，整理从测光星表到已知小行星测光 detection 的处理说明，并以
`gotta_asteroids.fits` 为唯一统计和绘图输入。

## Milestones

1. 已初始化本地 git 仓库和项目记忆文件
2. 已从服务器总表筛选得到本地 `gotta_asteroids.fits`
3. 已检查 `/Volumes/Foundation/Asteroid` 下 `.py` 和 `.ipynb` 文件，并迁移顶层相关脚本
4. 已参考 `/Users/island/Desktop/smt_asteroid` 迁移已知小行星处理、SBDB/JPL 匹配和绘图程序
5. 已读取 `gotta_asteroids.fits`，生成列名、类型和含义说明
6. 已创建远端仓库并推送 `main`
7. 已新增论文方法说明、GOTTA 统计摘要和论文图脚本

## Outstanding issues

- 后续新增统计和图时必须默认使用 `gotta_asteroids.fits`
- 轨道图 `outputs/asteroid_orbits.png` 必须保持当前 notebook 格式，不随意改样式

## Validation criteria

- `gotta_asteroids.fits` 存在于本地工作区但不提交 git：已完成
- 有用脚本已按用途放入当前仓库：已完成
- Markdown 文档写明处理顺序、脚本用途和最终结果字段：已完成
- Python 文件至少通过语法检查：已完成
- 本地 git 仓库已推送到新建远端：`https://github.com/xiaoyunao/gotta-asteroid-known`
- `docs/METHOD_KNOWN_ASTEROID_EXTRACTION.md` 说明从测光星表到已知小行星测光信息的处理链
- `docs/GOTTA_STATS.md` 记录当前 `gotta_asteroids.fits` 基础统计

## Next recommended steps

1. 等论文 prompt 明确后，继续补充额外统计量和图
2. 如需重新生成字段说明，运行 `python3 scripts/describe_fits_columns.py gotta_asteroids.fits --out docs/FITS_COLUMNS.md`
