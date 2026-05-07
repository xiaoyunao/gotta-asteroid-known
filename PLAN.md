# PLAN

## Current objective

继续审阅并小修 `paper_draft/v5.tex` 和 `paper_draft/v5.pdf`。保持科学定位为
GOTTA Prototype known-asteroid extraction and statistical performance evaluation。
当前重点是检查 v5 新增 Gaia stationary-source rejection 描述、Light-Curve
Analysis 章节、Fig. 3 拆图、Fig. 9 residual vectors、新增 top-5 asteroid 表和
最终 PDF 排版。

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
15. 已生成 v4 图表/表格，主测光统计改为 basic reduction pipeline optimal aperture 对应的 `Mag_Aper4`
16. 已生成 `paper_draft/v4.tex`，删除 Appendix A，加入 A4 papersize 和 hyperref，重写 Data/Photometry/Discussion 关键段落
17. 已编译生成 `paper_draft/v4.pdf`，页面尺寸为 A4，共 18 页
18. 已按用户截图风格小修 v4：Fig. 4/5/6 密度图去掉六边形 marker，表格统一三线表字号/间距，Fig. 9 residual vectors 加粗加长且固定箭头头部
19. 已按用户进一步要求将 Fig. 4/5 右下角密度面板改为全量散点，点颜色表示局部密度；Fig. 4 y 轴范围为 `-0.2` 到 `1.2`
20. 已更新 v4 作者列表：前 5 位顺序不变，后续按姓氏首字母加入 Shuai Feng、Bo Zhang、Yuyi Zhuang，并新增山东大学威海单位
21. 已生成 v5：加入 Gaia stationary-source rejection 方法描述，补 Huang/Han/Liu Mini-SiTian 正确引用，新增 Light-Curve Analysis 章节
22. 已将 v5 Fig. 3 拆成 sky distribution 和 orbit distribution 两张图，新增 top-5 most frequently recovered asteroid 表，Fig. 9 residual vectors 加粗加长

## Outstanding issues

- 后续新增统计和图时必须默认使用 `gotta_asteroids.fits`
- 轨道图 `outputs/asteroid_orbits.png` 必须保持当前 notebook 格式，不随意改样式
- v5 后续小修应直接覆盖 `paper_draft/figures_v5/`、`paper_draft/tables_v5/` 和 `paper_draft/v5.pdf`，不要再新建 v6，除非用户明确要求
- `paper_draft/v5.tex` 中 Received/accepted 日期、最终 grant list、完整 co-author list 仍需共同作者最终确认
- `paper_draft/v5.tex` 中 Gaia stationary-source rejection 已写入方法，但本地 `gotta_asteroids.fits` 没有 Gaia 标记列；需共同作者确认上游实现细节和最终剔除计数
- 匹配半径和星等一致性阈值未在正文写死；最终提交前需由生产配置确认
- 光变分析仍需等待协作者数据；v5 只写 auxiliary-observation validation framework，不声称 period results
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
- `paper_draft/v4.pdf` 页面尺寸为 A4：已完成，`595.28 x 841.89 pts`
- `paper_draft/v4.pdf` 已由 `tectonic` 编译生成，共 18 页
- `paper_draft/v4.tex` 无 undefined references/citations：已完成
- `paper_draft/v4.tex` 不含 `gotta_asteroids.fits`、`Mag_Aper5`、Appendix A 或内部 grant TODO 文本：已完成
- v4 图 4/5/6 密度图不再使用六边形 marker：已完成
- v4 图 4/5 右下角密度面板为全量散点，点颜色表示局部密度：已完成
- v4 表格使用统一字号、`booktabs` 三线表和保留左右列间距：已完成
- v4 Fig. 9 residual vectors 已明显加粗加长，箭头头部大小固定：已完成
- v4 作者列表已加入 Shuai Feng、Bo Zhang、Yuyi Zhuang 和山东大学威海单位：已完成
- `paper_draft/v5.pdf` 已由 `tectonic` 编译生成，共 20 页，A4 页面尺寸 `595.28 x 841.89 pts`
- v5 引用 Huang pathfinder/Han white paper/Liu asteroid light-curve 的 RAA 页码和 DOI 已按 RAA 官网核对
- v5 `v5.log` 未发现 undefined references、undefined citations 或 overfull
- v5 Section 5 使用正式标题 `Light-Curve Analysis with Auxiliary Observations`，未出现 placeholder
- v5 新增 `tables_v5/most_observed_objects.tex`，按当前 `g_{\rm aper}` 重新计算

## Next recommended steps

1. 人工检查更新后的 `paper_draft/v5.pdf` 首页作者、单位、Fig. 3 拆图、Fig. 9 residual vectors、top-5 asteroid 表、底部页边距和引用跳转
2. 确认 Gaia stationary-source rejection 的上游实现细节、剔除计数，以及是否需要在正文给出数量
3. 确认作者、单位、致谢、硬件参数、匹配半径和星等一致性阈值
4. 等光变分析材料到位后替换 Section 5 第三段，并加入真实 period / phased light-curve 结果
5. 如需重画 v5 图表，运行 `/opt/anaconda3/bin/python3 scripts/generate_paper_products.py gotta_asteroids.fits --outdir paper_draft --paper-version v5`
6. 如需重编 PDF，运行 `cd paper_draft && tectonic v5.tex --keep-logs --keep-intermediates`
