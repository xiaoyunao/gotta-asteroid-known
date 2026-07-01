# PLAN

## Current objective

准备根据审稿意见重新绘制或微调 v9 图表资产。
默认只修改 `scripts/generate_paper_products.py`、`paper_draft/figures_v9/`、`paper_draft/tables_v9/`
以及必要的项目记忆文件；不改 `paper_draft/v9.tex` 或正文，除非用户明确要求。
优先复用现有 `gotta_asteroids.fits`、现有 v9 图表目录和现有生成函数。
收到审稿意见后，先逐条映射到具体图号/表号、生成函数、输入数据和输出文件，再做最小范围修改。
已按第一条审稿意见新建独立目录 `reviewer_figures_20260701/`，用于放更新后的审稿回复图资产。
Fig. 1 的正确输入曝光已改为 `stpxl-0592_20250204_0001_3_cat.fits.gz`。
已生成全源选择图：
`reviewer_figures_20260701/fig1_all_cutouts_selection.png` 和 `reviewer_figures_20260701/fig1_all_cutouts_selection.pdf`，
包含该曝光全部 31 个 matched-source cutouts，供用户选择最终 4 个目标。
当前 4-target draft 已生成：
`reviewer_figures_20260701/fig1_review_cutouts.png` 和 `reviewer_figures_20260701/fig1_review_cutouts.pdf`。
该图使用左侧单次曝光全幅 panel + 右侧 `2 x 2` enlarged cutouts，用户已选择 selection-sheet 编号
`2, 9, 12, 21`，对应 `(559) Nanon`、`(18234) 4262 T-1`、`(27028) 1998 QS98`、
`(194920) 2002 AB124`。
图像显示已按用户反馈改为 full-frame zscale、cutouts 统一 scale、无 axes/spine 边框、四段式中心留空 marker。
最新小修：左侧 marker 加长且更靠近中心；正式 4-panel 图左右两侧的 `1,2,3,4` 编号已删除；
右侧 cutout 标注中的 `g_{\rm aper}`、`\mu` 和 `hr^{-1}` 已改为 bold mathtext。

