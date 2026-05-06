# PLAN

## Current objective

在 `paper_draft/v2.tex` 基础上生成更成熟的 RAA 风格 `paper_draft/v3.tex` 和
`paper_draft/v3.pdf`，以 `gotta_asteroids.fits` 为唯一统计和绘图输入，正文定位为
known-asteroid recovery / prototype capability evaluation。

## Milestones

1. 已初始化本地 git 仓库和项目记忆文件
2. 已从服务器总表筛选得到本地 `gotta_asteroids.fits`
3. 已检查 `/Volumes/Foundation/Asteroid` 下 `.py` 和 `.ipynb` 文件，并迁移顶层相关脚本
4. 已参考 `/Users/island/Desktop/smt_asteroid` 迁移已知小行星处理、SBDB/JPL 匹配和绘图程序
5. 已读取 `gotta_asteroids.fits`，生成列名、类型和含义说明
6. 已创建远端仓库并推送 `main`
7. 已新增论文方法说明、GOTTA 统计摘要和论文图脚本
8. 已生成并随后清理不再需要的 `paper_handoff/` packet
9. 已从 `paper_draft/v1.tex` 编译出 `paper_draft/v1.pdf`
10. 已新增 `scripts/generate_paper_products.py`，从 FITS 重新生成 v2 图表
11. 已生成 `paper_draft/v2.tex` 和 `paper_draft/v2.pdf`
12. 已新增 v3 图表/表格输出目录，主光度统计切换到 `Mag_Aper5`
13. 已生成 `paper_draft/v3.tex`，重写 Introduction/Data/Method/Results/Discussion
14. 已安装 `tectonic` 并编译生成 `paper_draft/v3.pdf`

## Outstanding issues

- 后续新增统计和图时必须默认使用 `gotta_asteroids.fits`
- 轨道图 `outputs/asteroid_orbits.png` 必须保持当前 notebook 格式，不随意改样式
- `paper_draft/v3.tex` 中 Received/accepted 日期、最终 grant list、完整 co-author list 仍需共同作者确认
- 匹配半径和星等一致性阈值未在正文写死；最终提交前需由生产配置确认
- 光变分析仍需等待协作者数据；v3 只讨论 light-curve potential，不声称 period results
- 当前安装的是 `tectonic`，不是完整 TeX Live；如需 VSCode LaTeX Workshop 默认 `xelatex/latexmk` 工作流，仍需用管理员密码安装 BasicTeX/MacTeX

## Validation criteria

- `gotta_asteroids.fits` 存在于本地工作区但不提交 git：已完成
- 有用脚本已按用途放入当前仓库：已完成
- Markdown 文档写明处理顺序、脚本用途和最终结果字段：已完成
- Python 文件至少通过语法检查：已完成
- 本地 git 仓库已推送到新建远端：`https://github.com/xiaoyunao/gotta-asteroid-known`
- `docs/METHOD_KNOWN_ASTEROID_EXTRACTION.md` 说明从测光星表到已知小行星测光信息的处理链
- `docs/GOTTA_STATS.md` 记录当前 `gotta_asteroids.fits` 基础统计
- `paper_draft/v1.pdf` 可由 `paper_draft/v1.tex` 编译得到：已完成
- `paper_draft/v2.pdf` 可由 `paper_draft/v2.tex` 编译得到：已完成
- `scripts/generate_paper_products.py` 通过 Python 语法检查：已完成
- `paper_draft/v3.tex` 不再包含 report-style 文件名、旧参数和 placeholder light-curve section
- v3 引用 key 均有对应 bibliography 条目
- v3 图表路径和 `tables_v3/` 输入均存在
- `paper_draft/v3.pdf` 已由 `tectonic` 编译生成，共 18 页

## Next recommended steps

1. 人工检查 `paper_draft/v3.pdf` 的图表版面、表格宽度和引用格式
2. 确认作者、单位、致谢、硬件参数、匹配半径和星等一致性阈值
3. 等光变分析材料到位后加入真实 period / phased light-curve 结果
4. 如需重画 v3 图表，运行 `/opt/anaconda3/bin/python3 scripts/generate_paper_products.py gotta_asteroids.fits --outdir paper_draft --paper-version v3`
5. 如需重编 PDF，运行 `cd paper_draft && tectonic v3.tex --keep-logs --keep-intermediates`
