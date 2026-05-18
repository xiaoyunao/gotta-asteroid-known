# PLAN

## Current objective

继续审阅并小修 `paper_draft/v6.tex` 和 `paper_draft/v6.pdf`。保持科学定位为
GOTTA Prototype known-asteroid extraction and statistical performance evaluation。
当前重点是人工检查 v6 附录中的两张光变 mosaic、
更新后的 24 行 Appendix Table A.1、Section 5 光变表述和最终 PDF 排版。

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
23. 已生成 v6：整合同事光变分析方法，加入 LS/PDM/FFT、周期聚类、P/2P Fourier+BIC、局部周期扫描和初步结果表述；后续光变结果已继续更新
24. 已将 v6 workflow figure 换回原始 `known_object_processing.png`，把 `nightly_top5` 移入 Section 4.1，把 example cross-match diagnostic 移到 Section 4.3 末尾
25. 已新增 `tables_v6/period_reliable_objects.tex` 主文表结构，并编译生成 `paper_draft/v6.pdf`
26. 已小修 v6 浮动体位置：将大部分 `figure*`/`table*` 改为局部 float，并加入 `placeins`/`\FloatBarrier`
27. 已加入 `figures_v6/lightcurve.png` 作为 Section 5 的早期 folded-light-curve summary figure，后续已由两张新 Fig. 11 mosaic 取代
28. 已清理 Software 清单，删除未实际使用的 SExtractor、SCAMP、astrometry.net，补保留实际使用的 SciPy、healpy/HEALPix 等工具库
29. 已根据 `/Users/island/Desktop/final_period_table.tsv` 和 `/Users/island/Desktop/all.fits` 生成早期 Table 7：21 行、14 reliable、7 questionable；该版本已被更新 TSV 取代
30. 已将 Fig. 2 workflow 图缩小到 80% 宽度并限制高度，避免 float-too-large
31. 已在 v6 Software 清单中删除 PyAstronomy，并加入周期聚类/分析相关的 scikit-learn
32. 已美化 v6 Fig. 5/6/8/9/10：柱状图使用 `alpha=0.5`、细边线和浅网格；Fig. 5/6 密度面板改为 `viridis` 小圆点逐点散点，颜色使用高分辨率 Gaussian-smoothed 局部密度插值，避免粗分箱色块，colorbar 更窄
33. 已用 `/Users/yunaoxiao/Downloads/final_period_table_merged_updated.tsv` 更新 v6 光变结果：Table 7 改为 24 行，`Final_Quality` 为 12 reliable 和 12 questionable；Fig. 11 改为 `lightcurve_reliable.png` 和 `lightcurve_questionable.png` 两张 mosaic 共用一条图注；正文区分 `Quality` 的 LS/PDM/FFT match-point 搜索一致性含义和 `Final_Quality` 的最终 folded-light-curve/sampling assessment
34. 已将两张光变 mosaic 和验证表移入 Appendix：Figures A.1/A.2 分页显示，Appendix Table A.1 全列居中，删除 `N_{\rm GOTTA}` 和 `N_{\rm 60cm}`，保留 `N_{\rm eff}` 并加入 `N_{\rm total}`

## Outstanding issues

- 后续新增统计和图时必须默认使用 `gotta_asteroids.fits`
- 轨道图 `outputs/asteroid_orbits.png` 必须保持当前 notebook 格式，不随意改样式
- v6 后续小修应直接覆盖 `paper_draft/figures_v6/`、`paper_draft/tables_v6/` 和 `paper_draft/v6.pdf`，不要再新建 v7，除非用户明确要求
- `paper_draft/v6.tex` 中 Received/accepted 日期、最终 grant list、完整 co-author list 仍需共同作者最终确认
- 光变分析方法已整合入 v6，Table 7 已按 `final_period_table_merged_updated.tsv` 更新为 24 行；仍建议人工检查表格含义和 reliable/questionable 标记
- Fig. 5/6/8/9/10 已重画，两张光变 mosaic 和验证表已移入 Appendix；仍建议人工确认打印版中的柱状图透明度、密度点大小、平滑密度色带、colorbar、Appendix figure panel 字号和 Appendix Table A.1 可读性
- 需要确认外部周期数据库来源是否为 MPC、LCDB、ALCDEF 或其他数据库，正文目前保守写作 external/literature period database
- 当前本机可用 `tectonic`；未发现 `/Library/TeX/texbin/xelatex` 或 `latexmk`

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
- 当前 `paper_draft/v6.pdf` 已由 `tectonic` 编译生成，共 28 页，A4 页面尺寸 `595.28 x 841.89 pts`
- v6 Section 5 不再是 placeholder，已整合 quality control、LS、PDM、插值 FFT、period clustering、P/2P、Fourier fit、BIC、visual inspection 和局部周期扫描
- v6 `v6.log` 未发现 undefined references、undefined citations、overfull 或 float-too-large
- v6 workflow figure 已换回原始 `known_object_processing.png`
- v6 `nightly_top5` 表已移到 Section 4.1，example diagnostic 已移到 Section 4.3
- v6 已加入 `figures_v6/lightcurve_reliable.png` 和 `figures_v6/lightcurve_questionable.png`，PDF 文本抽取显示 Appendix Figures A.1/A.2 位于 pages 24/25
- v6 Table 7 已由 `final_period_table_merged_updated.tsv` 更新为 24 行表，`Final_Quality` 为 12 reliable 和 12 questionable；后续已移入 Appendix Table A.1，PDF 文本抽取显示其位于 page 26
- v6 Software 清单已删除 SExtractor、SCAMP、astrometry.net、PyAstronomy，并加入 scikit-learn
- v6 Fig. 2 workflow 图已缩小并通过编译，无 float-too-large
- v6 Fig. 5/6/8/9/10 已重新生成并编译入 `paper_draft/v6.pdf`

## Next recommended steps

1. 人工检查更新后的 `paper_draft/v6.pdf` 中 Appendix Figures A.1/A.2、Appendix Table A.1、Section 5 光变表述和引用跳转
2. 确认外部周期数据库来源；若实际为 LCDB/ALCDEF，正文和表头应改为 LCDB/ALCDEF literature period
3. 确认作者、单位、致谢和硬件参数
4. 如需重画 v6 统计图表，运行 `/Users/island/opt/anaconda3/bin/python scripts/generate_paper_products.py gotta_asteroids.fits --outdir paper_draft --paper-version v6`
5. 如需重编 PDF，本机可运行 `cd paper_draft && tectonic v6.tex --keep-logs --keep-intermediates`；旧机器如有 TeXLive，也可运行 `/Library/TeX/texbin/xelatex -interaction=nonstopmode -halt-on-error v6.tex`，必要时执行两遍