历史目标：按导师返回意见继续修订 `paper_draft/v9.tex` 和 `paper_draft/v9.pdf`。
保持科学定位为 GOTTA Prototype known-asteroid extraction and statistical performance evaluation。
当前 v9 已完成投稿前一致性修订、终稿通读报告清理和后续小修：matching/Gaia mask 统一为 1 arcsec，
删除 predicted magnitude filtering 表述，周期验证表已移到正文，Appendix 只保留
light-curve figures，Table 5 已通过 `\FloatBarrier` 保持在 Discussion 前，Appendix A 图页已调整，
Discussion 中机器学习和光变科学价值表述已小修。workflow 图只做节点文字 raster 小修，v9 继续使用最终 2x PNG：
`paper_draft/figures_v9/known_object_processing_minimal_edit_final_2x.png`。
已生成 Overleaf 修改包 `paper_draft/v9_overleaf_package_20260602.zip`，供用户上传后手动修改。
用户已明确要求本地不要继续改文章正文；当前只辅助重画/重发表格和图片资产。
已更新 v9 的 Fig. 6 photometric statistics、Table 2、Table 3，并新增 orbit-class composition pie figure。
后续又按用户要求将 Fig. 6 右下 y 轴改为 `\Delta m [mag]`，并给 orbit-class 饼图加上 non-MBA 指向细分饼图的箭头。
Table 2 fraction 表头已修正为 `Detection fraction`/`Object fraction` 第一行、`(%)` 第二行。
Table 2 已进一步放宽：用 `\makebox[\textwidth][c]{...}` 居中伸出版心，增加 `Orbit class` 列宽和列间距。
Table 2 最新调整为 `tabular*{1.10\textwidth}`：第 2--3 列固定小间距，其余数值列用 `\extracolsep{\fill}` 放开。
已新增两个指定 light-curve 子图裁剪资产：`lightcurve_25745_reliable_crop.png` 和 `lightcurve_51965_questionable_crop.png`，尺寸均为 `1500 x 1200 px`。
后续重点是接收用户在 Overleaf 修改后的 tex/zip 或继续按需提供单独图表资产；不要新建 v10，除非用户明确要求。

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
35. 已修正 Appendix 排版和 Table A.1：Appendix A 标题与 Figure A.1 同页，Figure A.2 单独一页；Table A.1 列顺序为 `N_{\rm total}` 后接 `N_{\rm eff}`，行排序为 reliable 在前、questionable 在后，各组内按 object ID 升序
36. 已更新 v6 作者和版面：Feiyang Tian 为第二作者，Hu Zou 为第三作者和通讯作者（`zouhu@nao.cas.cn`），第二单位邮编改为 `100049`，Fig. 3 改为 75% 宽，Fig. 5 和 Fig. 10 缩小以减少图下空白
37. 已按 GPT Pro 意见生成 v7：重写 Method 星历和 Gaia mask，删除主文 Fig. 8/Table 4/Table 5，Fig. 6 加 magnitude running median，Fig. 10 改为单 panel CDF，Fig. 9 移到 Section 4.1，新增 NEO/PHA 子集统计和主文 reliable period 表，Appendix Table A.1 删除 Name 并加入 Type
38. 已恢复 v7 astrometric residual 图右下角为 v6 的 `viridis` 局部密度散点底图，同时保留 running median 和 16--84 percentile 阴影
39. 已按 GPT Pro 意见生成 v8：摘要结果导向压缩，光变方法移入 Section 3.4，光变结果移入 Section 4.5，Discussion 改为 Section 5，主文 reliable period table 删除，新 workflow PNG 插入 Fig. 2，Fig. 5 增加 median 图例，Fig. 7/8 改为 binned median，Fig. 9 改为 detection-count histogram，Table 1 和 Appendix Table A.1 排版更新
40. 已按用户小修 v8：Fig. 2 LaTeX 去掉显式宽度并通过 PNG DPI 元数据控制自然打印尺寸，原 4.4/4.5 合并为 `Temporal Sampling and Pilot Light-Curve Results`，Fig. 9 改为前文 histogram 风格，并在光变结果段补充可靠周期的物理解释
41. 已按用户最后意见更新 v8 workflow 图：上游链条右移、Gaia label 改为 `within 1 arcsec`、四个分支 label 固定在箭头右侧，并将 no/yes 分支箭头延伸到下方框边缘后重新编译 `paper_draft/v8.pdf`
42. 已整理 v8 workflow 图文件：最终使用 `figures_v8/known_object_processing_minimal_edit_final_2x.png`，删除 v8 中未使用的旧 workflow/mermaid 中间文件和 `outputs/known_object_processing_updated_v7.png`
43. 已基于 v8 生成 v9 投稿前修订稿：删除 predicted magnitude cut 叙述，matching/Gaia mask 统一 1 arcsec，周期验证表移入正文并删除 Type 列，Discussion 删除 trailing-length 公式，Fig. 9 和表注/引用做最终小修
44. 已小修 v9：移除 Table 5 后的 `\FloatBarrier` 让 Discussion 前移，补充 Table 5 Search flag 说明，移动 ADES PSV `>=3` 句子到 Section 3.3，删除 formal detection-efficiency 句子，首次写全 `Xinglong 60/90 cm Schmidt Telescope`，并让 Appendix A 标题与 Fig. A.1 同页
45. 已修正 v9 Appendix A 两张 folded light-curve figure 插入顺序，使 Fig. A.1/Fig. A.2 与 caption 逻辑对应
46. 已修正 v9 Discussion 中机器学习 cutout-recognition 模块范围：未来同时接入 known-object recovery 和 unknown-moving-object search；Section 4.4 光变结果改为强调 retained candidates 无公开周期测量、reliable solutions 具有科学价值
47. 已完成 v9 终稿前基线检查：本地 `main` 与 `origin/main` 同步，`paper_draft/v9.pdf` 可重编，共 25 页，日志无严重 LaTeX 问题；确认 Appendix A 两张图虽文件名与 caption 对调，但内容与 Fig. A.1/Fig. A.2 caption 对应正确
48. 已按 v9 终稿通读报告清理：Fig. 2 节点改为 `Sky-coordinate association`，Appendix 两张光变 PNG 文件名/内容/caption/label 统一，Table 5 通过 `\FloatBarrier` 保持在 Discussion 前，光变 `new period measurements` 表述改为更保守的 period estimates，Abstract/Discussion 等 AI 感句子已压实，正式 bibliography DOI 已补齐；`Larson2003` BAAS 引用改为 DOI-bearing `Drake2009`
49. 已初始化导师返回意见修订会话：本地 `main` 与 `origin/main` 同步，当前等待用户提供精确意见后继续直接修订 v9
50. 已生成 Overleaf 修改包 `paper_draft/v9_overleaf_package_20260602.zip`：包含 `v9.tex`、`v9.pdf`、`raa.cls`、`raa.bst`、`figures_v9/`、`tables_v9/`，解压后可直接编译
51. 已按用户要求只重画 v9 图表、不改文章正文：更新 Fig. 6、Table 2、Table 3，并新增 `figures_v9/orbit_class_composition_pies.{png,pdf}`
52. 已小修两个 v9 图：Fig. 6 右下 y 轴改为 `\Delta m [mag]`，新增饼图加 non-MBA 关联箭头
53. 已修正 Table 2 fraction 表头换行位置，并通过临时 v9 编译确认无 overfull
54. 已放宽 Table 2 版式：表格居中略伸出版心，`Orbit class` 列和列间距加宽，临时 v9 编译无 overfull
55. 已针对 Table 2 局部列距再调：第 2--3 列缩小为固定 `10pt`，第 3 列后自动分配剩余空间，临时 v9 编译无 overfull
56. 已从 v9 light-curve mosaics 截取两个同尺寸子图：reliable 中 `25745` 和 questionable 中 `51965`
57. 已初始化审稿意见重画图会话：本地 `main` 与 `origin/main` 同步，确认当前图表主线为 `figures_v9`/`tables_v9` 和 `scripts/generate_paper_products.py`
58. 已新建 `reviewer_figures_20260701/` 并生成 revised Fig. 1 candidate：左侧全幅单次曝光标记 4 个目标，右侧 `2 x 2` 放大 cutouts 标注 object ID、`g_{\rm aper}`、angular rate 和 O-C separation
59. 已修正 Fig. 1 输入曝光为 `stpxl-0592_20250204_0001_3_cat.fits.gz`，并生成包含全部 31 个 matched sources 的 `fig1_all_cutouts_selection`；4-target draft 已改为 log stretch、无边框、空心十字 marker
60. 已按用户选择将 Fig. 1 四个目标改为 selection-sheet `2, 9, 12, 21`；full-frame 改为 zscale，cutouts 改为统一 scale，marker 改为中心留空的四段短线
61. 已微调 Fig. 1：左侧 marker 加长并缩小中心留空距离，删除正式图左右两侧 `1,2,3,4` 编号，右侧数学标注改为粗体

