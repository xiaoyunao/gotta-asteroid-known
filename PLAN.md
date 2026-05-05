# PLAN

## Current objective

建立 GOTTA 已知小行星探测处理仓库，收集可复用程序，整理处理顺序和
`all_asteroids.fits` 结果字段说明，并推送到一个新的远端仓库。

## Milestones

1. 初始化本地 git 仓库和项目记忆文件
2. 下载服务器 `/data/proc/xiaoyunao/all_asteroids.fits`
3. 检查 `/Volumes/Foundation/Asteroid` 下 `.py` 和 `.ipynb` 文件，筛选有用脚本
4. 参考 `/Users/island/Desktop/smt_asteroid` 迁移已知小行星处理、SBDB/JPL 匹配和绘图程序
5. 读取 FITS 文件，生成列名、类型和含义说明
6. 创建远端仓库并推送一次

## Outstanding issues

- 尚未下载 GOTTA 总表
- 尚未确认远端参考目录中哪些脚本最有用
- 尚未生成字段说明文档

## Validation criteria

- `all_asteroids.fits` 存在于本地工作区但不提交 git
- 有用脚本已按用途放入当前仓库
- Markdown 文档写明处理顺序、脚本用途和最终结果字段
- Python 文件至少通过语法检查
- 本地 git 仓库已推送到新建远端

## Next recommended steps

1. 下载 FITS 数据
2. 拉取并审阅远端参考脚本
3. 迁移程序并生成文档