## Outstanding issues

- Fig. 1 已按用户最近反馈微调，等待最终视觉确认
- 4 个 selection-sheet 目标缺少本地 angular-rate 匹配：`2006 FT8`、`2004 JC30`、`2003 BL70`、`2009 QE23`
- 其余审稿意见中需要重画的具体图号、修改要求或示例风格尚未收到；收到后需要逐条映射到具体输出文件和生成函数
- 如果用户在 Overleaf 手动修改，应后续下载最新版 `.tex` 或完整 project zip 并同步回本地 git
- 用户当前要求本地不要改文章正文；后续除非明确要求，只提供图表资产或同步 Overleaf 已完成修改
- 后续新增统计和图时必须默认使用 `gotta_asteroids.fits`
- 轨道图 `outputs/asteroid_orbits.png` 必须保持当前 notebook 格式，不随意改样式
- v9 后续小修应直接覆盖 `paper_draft/figures_v9/`、`paper_draft/tables_v9/` 和 `paper_draft/v9.pdf`，不要再新建 v10，除非用户明确要求
- `paper_draft/v9.tex` 中 `Received 20xx month day; accepted 20xx month day`、最终 grant list、完整 co-author list 仍需共同作者最终确认
- 光变分析方法已整合入 v9 Section 3.4，结果移入 Section 4.4，周期验证表已移到正文 Table 5；仍建议人工检查表格含义、MP 定义和 tentative 标记
- Fig. 5/6/7/8/9 已重画或调整，两张光变 mosaic 保留在 Appendix，周期验证表已移到正文 Table 5；仍建议人工确认打印版中的柱状图透明度、密度点大小、colorbar、Fig. 6 右下角局部密度散点和 median band、Fig. 9 histogram、更新后的 workflow 图、Appendix figure panel 字号和正文 Table 5 可读性
- 需要确认外部周期数据库来源是否为 MPC、LCDB、ALCDEF 或其他数据库，正文目前保守写作 external/literature period database
- `Morrison1992` 为 NASA technical memorandum，未找到 DOI，已补 NASA NTRS record URL；两条 Li et al. in preparation 无 DOI
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
- 当前 `paper_draft/v6.pdf` 已由 `tectonic` 编译生成，共 26 页，A4 页面尺寸 `595.28 x 841.89 pts`
- v6 Section 5 不再是 placeholder，已整合 quality control、LS、PDM、插值 FFT、period clustering、P/2P、Fourier fit、BIC、visual inspection 和局部周期扫描
- v6 `v6.log` 未发现 undefined references、undefined citations、overfull 或 float-too-large
- v6 workflow figure 已换回原始 `known_object_processing.png`
- v6 `nightly_top5` 表已移到 Section 4.1，example diagnostic 已移到 Section 4.3
- v6 已加入 `figures_v6/lightcurve_reliable.png` 和 `figures_v6/lightcurve_questionable.png`，PDF 文本抽取显示 Appendix A title 和 Figure A.1 位于 page 23，Figure A.2 位于 page 24
- v6 Table 7 已由 `final_period_table_merged_updated.tsv` 更新为 24 行表，`Final_Quality` 为 12 reliable 和 12 questionable；后续已移入 Appendix Table A.1，PDF 文本抽取显示其位于 page 25
- v6 Software 清单已删除 SExtractor、SCAMP、astrometry.net、PyAstronomy，并加入 scikit-learn
- v6 Fig. 2 workflow 图已缩小并通过编译，无 float-too-large
- v6 Fig. 5/6/8/9/10 已重新生成并编译入 `paper_draft/v6.pdf`
- 当前 `paper_draft/v7.pdf` 已由 `tectonic` 编译生成，共 26 页，A4 页面尺寸 `595.28 x 841.89 pts`
- v7 `v7.log` 未发现 undefined references、undefined citations、overfull、float-too-large 或 LaTeX errors
- v7 PDF 文本抽取未发现内部 TODO、`This statement should`、`validation table`、`questionable final classifications` 或 `sqrt(mean...)`
- v7 Section 3.2 已扩展轨道根数到 RA/Dec 的描述，Section 3.3 已删除 cross-match 距离公式并采用 1.5 arcsec Gaia mask 表述
- v7 Fig. 6 右下角已加入 running median 和 16th--84th percentile；主文不再输入 Table 4/Table 5
- v7 astrometric residual 图右下角底图已恢复为 v6 的局部密度散点样式，并保留 running median 和 16th--84th percentile
- v7 Section 5 已新增 `tables_v7/period_reliable_main.tex` 主文可靠周期表，Appendix Table A.1 已删除 Name、加入 Type、并将极小 `\Delta P` 显示为 `<0.0001`
- 当前 `paper_draft/v8.pdf` 已由 `tectonic` 编译生成，共 26 页，A4 页面尺寸 `595.28 x 841.89 pts`
- v8 `v8.log` 未发现 undefined references、undefined citations、overfull、float-too-large 或 LaTeX errors
- v8 PDF 文本抽取未发现独立 `Light-Curve Analysis with Auxiliary Observations`、`running median`、`cumulative distribution`、`validation table`、内部 TODO 或主文 `Table 5`
- v8 Section 3.4 已加入 light-curve period-analysis method，Section 4.5 已加入 pilot rotation-period results，Discussion 变为 Section 5
- v8 Fig. 2 使用 `paper_draft/figures_v8/known_object_processing_minimal_edit_final_2x.png`
- v8 Table 1 使用 `tabularx` 固定列宽，Appendix Table A.1 有单位行、`tab:period_validation` label、`Aper` photometry label 和 `<0.0001` 极小 `\Delta P` 格式
- v8 Fig. 9 已改为 detection-count histogram，legend 显示 median = 2、84th = 6、max = 317
- v8 原 4.4/4.5 已合并为 `Temporal Sampling and Pilot Light-Curve Results`；PDF 文本抽取未发现独立 `Pilot Rotation-Period Results`
- 当前 `paper_draft/v9.pdf` 已由 `tectonic` 编译生成，共 26 页，A4 页面尺寸 `595.28 x 841.89 pts`
- v9 `v9.log` 未发现 undefined references、undefined citations、overfull、float-too-large、missing files 或 LaTeX errors
- v9 PDF 文本抽取未发现 `1.5 arcsec`、`arcsecond-level`、旧 magnitude-limit filtering、`Appendix Table`、`Table A.1`、trailing 公式、`scikit-learn`、内部 TODO 或旧 Appendix 标题
- v9 Fig. 2 caption 明确 association 基于 sky position，predicted magnitude only diagnostics
- v9 周期验证表为正文 Table 5，删除 Type 列，并用表下注释解释 `N_{\rm total}`、`N_{\rm eff}`、Phot、MP、Search、Final
- v9 小修后 `paper_draft/v9.pdf` 编译成功，共 25 页；PDF 文本抽取确认 Section 5 开始于 Table 5 前一页，Appendix A 标题和 Fig. A.1 同页
- v9 终稿前重编成功，共 25 页，A4 页面尺寸 `595.28 x 841.89 pts`；`v9.log` 未发现 undefined references、undefined citations、overfull、float-too-large、missing files 或 LaTeX errors；PDF 文本抽取未发现旧问题文本残留
- v9 通读报告清理后 `paper_draft/v9.pdf` 编译成功，共 25 页，A4 页面尺寸 `595.28 x 841.89 pts`；`v9.log` 未发现 undefined references、undefined citations、overfull、float-too-large、missing files 或 LaTeX errors；PDF 文本抽取确认 Table 5 在 pages 18--19 且先于 page 19 的 Discussion 标题，Fig. A.1/Fig. A.2 分别在 pages 22/23

## Next recommended steps

1. 用户检查 `reviewer_figures_20260701/fig1_review_cutouts.png`，确认是否还需要调整 full-frame stretch、cutout scale、marker 长度或标签位置
2. 如需继续微调，只改 `reviewer_figures_20260701/make_fig1_review.py` 并重新生成 PNG/PDF
3. 用户继续提供其余审稿意见原文、截图或整理后的逐条修改要求
4. 将每条意见映射到 v9 图号/表号、输出路径和对应生成函数
5. 对 Python 改动先跑语法检查；对生成图做尺寸检查和视觉检查
6. 更新 `WORKLOG.md` 和 `PLAN.md`，完成后视修改规模提交 git
